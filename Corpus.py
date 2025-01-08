import re
from Author import Author
import pandas as pd
import scipy as sp
import numpy as np

#--------------------------
# la classe Document qui est une classe mère pour les classes reditDocuMent et ArxivDocument
# --------------------------------------

class Corpus  :
    def __init__(self , nom , authors = {}, aut2id = {}, id2doc = {}, ndoc = 0, naut = 0) :
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
    
    
     
     
    #ajouter un document au corpus
    def add(self , doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author()
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)
        
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
    
    def search(self, mot):
        pattern = re.compile(r'\b' + re.escape(mot) + r'\b', re.IGNORECASE)
        matches = pattern.finditer(str(self))
        return [match.group(0) for match in matches]
        
    def concorde(self, mot, context_size=30):
        pattern = re.compile(r'(.{0,' + str(context_size) + r'})\b' + re.escape(mot) + r'\b(.{0,' + str(context_size) + r'})', re.IGNORECASE)
        matches = pattern.finditer(str(self))
        
        results = []
        for match in matches:
            left_context = match.group(1)
            found_keyword = match.group(0)
            right_context = match.group(2)
            results.append((left_context, found_keyword, right_context))
        
        df = pd.DataFrame(results, columns=['contexte gauche', 'motif trouvé', 'contexte droit'])
        return df
    
    
    
#-------------------------- 
# la classe SearchEngine qui permet de rechercher des documents dans un corpus
# --------------------------------------

class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus

    def construire_matrice(self):
        vocab = {}
        for doc in self.corpus.id2doc.values():  # Utilisation de self.corpus.id2doc
            words = doc.texte.split()
            for word in words:
                if word not in vocab:
                    vocab[word] = {
                        'unique_id': len(vocab),
                        'total_occurrences': 1
                    }
                else:
                    vocab[word]['total_occurrences'] += 1

        n_doc = len(self.corpus.id2doc)  # Nombre de documents
        n_mot = len(vocab)  # Nombre de mots dans le vocabulaire
        ligne, colonne, data = [], [], []
        
        for i, doc in enumerate(self.corpus.id2doc.values()):
            words = doc.texte.split()
            for word in words:
                if word in vocab:
                    ligne.append(i)  # Ajouter l'index du document
                    colonne.append(vocab[word]['unique_id'])  # Index unique du mot
                    data.append(1)

        # Créer une matrice creuse TF
        mat_TF = sp.sparse.csr_matrix((data, (ligne, colonne)), shape=(n_doc, n_mot))
        
        # Calculer les occurrences globales
        occ_total_corpus = mat_TF.sum()
        doc_freq = (mat_TF > 0).sum(axis=0)

        # Mettre à jour le vocabulaire avec la fréquence des documents
        for word in vocab:
            vocab[word]['doc_freq'] = doc_freq[0, vocab[word]['unique_id']]

        vocab['occ_total_corpus'] = occ_total_corpus
        return mat_TF, vocab

    def search(self, mots_cles, nbdocument=5):
    
        # Construire la matrice TF et le vocabulaire
        mat_TF, vocab = self.construire_matrice()

        # Initialiser le vecteur de la requête
        query_vector = np.zeros((mat_TF.shape[1]))

        # Construire le vecteur pour chaque mot-clé
        for word in mots_cles.split():
            if word in vocab:
                query_vector[vocab[word]['unique_id']] = 1  

        
        query_norm = np.linalg.norm(query_vector)
        if query_norm == 0:
            return "Aucun mot clé fourni ne se trouve dans le corpus."

        
        mat_dense = mat_TF.toarray()  
        doc_norms = np.linalg.norm(mat_dense, axis=1)
        scores = np.zeros(mat_dense.shape[0])

        for i in range(mat_dense.shape[0]):
            if doc_norms[i] != 0:
                scores[i] = mat_dense[i].dot(query_vector) / (doc_norms[i] * query_norm)

        
        best_docs_indices = np.argsort(scores)[::-1][:nbdocument]

        # Construire les résultats
        results = []
        for i in best_docs_indices:
            if scores[i] > 0:
                doc = self.corpus.id2doc[i + 1] 
                matching_words = [
                    word for word in mots_cles.split()
                    if word in vocab and mat_dense[i, vocab[word]['unique_id']] > 0
                ]
                results.append({
                    "mot_cle": ", ".join(matching_words),  
                    "titre_document": doc.titre,  
                    "score": scores[i] ,  
                    "identifiant": i, 
                    "source du document": doc.type ,
                    "lien": doc.url
                })
                
                # Retourner un DataFrame des résultats
                df = pd.DataFrame(results, columns=["mot_cle", "titre_document", "score" , "identifiant" , "source du document"  ,"lien"])
                
               

        
        return df
    

