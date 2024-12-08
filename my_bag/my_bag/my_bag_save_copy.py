import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import math
import numpy.random
import random
import pylab

def my_bag(n, m):
    G = nx.complete_graph(m)
    for i in range(m, n):
        G.add_node(i)
    nodeCount = m
    o = True
    nodes = []
    degrees = []
    used = []
    for j in range(n):
        used.append(False)
    for i in range(m):
        nodes.append(i)
        degrees.append(m)
    for i in range(m, n):
        if not o :
            conections = []
            j = 0
            while j < m:
                choice = random.choices(nodes, weights = degrees, k = 1)
                choosen = choice[0]
                if not used[choosen]:
                    G.add_edge(i, choosen)
                    j += 1
                    conections.append(choosen)
                    used[choosen] = True
            for j in range(m):
                used[conections[j]] = False
                degrees[conections[j] - 1] += 1
        else:
            G.add_edge(0, 1)
            o = False
        nodeCount += 1
        nodes.append(nodeCount)
        degrees.append(m)
    return G

#G = my_bag(50, 1)



#pos = nx.spring_layout(G)
#nx.draw(G, pos)
#node_labels = nx.get_node_attributes(G,'state')
#nx.draw_networkx_labels(G, pos, labels = node_labels)
#plt.savefig('this.png')
#plt.show()



k = 100000
l = 5
x = []
c = []
for i in range(k):
    c.append(0)
    x.append(i)
for i in range(10):
    bag = my_bag(n = k, m = l)
    for i in bag.adjacency():
        c[len(i[1])]+=1
    print(i)
for i in range(k):
    c[i]/=10


#pylab.plot (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
#pylab.semilogx (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
pylab.loglog (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
plt.savefig('this.png')
pylab.show()