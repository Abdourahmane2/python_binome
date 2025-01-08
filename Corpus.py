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
        self.nom = nom #nom du corpus
        self.authors = {} # auteurs du corpus
        self.aut2id = {}  # dictionnaire qui associe un auteur à un identifiant
        self.id2doc = {} # dictionnaire qui associe un identifiant à un document
        self.ndoc = 0 #nombre de documents dans le corpus
        self.naut = 0 #nombre d'auteurs dans le corpus
    
    
     
     
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
        # Créer une représentation textuelle unifiée pour chaque document
        unified_corpus = []
        for doc in self.corpus.id2doc.values():
            # Concaténer titre, auteur et texte
            full_text = f"{doc.titre.lower()} {doc.auteur.lower()} {doc.texte.lower()}"
            unified_corpus.append(full_text)

        # Initialiser les scores pour chaque document
        scores = np.zeros(len(unified_corpus))

        # Préparer les mots-clés
        mots_cles_lower = mots_cles.lower().split()

        # Calcul des scores
        for idx, full_text in enumerate(unified_corpus):
            for word in mots_cles_lower:
                if word in full_text:
                    scores[idx] += full_text.count(word)  # Comptage des occurrences

        # Trier les documents par pertinence
        best_docs_indices = np.argsort(scores)[::-1][:nbdocument]

        # Construire les résultats
        results = []
        for i in best_docs_indices:
            if scores[i] > 0:
                doc = self.corpus.id2doc[i + 1]
                matching_words = [word for word in mots_cles_lower if word in unified_corpus[i]]
                results.append({
                    "mot_cle": ", ".join(matching_words),
                    "titre_document": doc.titre,
                    "auteur": doc.auteur,
                    "score": scores[i],
                    "identifiant": i,
                    "source_du_document": doc.type,
                    "lien": doc.url
                })

        # Retourner les résultats sous forme de DataFrame
        df = pd.DataFrame(results, columns=["mot_cle", "titre_document", "auteur", "score", "identifiant", "source_du_document", "lien"])
        return df if not df.empty else "Aucun document ne correspond aux mots-clés."
