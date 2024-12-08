import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import math
import pylab

k = 100000
l = 100
x = []
c = []
for i in range(k):
    c.append(0)
    x.append(i)
for i in range(10):
    bag = nx.barabasi_albert_graph(n = k, m = l)
    for i in bag.adjacency():
        c[len(i[1])]+=1
print(c)
for i in range(k):
    c[i]/=10

#pylab.plot (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
#pylab.semilogx (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
pylab.loglog (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
pylab.show()