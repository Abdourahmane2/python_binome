## Description

notre projet implémente un système de gestion et d'analyse de documents provenant de Reddit et d'Arxiv. 
Il utilise des classes Python pour modéliser les documents, les auteurs et le corpus, avec des fonctionnalités avancées comme la recherche textuelle, la construction de matrice TF et l'analyse de vocabulaire.

## Fonctionnalités principales

 - Récupération de données : Collecte des posts Reddit et des articles Arxiv.

 - Filtrage et stockage : Filtrage des documents par longueur minimale et stockage dans des classes dédiées.

 - Analyse textuelle : Nettoyage, comptage des mots, concordances et recherche textuelle dans le corpus.

 - Recherche : Recherche dans le corpus via une API ou des mots-clés avec tri par pertinence.

 - Gestion des auteurs et des documents : Ajout et gestion des auteurs et des documents au sein du corpus.

## Architecture

L'architecture repose sur plusieurs fichiers et classes :

 - Author.py : Modélise un auteur avec ses productions.

 - Document.py : Modélise un document avec des sous-classes pour Reddit et Arxiv.

 - Corpus.py : Gère un corpus contenant des documents et des auteurs.

 - tp.py : Contient le script principal pour récupérer les données, les traiter et les analyser.

## Installation

Prérequis :

 - Python 3.7+

 - Bibliothèques Python : praw, xmltodict, pandas, numpy, scipy

 - Accès à l'API Reddit (clés client et secret).

Cloner le dépôt :

git clone <https://github.com/Abdourahmane2/python_binome>
cd <python_binome>

## Installer les dépendances :

pip install -r requirements.txt

## Utilisation

Lancer le script principal :

python tp.py

Fonctionnalités incluses :

Analyse et recherche dans le corpus.

Nettoyage et statistiques des mots.

## Exemple de résultats

Nombre total de mots dans le corpus.

Concordance des mots-clés dans les documents.

Recherche et tri des documents par pertinence.

## Contribution

Pour contribuer :

 - Forkez le dépôt.

 - Créez une branche pour vos modifications :

 - git checkout -b feature/ma_nouvelle_fonctionnalite

 - Soumettez une pull request.


## Auteur

Projet réalisé par Abdourahmane et NGUYEN Do Minh Trang