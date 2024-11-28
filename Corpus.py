import re
from Author import Author
import pandas as pd

class Corpus  :
    def __init__(self , nom , authors = {}, aut2id = {}, id2doc = {}, ndoc = 0, naut = 0) :
        self.nom = ""
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
    
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

    
        
    
        
    
   
    
     
    
    