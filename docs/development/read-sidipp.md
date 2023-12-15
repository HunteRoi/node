# Documentation sur #12

Afin de lire un SIDIPP, il est important que :
- les informations sur le SIDIPP soient disponibles
- le contenu du SIDIPP soit également disponible (ce qui signifie qu'elles sont également sauvegardées dans la base de données)

## Une communauté a toujours un premier membre
Comme modification importante dans la portée de cette user story, il est important de pouvoir définir qu'une communauté créée commence toujours avec un premier membre enregistré.
Pour ce faire, il faut donc adapter le cas d'utilisation existant de création d'un SIDIPP afin d'ajouter le membre "créateur" à la liste des membres de cette communauté.

Cela s'accompagne donc d'un _refactoring_ de la classe `CommunityRepository` afin de pouvoir:
- créer la table "nodes" qui contiendra l'ensemble des noeuds (aka des membres) d'une communauté ;
- ajouter un membre à une communauté lors de sa création.

Tous les changements autour d'un membre et d'une communauté (l'ajout d'une clé d'authentification, d'une date de création au membre ainsi qu'à la communauté, etc.) sont également à pris en compte.

Il a été également nécessaire de créer un `IMachineService` dans le cadre de l'instanciation d'un membre de la communauté. 
En effet, il est nécessaire de pouvoir récupérer les informations de la machine (comme son adresse IP ou son code d'authentification).

## Machine service
Ce service permet d'obtenir l'adresse ip de la machine hôte ainsi que son code d'authentification attribuée par le programme. Il est donc nécessaire de créer une nouvelle classe `MachineService` qui implémente l'interface `IMachineService` et qui permet de récupérer ces informations.  
Concernant l'adresse ip de la machine, nous sommes limité à son adresse locale. Pour l'obtenir, nous utilisons la librairie `socket` qui nous permet d'obtenir l'adresse ip de la machine à l'aide de son nom d'hôte.  
Pour le code d'authentification, nous utilisons le service `UuidGeneratorService` qui nous permet de générer un code uuid unique. Nous générons le code d'autgentification de la machine lors de son ajout à une communauté. Si la machine créee la communauté, le code d'authentification lui est généré. Si la machine rejoint une communauté, le code d'authentification lui est fourni par le membre de la communauté qui l'a ajouté.
Le service `MachineService` récupère donc l'adresse ip par la librairie `socket` et le code d'authentification dans la base de données `index` pour la communauté concernée.

## Séparation de la gestion des membres et de la gestion des communautés
Afin de séparer la gestion des membres et la gestion des communautés, il est nécessaire de créer une nouvelle classe `MemberRepository` qui implémente l'interface `IMemberRepository`. Ce nouveau repository permet de gérer les membres d'une communauté.  
Le cas d'utilisation de création d'une communauté a du être modifié afin de prendre en compte cette nouvelle dépendance. Il en découle également la modification de la classe `CommunityRepository` afin d'en extraire la gestion des membres d'une communauté.

## Développement de la couche "Infrastructure"
La consultation d'une communauté consiste à visualiser les messages de celle-ci. Pour cela, il est nécessaire de créer une nouvelle table `messages` dans la base de données de la communauté afin de stocker les messages. Le contenu de cette table est composé de l'identifiant du message, de son contenu, de son membre auteur, de la date de création du message et de l'identifiant du message auquel il appartient.  
Un message peut être une idée ou une prise de position sur cette idée ou une autre prise de position. Dans la base de données, ces messages sont stockés dans la même table. Pour différencier les idées des prises de position, nous utilisons l'attribut du message parent. En effet, une idée n'a pas de message parent alors qu'une prise de position a un message parent.  
Dans l'application, nous avons créé une classe pour chaque type de message : `Idea` et `Opinion`. Ces classes contiennent : un identifiant, le contenu, le membre auteur et la date de création. La classe `Idea` ne possède pas d'attribut supplémentaire, la classe `Opinion` possède un attribut `parent` qui correspond à l'identifiant de l'idée ou de la prise de position parente.  
Pour la gestion des messages dans la base de données, nous avons créé une nouvelle classe pour chaque type de message : `IdeaRepository` et `OpinionRepository`. Ces dernières implémentent leur interface respective : `IIdeaRepository` et `IOpinionRepository`. Ces deux repository possèdent, chacun, deux méthodes : une pour ajouter une nouvelle idée ou prise de position et une pour récupérer les idées ou prises de position d'une communauté.
