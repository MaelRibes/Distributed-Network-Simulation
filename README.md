#  Distributed Network Simulation 
<p align="center"> 
<img src="src\SimPy_logo.png" width=150> <img src="src\networkx_logo.svg" width=300>
</p>
Ce projet est une simulation d'un système de réseau distribué. Il utilise la bibliothèque SimPy pour simuler le passage de messages à travers un réseau de nœuds.



## Installation 

Pour exécuter cette simulation, vous devez installer Python 3 et les bibliothèques SimPy et NetworkX. Vous pouvez les installer à l'aide de pip :
```bsh
pip install simpy networkx
```



## Usages
Pour lancer la simulation, il suffit d'exécuter le fichier *main.py*:

```bsh
python main.py
```
Il créera un réseau de trois nœuds. Il ajoutera ensuite d'autres nœuds au réseau, simulera le passage de messages d'insertions, puis supprimera l'un des nœuds du réseau.

Après avoir exécuté la simulation, un graphique du réseau sera affiché à l'aide de la bibliothèque [NetworkX](https://networkx.org/documentation/stable/tutorial.html).



## Introduction et objectifs

Dans ce projet, notre objectif a été d'implémenter une DHT en Python. Une Distributed Hash Table est une structure de données distribuée qui permet de stocker et de récupérer des informations de manière décentralisée.

Elle fonctionne en répartissant les données à travers un réseau d'ordinateurs connectés, appelés nœuds. Chaque nœud possède une partie de la table de hachage et est responsable d'une partie de l'espace de clés. 

Une clé est une chaîne de caractères qui est associée à une valeur, qui peut être une donnée, un fichier ou une autre information. Pour stocker une donnée dans la DHT, le nœud utilise une fonction de hachage pour calculer un identifiant unique à partir de la clé de cette donnée. Cet identifiant est ensuite utilisé pour déterminer le nœud responsable de stocker la donnée.

Afin de simuler les noeuds et leurs différentes interactions (envoie et réception de messages), nous avons utilisé la librairie [SimPy](https://simpy.readthedocs.io/en/latest/) pour simuler les délais de génération, de réception et de traitement des messages.



## Structure du projet

L'intérêt d'une DHT est de proposer une structure de données totalement décentralisée. Nous ne pouvons donc pas créer de serveur central permettant de gérer le système de noeuds et c'est la que réside la difficulté du projet. En effet, le réseau n'existe que grâce aux liens que les noeuds entretiennent avec leurs voisins respectifs. Le réseau n'est pas stocké dans une classe particulière et rien ne permet de le connaître globalement.

Le projet à donc une structure plutôt simple : un fichier *node.py* qui permet de définir les noeuds et leurs comportements, *message.py* qui constitue simplement la classe **Message** que les noeuds utilisent pour communiquer et *main.py* qui permet de lancer la simulation et tester les fonctionnalités du projet.



## Fonctionnalités et choix effectués

décrire les fonctionnalités (ordre noeuds dans la dht, fonction find triche etc.) et comment ca marche
justifier nos choix (timeouts par exemple, fait qu'on a pas sécurisé le réseau (on vérifie pas avant d'ajouter un noeud qu'il n'appartient pas deja a la dht))


### Logger
expliquer ici que les logs on été super important pour comprendre comment fonctionne la la simulation et que c'est ce qui nous a permis de corriger nos erreurs 


## Difficultés et bugs



## Documentation

Voici une explication exhaustive du role des méthodes du code.

- ***init()*** : initialise un noeud avec un identifiant, une référence à son environnement de simulation (env), un canal de communication (pipe) pour envoyer et recevoir des messages, et une liste vide de messages. À sa création, un noeud est son propre voisin suivant et précédent en attendant qu'il rejoigne la DHT.

- ***set_next()*** : permet de définir le noeud suivant dans la DHT.
- ***set_prev()*** : permet de définir le noeud précédent dans la DHT.

- ***join()*** : est appelée lorsqu'un nouveau noeud souhaite rejoindre la DHT. Elle recherche d'abord le noeud de contact dans la DHT avec ***find()*** avant de lui envoyer un message d'insertion.

- ***find()*** : est utilisée pour rechercher le contact d'un nouveau noeud dans la DHT en faisant en sorte que la DHT soit un cycle de noeuds classé par ordre croissant.

- ***insert()*** : permet d'insérer un nouveau noeud dans la DHT en utilisant les références de noeuds voisins pour mettre à jour la DHT.

- ***leave()*** : est appelée lorsqu'un noeud souhaite quitter la DHT. Elle envoie un message à chacun des voisin du noeud pour leur indiquer que celui-ci quitte la DHT. Elle utilise ensuite les setters pour supprimer les liens que le noeud avait avec ses voisins le faisant ainsi quitter la DHT.

- ***nodes_rearrangement()*** : est appelée lorsqu'un noeud reçoit un message de suppression. Elle met à jour les références de noeuds voisins pour supprimer le noeud de la DHT.

- ***message_generator()*** : est utilisée pour créer un message et l'envoyer à un autre nœud.

- ***send()*** : envoie un message à un autre nœud en utilisant le canal de communication et appelle la méthode ***receive()*** du destinataire.

- ***receive()*** : est appelée lorsqu'un noeud reçoit un message. Elle traite le message et le stocke dans la liste des messages du noeud.

- ***run()*** : est la méthode principale qui gère le comportement du noeud dans l'environnement de simulation. Elle vérifie régulièrement la liste des messages et traite chaque message en conséquence.
