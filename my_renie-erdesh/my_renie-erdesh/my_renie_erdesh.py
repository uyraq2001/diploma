import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import math
import random
    
g = nx.DiGraph()
n = 10
p = 0.01
for i in range(n):
    g.add_node(nx.path_graph(n))
for i in g.nodes:
    for j in g.nodes:
        if i!=j and random.random()<p:
            g.add_edge(i, j)
nx.draw(g)
plt.show()