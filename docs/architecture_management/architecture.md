# Gestion de l'architecture du réseau

Nous allons construire le système informatique de dépôt d'idées et de prises de position sur une architecture en Peer-to-Peer : une architecture réseau distribué décentralisé.  
Cette architecture implique que chaque machine connectée au réseau (appelée noeud) doit posséder ses propres données et doit pouvoir communiquer avec les autres noeuds du réseau. Une telle architecture évite ainsi l'utilisation d'un serveur central et évite les coûts qui y sont liés.

## Types d'individus dans une communauté
### Un membre
Un membre de la communauté est un noeud autorisé à envoyer des messages (idée - prise de position). Ce noeud doit donc avoir une connexion sécurisée vis-à-vis du réseau.
Pour ce type de noeud, nous retenons son adresse ip et son port, la date d'ajout dans la communauté et son code d'authentification.

### Une personne externe
Un externe est un noeud qui n'est pas membre de la communauté. Ce noeud ne peut que consulter les messages, il ne peut pas en envoyer.

Pour se connecter au réseau, il doit joindre un noeud membre et obtenir les informations présentes sur le réseau.

## Architecture du réseau
### Connaissances d'un membre
Dans cette nouvelle version, un membre d'une communauté connait tous les membres de celle-ci. Cependant, il ne communiquera plus qu'avec ceux avec lesquels il a un lien : le membre qui l'a invité et les membres qu'il a invités.
En effet, cette conception nous parait la plus logique au niveau métier : une personne connait les membres qu'elle a invités ainsi que celui qui l'a invitée.
Ce système de communications permet de réduire le nombre de communications entre les membres d'une communauté. Si nous devions représenter les communications entre les membres d'une communauté, nous aurions un graphe de type arbre avec un noeud racine (le premier membre de la communauté) et des noeuds enfants (les membres invités par d'autres membres).

## Communication entre les noeuds
Chaque noeud doit avoir le rôle de client et de serveur. En effet, il doit pouvoir envoyer des messages aux noeuds et en recevoir de ceux-ci. Pour cela, un noeud doit posséder un socket client pour communiquer directement avec une autre machine et un socket serveur pour réceptionner tous les messages inattendus.

Tous les messages transittants entre les noeuds doivent être chiffrés. Pour cela, nous utiliserons un chiffrement asymétrique lors de l'ajout d'un nouveau membre dans une communauté. Cela est nécessaire car ils communiqueront des données sensibles telles que la clé de chiffrement commune à la communauté. Les messages envoyés au sein d'une communauté seront chiffrés symétriquement à l'aide d'une clé commune à tous les membres de la communauté.

### Leader de l'architecture
Pour notre structure en arbre, il nous parait évident que le noeud racine soit le leader de l'architecture. En effet, il est le noeud central de l'arbre et il est le noeud, par définition, le plus ancien de la communauté.

### Déconnexion d'un membre
L'architecture en arbre n'est pas défensive vis-à-vis des déconnexions des noeuds. En effet, si un noeud disparait, une moitié de l'arbre peut facilement se faire déconnectée du reste de la communauté avec lui. Pour éviter cela, nous allons mettre en place un système de gestion des déconnexions.

Si un noeud de l'arbre se déconnecte (disparait de l'arbre), seuls les noeuds liés à lui sont impactés. Le noeud père de ce noeud doit le supprimer de sa liste de noeuds fils. Les noeuds fils de ce noeud doivent trouver un nouveau père à qui se lier. C'est ici que l'intérêt de garder une liste complète des membres de la communauté prend tout son sens. En effet, les noeuds fils choisissent un nouveau père parmi les membres de la communauté.  
Pour ce faire, tout se base sur la date d'entrée dans la communauté de chaque noeud : le noeud le plus vieux correspond au créateur de la communauté et est donc le noeud racine de l'arbre par défaut. Un fils en recherche de père choisira donc parmis les noeuds plus vieux que lui. Il trouvera donc, parmis eux, son père déconnecté ainsi que ses ancêtres. Il contactera les noeuds, un par un, en commençant par le plus récent. Le premier noeud qui répondra sera son nouveau père.

La complexité de cette méthode est de O(n) avec n le nombre de noeuds de la communauté. Cependant, cette complexité est très peu probable car il est peu plausible que le noeud en recherche de père soit le plus récent de la communauté et que tous les noeuds plus vieux que lui soient déconnectés.

### Reconnexion d'un membre déconnecté
Lorsqu'un membre se reconnecte à la communauté, il doit se replacer dans l'architecture. Pour cela, il suivra le même principe qu'un noeud orphelin. Il contactera les noeuds plus vieux que lui pour trouver un nouveau père. Il doit ensuite demander à son nouveau père la nouvelle version de la base de données de la communauté.

### Partage d'une information dans la communauté
Lorsqu'un membre désire partager une information à toute la communauté (ex : ajout d'une idée), il doit envoyer cette information à son père et à ses fils. Le père et les fils doivent ensuite envoyer cette information à leur père et à leurs fils mis à part celui qui vient de leur envoyé l'information. Ainsi, l'information se propage dans toute la communauté.

### Ajout d'un nouveau membre
Lorsqu'un membre invite un nouveau membre dans la communauté, le processus d'invitation reste le même qu'auparavant. Il est important que le nouveau membre reçoive les données de la communauté dès son acceptation. Ainsi, s'il y a un problème de connexion avec le membre, il pourra se reconnecter à la communauté par lui-même.

Au niveau de l'architecture, le nouveau membre doit retenir le membre qui l'a invité comme son noeud père. Le membre qui l'a invité doit également ajouter le nouveau à sa liste de noeuds fils et propager l'information de l'ajout du nouveau membre à toute la communauté.

### Synchronisation des données
Afin d'éviter des conflits de données, il est important que tous les membres de la communauté aient la même version de la base de données. Pour cela, nous allons mettre en place un système de synchronisation des données au sein de l'architecture.

Pour réaliser cette synchronisation, le noeud racine de l'arbre prendra le rôle du leader. Il demandera à tous les noeuds de la communauté leur version de la base de données. Chaque noeud transmettra la demande à ses fils. Quand un noeud reçoit la demande et qu'il n'a pas de fils, il renverra en retour la version de sa base de données. Un noeud qui reçoit la demande et qui a des fils, attendra que tous ses fils lui aient répondu. Il comparera ensuite les versions reçues avec la sienne et renverra la version la plus récente à son père. Le noeud racine recevra donc les versions les plus récentes de la part de ses fils. Il les comparera et prendra la version la plus récente comme version à suivre pour la communauté. Il enverra ensuite cette version à tous les noeuds de la communauté. Chaque noeud fera de même avec ses fils. Ainsi, la version la plus récente de la base de données se propagera dans toute la communauté.

Il est important que durant cette opération, tous les noeuds de la communautés ne modifient pas leur base de données afin de ne pas avoir de conflits. Autrement dit, chaque noeud verrouillera la modification de sa base de données entre le moment où il reçoit la demande de version et le moment où il reçoit la version à suivre.

Cette opération de synchronisation doit être réalisée régulièrement : périodiquement et/ou à chaque fois qu'un noeud réalise une certaine opération (ex : ajout d'un nouveau membre).
