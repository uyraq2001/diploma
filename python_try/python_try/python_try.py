import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import math
    
g = nx.gnm_random_graph(10, 6, directed=True)
k = 0
for i in g.nodes:
    g.nodes[i]['weight'] = k
    k+=1
    i+=1
nx.draw(g)
nx.drawing.nx_pylab.draw_networkx_labels(g, pos=nx.spring_layout(g))
nx.draw_networkx_edge_labels(g, pos=nx.spring_layout(g))
plt.show()