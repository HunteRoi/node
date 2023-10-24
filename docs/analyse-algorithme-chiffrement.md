# Choix des algorithmes de chiffrements

## Contexte

Dans le contexte de notre application distribuée, caractérisée par de nombreux flux de données et des échanges fréquents de commandes, la sécurité des échanges est cruciale. Cependant, il est également impératif que ces mécanismes de sécurité n'ajoutent pas une charge excessive au système.

Pour cela, nous allons voir les types de chiffrement afin de déterminer le plus optimal.

## Algorithmes Symétriques

Les algorithmes de chiffrement symétriques utilisent une seule clé pour le chiffrement et le déchiffrement. Ils sont rapides et sont couramment utilisés pour le chiffrement de données en vrac comme les disques durs et les fichiers.

### Exemples d'Algorithmes Symétriques

- Advanced Encryption Standard (AES)
- Data Encryption Standard (DES)
- Triple DES (3DES

## Algorithmes Asymétriques

Les algorithmes de chiffrement asymétriques utilisent une paire de clés, une clé publique pour le chiffrement et une clé privée pour le déchiffrement. Ils sont plus lents que les algorithmes symétriques mais offrent un niveau de sécurité plus élevé.

### Exemples d'Algorithmes Asymétriques

- Rivest-Shamir-Adleman (RSA)
- Digital Signature Algorithm (DSA)
- Elliptic Curve Cryptography (ECC)

## Comparaison

| Critères          | Algorithmes Symétriques                                           | Algorithmes Asymétriques                                                   |
|-------------------|-------------------------------------------------------------------|----------------------------------------------------------------------------|
| **Clés**          | Une clé partagée pour le chiffrement et le déchiffrement.         | Une paire de clés publique et privée.                                      |
| **Vitesse**       | Rapides car ils utilisent une seule clé pour le chiffrement et le déchiffrement. | Plus lents en raison de la complexité mathématique impliquée.             |
| **Sécurité**      | Dépend de la longueur de la clé. Plus la clé est longue, plus le chiffrement est sécurisé. | Théoriquement plus sécurisés car basés sur des problèmes mathématiques difficiles. |
| **Taille des clés** | Les clés sont généralement plus courtes (par exemple, 128, 256 bits). | Les clés sont généralement plus longues (par exemple, 2048, 3072 bits).     |
| **Utilisation courante** | Chiffrement de données en vrac (par exemple, disques durs, fichiers). | Échange sécurisé de clés pour établir des connexions sécurisées (par exemple, HTTPS). |
| **Exemples d'algorithmes** | AES, DES, 3DES                                                  | RSA, DSA, ECC                                                              |

### Choix
On se rend compte que dans notre contexte on aura besoin de de faire des échanges de données en vrac (partarge et chiffrement de fichiers ...) masi également dés échanges de clés. d'où l'utilisation des algorithmes symétriques mais également des algorithmes asymétriques.

#### Choix de algorithmes symétriques

| Critères                       | AES                                   | DES                             | 3DES                                |
|---------------------------------|---------------------------------------|-----------------------------------|-------------------------------------|
| **Année d'introduction**       | 2001                                  | 1977                              | Années 1990 (variations de DES)     |
| **Taille de la clé**           | 128, 192 ou 256 bits                 | 56 bits                           | 112 ou 168 bits                     |
| **Nombre de tours**            | 10 tours pour AES-128, 12 tours pour AES-192, 14 tours pour AES-256 | 16 tours                         | 48 tours (16 tours effectués trois fois) |
| **Vitesse**                    | Très rapide                           | Relativement lent                 | Plus lent que AES, mais plus rapide que DES |
| **Sécurité**                   | Considéré comme très sûr, largement utilisé | Non recommandé pour les nouvelles applications en raison de sa clé courte et de sa vulnérabilité aux attaques par force brute | Plus sûr que DES en raison de l'itération des étapes, mais moins sécurisé que AES |
| **Utilisation courante**       | Utilisé dans de nombreux protocoles de sécurité, y compris TLS/SSL, IPsec et WPA2 | Utilisé dans le passé pour le chiffrement de données sensibles, mais largement remplacé par AES | Encore utilisé dans certains systèmes hérités où la compatibilité avec DES est nécessaire |
| **Flexibilité**                | Offre différentes tailles de clés pour répondre à divers besoins de sécurité | Utilise une taille de clé fixe de 56 bits | Peut être configuré pour utiliser deux ou trois clés différentes, offrant des niveaux de sécurité variables |
| **Complexité de l'implémentation** | Modérément complexe                | Relativement simple                | Plus complexe en raison de l'utilisation de trois clés et des multiples tours |

Le tableau parle de lui même il est évident que ***AES*** est le plus appropié.

#### Choix des algorithmes symétriques

| Critères                       | RSA                                   | DSA                             | ECC                              |
|---------------------------------|---------------------------------------|-----------------------------------|----------------------------------|
| **Année d'introduction**       | 1977                                  | 1991                              | Années 1980 (concept), années 2000 (standardisation)     |
| **Taille de la clé**           | 1024, 2048, 3072, 4096 bits           | 1024, 2048 bits                   | La taille des clés ECC est proportionnelle à la sécurité souhaitée (par exemple, 256, 384, 521 bits) |
| **Sécurité**                   | Dépend de la taille de la clé. Plus la clé est longue, plus le chiffrement est sûr, mais cela ralentit les opérations. Considéré comme sûr avec des clés de 2048 bits ou plus. | Utilisé principalement pour les signatures numériques et basé sur le problème du logarithme discret. Sûr avec des clés de 2048 bits. | Propose une sécurité comparable à RSA et DSA mais avec des clés plus courtes, offrant des performances et une efficacité énergétique accrues. |
| **Utilisation courante**       | Chiffrement de clés, signatures numériques, échange de clés sécurisé (parfois) | Principalement utilisé pour les signatures numériques, en particulier dans les certificats numériques. | Utilisé pour le chiffrement, les signatures numériques et les protocoles de sécurité, en particulier dans les environnements où les ressources sont limitées, tels que les appareils IoT. |
| **Efficacité**                  | Plus lent que DSA et ECC en raison de calculs plus complexes, surtout avec des clés longues. | Plus rapide que RSA pour générer des signatures. | Plus efficace que RSA avec des clés de taille équivalente, nécessite moins de ressources computationnelles. |
| **Complexité de l'implémentation** | Modérément complexe               | Relativement simple               | Modérément complexe, mais offre des performances élevées avec des clés plus courtes. |

