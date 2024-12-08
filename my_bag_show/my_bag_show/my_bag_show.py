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


n = 10000;
p = n
m = [1, 2, 5, 7, 10]
print('static:')
for j in range(5):
    print(str(m[j])+ '):', end = '\t')
    x = []
    c = []
    for i in range(n):
        c.append(0)
        x.append(i)
    for i in range(10):
        print(str(i) + ',', end = ' ')
        bag = my_bag(n = p, m = m[j])
        for k in bag.adjacency():
            c[len(k[1])]+=1
    for i in range(n):
        c[i]/=10
    fname = "E:\\CSW\\results\\data_s_" + str(m[j]) + ".txt"
    f = open(fname, "w")
    f.write("x\ty\n")
    for i in range(n):
        f.write(str(i) + '\t' + str(c[i]) + '\n')
    pylab.loglog (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
    plt.savefig('E:\\CSW\\results\\plot_s_' + str(m[j]) + '.png')
    plt.clf()
    print('\n');

print('poisson:')
for j in range(5):
    print(str(m[j])+ '):', end = '\t')
    x = []
    c = []
    for i in range(n):
        c.append(0)
        x.append(i)
    for i in range(10):
        print(str(i) + ',', end = ' ')
        bag = my_bag_poisson(n = p, m = m[j])
        for k in bag.adjacency():
            c[len(k[1])]+=1
    for i in range(n):
        c[i]/=10
    fname = "E:\\CSW\\results\\data_p_" + str(m[j]) + ".txt"
    f = open(fname, "w")
    f.write("x\ty\n")
    for i in range(n):
        f.write(str(i) + '\t' + str(c[i]) + '\n')
    pylab.loglog (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
    plt.savefig('E:\\CSW\\results\\plot_p_' + str(m[j]) + '.png')
    plt.clf()
    print('\n');

