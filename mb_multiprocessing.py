import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import math
import random
import pylab
import multiprocessing
import datetime

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


if __name__ == "__main__":
    for i1 in [1, 2, 4, 6, 8, 10, 16]:
        print(str(i1)+' treads:\nn\\m  |  \t1\t|\t3\t|\t5', end ='')
        for i2 in [10000, 20000, 30000, 40000, 50000]:
            print('\n' + str(i2), end='|')
            for i3 in [1, 3, 5]:
                k = i2
                l = i3
                x = []
                c = []
                o = []
                count = 24
                for i in range(k):
                    c.append(0)
                    x.append(i)
                for i in range(count):
                    o.append((k, l))
                pool = multiprocessing.Pool(i1)
                t1 = datetime.datetime.now()
                bagRes = pool.starmap(my_bag_poisson, o)
                for i in bagRes:
                    for j in i.adjacency():
                        c[len(j[1])]+=1
                t2 = datetime.datetime.now()
                print(t2 - t1, end='|')