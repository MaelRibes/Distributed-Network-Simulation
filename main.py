########## IMPORTATION DES LIBRAIRIES ##########

import random
import simpy
import networkx as nx
from node import Node
import matplotlib.pyplot as plt

########## MISE EN PLACE DU SYSTEME ##########

G = nx.DiGraph()
env = simpy.Environment()
pipe = simpy.Store(env)
id_init = [250, 500, 750]
nodes = [Node(env, pipe, id_init[i]) for i in range(3)]

nodes[0].set_next(nodes[1])
nodes[1].set_next(nodes[2])
nodes[2].set_next(nodes[0])

nodes[0].set_prev(nodes[2])
nodes[2].set_prev(nodes[1])
nodes[1].set_prev(nodes[0])

print('BASE :', nodes[0].id, nodes[1].id, nodes[2].id)

########## AJOUT DE NOEUDS ##########

for i in range(1, 10):
    id = random.randint(1, 1000)
    node = Node(env, pipe, id)
    node.join(nodes)
    nodes.append(node)
    env.run(until=env.now + 10)

########## RETRAIT D'UN NOEUD ##########
nodes[0].leave()
env.run(until=env.now + 10)

########## AJOUT DE DONNEES ##########

nodes[0].put(("Seb", "seb.c"), nodes)
env.run(until=env.now + 20)

nodes[0].put(("Kavé", "kave.mp4"), nodes)
env.run(until=env.now + 20)

nodes[0].put(("Flav", "flav.sql"), nodes)
env.run(until=env.now + 20)

nodes[0].put(("Sorana", "soso.java"), nodes)
env.run(until=env.now + 20)

########## RECUPERATION D'UNE DONNEE ##########

nodes[5].get("Kavé", nodes)
env.run(until=env.now + 20)

########## AFFICHAGE DES TABLES DE HACHAGE ##########

for node in nodes:
    print(node.id, " : ", node.hashtable)

########## NETWORKX ##########

for i in range(len(nodes) - 1):
    G.add_node(nodes[i].id)
    G.add_edge(nodes[i].prev.id, nodes[i].id)
    G.add_edge(nodes[i].id, nodes[i].next.id)
nx.draw(G, with_labels=True)
plt.show()
