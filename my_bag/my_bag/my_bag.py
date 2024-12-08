import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import math
import numpy.random
import random
import pylab

def my_bag_poisson(n, m):
    m0 = numpy.random.poisson(m)
    G = nx.complete_graph(m0)
    for i in range(m0, n):
        G.add_node(i)
    nodeCount = m0
    o = True
    nodes = []
    degrees = []
    used = []
    for j in range(n):
        used.append(False)
    for i in range(m0):
        nodes.append(i)
        degrees.append(m0)
    mi = numpy.random.poisson(m0, n)
    for i in range(m0, n):
        if not o :
            conections = []
            j = 0
            while j < min(mi[i], nodeCount):
                choice = random.choices(nodes, weights = degrees, k = 1)
                choosen = choice[0]
                if not used[choosen]:
                    G.add_edge(i, choosen)
                    j += 1
                    conections.append(choosen)
                    used[choosen] = True
            for j in range(min(mi[i], nodeCount)):
                used[conections[j]] = False
                degrees[conections[j] - 1] += 1
        else:
            G.add_edge(0, 1)
            o = False
        nodeCount += 1
        nodes.append(nodeCount)
        degrees.append(m)
    return G


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



b = input("n:")
k = int(b)
p = input("m:")
l = int(p)
x = []
c = []
for i in range(k):
    c.append(0)
    x.append(i)
for i in range(10):
    bag = my_bag_poisson(n = k, m = l)
    for i in bag.adjacency():
        c[len(i[1])]+=1
    print(i)
for i in range(k):
    c[i]/=10


#pylab.plot (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
#pylab.semilogx (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
fname = "E:\\CSW\\my_bag\\my_bag\\data_s_" + str(l) + ".txt"

f = open(fname, "w")
for i in c:
    f.write(str(i));
    f.write("\n");
pylab.loglog (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
plt.savefig('plot_poison_' + str(l) + '.png')
pylab.show()