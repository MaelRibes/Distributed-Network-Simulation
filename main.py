import random
import simpy

import networkx as nx
from node import Node
import matplotlib.pyplot as plt

G = nx.DiGraph()
env = simpy.Environment()
pipe = simpy.Store(env)
id_init = [100, 500, 750]
nodes = [Node(env, pipe, id_init[i]) for i in range(3)]  # TO FIX FOR n NODES

nodes[0].set_next(nodes[1])
nodes[1].set_next(nodes[2])
nodes[2].set_next(nodes[0])

nodes[0].set_prev(nodes[2])
nodes[2].set_prev(nodes[1])
nodes[1].set_prev(nodes[0])

print('BASE :', nodes[0].id, nodes[1].id, nodes[2].id)

for i in range(1, 10):
    id = random.randint(1, 1000)
    node = Node(env, pipe, id)
    node.join(nodes)
    nodes.append(node)
    env.run(until=20*i)


"""
for node in nodes:
    print("----------")
    print(node.id)
    print("Prev. :", node.prev.id)
    print("Next. :", node.next.id)
    print("----------")
"""


for i in range(len(nodes) - 1):
    G.add_node(nodes[i].id)
    G.add_edge(nodes[i].prev.id, nodes[i].id)
    G.add_edge(nodes[i].id, nodes[i].next.id)
nx.draw(G, with_labels=True)
plt.show()
