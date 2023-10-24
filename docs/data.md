# Enregistrement des données

## Données à retenir

- **`Message`** *(correspond aux avis et prises de position)*
  - `id` (unique)
  - `texte`
  - `message parent` *(un message sans message parent est toujours une idée)*
  - `date-heure`
  - `auteur` *(noeud - clé d'authentification)*


- **`Noeud`** *(correspond aux utilisateurs)*
  - `clé d'authentification` (unique) *(clé reçue lors de l'invitation à rejoindre le réseau)*
  - `adresse ip`
  - `date de création`
  - `date de dernière connexion`


## Choix de la technologie d'enregistrement

Après analyse des données à retenir, le choix d'utiliser une base de données (PostgreSql, MariaDB...) se trouve surdimensionné.  
En effet, nous ne devons pas retenir une structure de données complexe et vouée à être modifiée.  
Le choix donc se porte sur ***un enregistrement sur fichiers***.

Pour ce choix, plusieurs technologies :
- **Fichiers simples**  
  - Gestion "à la main" de l'accès R/W des données. Cela implique une très grande rigourosité dans la gestion des accès aux fichiers, au risque de rendre toutes les données erronées.
  - Utilisation des accès fichiers pour accéder aux données.

- **SqLite**  ([Documentation](https://www.sqlite.org/index.html))
  - Gestion automatisée de l'accès R/W des données.  
  - Utilisation de SQL pour accéder aux données.

Nous choisissons ***SqLite*** pour l'enregistrement des données grâce à sa simplicité d'utilisation et de gestion des fichiers.