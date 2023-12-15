# Documentation sur #11

## Développement de la couche "Domain"
Nous avons décidé de commencer par la couche la plus centrale (et donc la plus indépendante) appelée "Domain".
Elle contient les classes qui représentent les objets métiers de notre application.

Nous avons pris le parti de créer deux représentations métier : une pour les communautés et une pour les membres.

### Création d'un membre
Un membre est représenté par plusieurs attributs :
- une adresse IP, de type chaine de caractères
- une date de dernière connexion, de type date

### Création d'une communauté
Une communauté est représentée par plusieurs attributs :
- un identifiant, de type chaine de caractères
- un nom, de type chaine de caractères
- une description, de type chaine de caractères
- une liste de membres, de type liste de membres

## Développement de la couche "Application"
Après avoir créé les objets métiers, nous avons créé la couche "Application" qui contient les cas d'utilisation de notre application.

Ceux-ci se traduisent par des classes "case d'utilisation" qui vont développer un flux d'interaction entre l'utilisateur et l'application.

## Développement de la couche "Infrastructure"
Nous travaillons sur la génération d'un identifiant automatique. Cet identifiant sera utilisé pour identifier les communautés.

Pour cela, nous créons une classe `UuidGeneratorService` qui implémente l'interface `IIdGeneratorService`. 
Cette interface permet de fixer une structure à suivre pour tous les générateur d'identifiant.
Dans notre cas actuel, pour générer l'identifiant nous utilisons la librairie `uuid4`.

En ce qui concerne le stockage des données, nous avons choisi d'utiliser une base de données `sqlite3`. Pour valider son utilisation,
nous allons donc tester la création d'une communauté et son stockage dans la base de données.
Puisque cela repose sur le système d'exploitation et le framework "sqlite", notre test sera un test d'intégration pour la classe `CommunityRepository` implémentant l'interface `ICommunityRepository`.
Dans un deuxième temps, nous testons et implémentons l'obtention d'une communauté à partir de son identifiant depuis la base de données.
