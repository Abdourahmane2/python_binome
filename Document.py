class Document :
    def __init__(self, titre="", auteur="", date="", url="", texte="" , type = "") :
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte 
        self.type = type
        
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
     
     
class reditDocuMent(Document) : 
        def __init__(self, titre="", auteur="", date="", url="", texte="" , nbmessages=0):
            super().__init__(titre, auteur, date, url, texte)
            self.nbmessages = nbmessages
        
        def gettype(self):
            return "reddit"
            
        def getnbmessages(self):
            return self.nbmessages
        
        def setnbmessages(self, nbmessages):
            self.nbmessages = nbmessages
        
        def __str__(self):
            return f"{super().__str__()} ({self.nbmessages} messages)"
        
        
class ArxivDocument(Document) :  
        def __init__(self, titre="", auteur="", date="", url="", texte="", coauthors=[]):
            super().__init__(titre, auteur, date, url, texte)
            self.coauthors = coauthors
         
        def gettype(self):
            return "arxiv"  
         
        def getauthors(self):
            return self.auteur + ", " + ", ".join(self.coauthors)    
        
        def setcoauthors(self, coauthors):
            self.coauthors = coauthors   
            
            