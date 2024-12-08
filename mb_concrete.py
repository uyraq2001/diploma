from multiprocessing.dummy import current_process
import sys
# are we running inside Blender?
bpy = sys.modules.get("bpy")
if bpy is not None:
    sys.executable = bpy.app.binary_path_python
    # get the text-block's filepath
    __file__ = bpy.data.texts[__file__[1:]].filepath
del bpy, sys

import os

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
def run_thread(n, m, N, i, res):
    for j in range(N):
        my_bag(n, m)
    res[i] = 0
def run(n, m, N, treads):
    # print((n, m, N// treads))
    assert N % treads == 0
    global run_thread
    procs = []
    manager = multiprocessing.Manager()
    res = manager.dict()
    t1 = datetime.datetime.now()
    for i in range(treads):
        p = multiprocessing.Process(target=run_thread, args=(n, m, N//treads, i, res))
        procs.append(p)
        p.start()
    for proc in procs:
        proc.join()
    t2 = datetime.datetime.now()
    k = datetime.timedelta() + (t2 - t1)
    return k / N
if __name__ == "__main__":
    for i1 in [1, 2, 4, 8]:
        print('\n'+str(i1)+'treads:\nn\\m  |      1\t|\t3\t|\t5', end ='')
        for i2 in [100, 1000, 10000]:
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
                print 
                print(run(round(i2//1), i3, 8, i1), end='|')