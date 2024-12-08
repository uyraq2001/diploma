from multiprocessing.dummy import current_process
from statistics import mean

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
import numpy as np
import random
import pylab
def my_bag_poisson(n, m):
    m0 = np.random.poisson(m)
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
    mi = np.random.poisson(m0, n)
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
    # print(n + m)
    G = nx.complete_graph(m)
    for i in range(m, n):
        G.add_node(i)
    nodeCount = m
    o = False
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

def run_thread(n, m, N, i, res, args, f):
    ans = []
    for j in range(N):
        G = my_bag(n, m)
        ans.append(np.apply_along_axis(lambda x: f(G, x[0]), 0,[args]).tolist())
    res[i] = ans
def run(n, m, N, treads, args, f):
    assert N % treads == 0
    global run_thread
    procs = []
    manager = multiprocessing.Manager()
    res = manager.dict()
    for i in range(treads):
        p = multiprocessing.Process(target=run_thread, args=(n, m, math.ceil(N/treads), i, res, args, f))
        procs.append(p)
        p.start()
    for proc in procs:
        proc.join()
    ans = []
    for i in res.values():
        ans += i
    return ans
def d (G, i):
    return dict(G.degree)[i]
def s (G, i):
    ans = 0
    for j in G.neighbors(i):
        ans += dict(G.degree)[j]
    return ans
def alfa (G, i):
    return s(G, i) / d(G, i)
def beta (G, i):
    return alfa(G, i) / d(G, i)
if __name__ == "__main__":
    k = 1000
    l = 5
    
    ans = np.histogram(run(k, l, 6, 6, np.array(range(k//1)) * 1, beta), bins = 12)
    plt.bar(ans[1][:-1], ans[0] / 6)
    plt.show()