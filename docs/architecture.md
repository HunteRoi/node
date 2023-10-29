# Gestion de l'architecture du réseau

Nous allons construire le système informatique de dépôt d'idées et de prises de position sur une architecture en Peer-to-Peer : une architecture réseau distribué décentralisé.  
Cette architecture implique que chaque machine connectée au réseau (appelée noeud) doit posséder ses propres données et doit pouvoir communiquer avec les autres noeuds du réseau. Une telle architecture évite ainsi l'utilisation d'un serveur central et évite les coûts qui y sont liés.

## Connexion d'un nouveau noeud
### Un noeud membre de la communauté

Un noeud membre de la communauté est un noeud autorisé à envoyer des messages (idée - prise de position). Ce noeud doit donc avoir une connexion sécurisée vis-à-vis du réseau.

Un noeud qui veut rejoindre le réseau, en tant que membre, doit possèder une clé publique qu'il partage au noeud qui l'invite.  
Ce dernier lui envoie une clé d'authentification chiffrée à l'aide de la clé publique de l'invité.  
La clé d'authentification reçue par le noeud invité doit être déchiffrée grâce à sa clé privée. Il renvoie ensuite cette valeur déchiffrée au noeud hôte pour valider son accès membre. L'IP du nouveau noeud est enfin stockée dans la table des users sur tous les noeuds du réseau.

La clé d'authentification en clair, la clé publique de l'invité, la date de création ainsi qu'un statut de validation sont stockés sur le réseau.


**`Problème`**  
Cette méthode a un problème au niveau du lien entre l'invité et l'hôte : pour que l'invité sache contacté le noeud hôte, il doit y avoir une communication humaine de l'adresse ip et du port. Il faudrait un moyen de communiquer à l'invité un simple url et que cet url redirige vers une machine du réseau qui jouera le rôle de hôte.


## Un noeud externe

Un noeud externe est un noeud qui n'est pas membre de la communauté. Ce noeud ne peut que consulter les messages, il ne peut pas en envoyer.

Pour se connecter au réseau, il doit joindre un noeud membre et obtenir les informations présentes sur le réseau.


## Méthode de communication

Toute communications entre noeuds se fait par le biais de messages chiffrés **symétriquement**. Nous avons fait le choix d'utiliser l'algorithme de chiffrement AES (ref : [./analyse-algorithme-chiffrement.md](./analyse-algorithme-chiffrement.md)).


## Communication entre les noeuds

Chaque noeud doit avoir le rôle de client et de serveur. En effet, il doit pouvoir envoyer des messages aux noeuds et en recevoir de ceux-ci. Pour cela, un noeud doit posséder un socket client et un socket serveur.

### Connexion au réseau

Lors de la première connexion d'un nouveau noeud invité par un noeud membre au réseau, le nouveau doit se connecter au réseau avec comme premier point de contact le noeud qui l'a invité.

Lors de sa reconnexion, le noeud doit contacter tous les noeuds qu'il connait sur le réseau afin d'avoir les dernières informations. Il connait ces noeuds grâce à leur adresse ip retenue dans sa base de données.  
Il est normal qu'un noeud ne réponde pas à la demande d'informations si celui-ci est déconnecté. En toute logique, les noeuds connectés doivent répondre et doivent avoir tous les mêmes informations.  

Dans le cas où il se peut que les noeuds connectés ne soient pas tous à jour (n'ont pas tous les même données), il faudrait mettre en place un système qui fait attention aux communications sur le réseau. Pour préserver une certaine légerté de communication, pour mettre à jour ses données, le noeud reconnecté doit, dans son premier message, demander aux noeuds connectés leur date de dernière modification des informations. Si la date la plus récente est supérieur à la sienne, il doit demander les nouvelles informations au noeud / à un seul parmis les noeuds ayant envoyé cette date.

Dans le cas où tous les noeuds connectés ont toujours les mêmes informations, le noeud reconnecté demande au premier noeud qui répond ses informations.

**`Problème`**  
Un problème subsiste tout de même : une adresse ip est dynamique et peut changer à tout moment. Cela entraine que le noeud ne pourra pas contacter celui qui a changé d'adresse ip, même si ce dernier est connecté. Pour récupérer sa nouvelle adresse ip, le noeud doit soit attendre un message du noeud avec la nouvelle adresse ou soit récupérer cette adresse dans les nouvelles informations reçues du réseau.  
Cependant, ce problème est bloquant dans le cas où tous les noeuds ont changé d'adresse ip. Comment se reconnecter au réseau sans avoir de point de contact ?

### Mise à jour des informations

Lorsqu'un noeud modifie les informations (adresse ip, messages...), il doit prévenir les autres noeuds connectés du réseau. Pour cela, il envoie un message à tous les noeuds qu'il connait avec la modification.

De l'autre côté, un noeud qui reçoit un message prévenant une modification doit mettre à jour ses informations.
