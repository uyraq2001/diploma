import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import math
import random
import pylab
import multiprocessing  

def my_bag(n, m):
    G = nx.MultiGraph();
    for i in range(m):
        G.add_node(i);
    for i in G.nodes():
        G.nodes[i]['state'] = i
        #G.nodes[i]['refs'] = 1
    for i in range(m - 1):
        G.add_edge(i, i + 1);
    G.add_edge(m - 1, 0)
    for i in range(n-m):
        G.add_node(m + i)
    for i in range(n-m):
        G.nodes[m + i]['state'] = m + i
        #G.nodes[m + i]['refs'] = 0
    node_count = m
    for i in range(n-m): 
        node_count += 1    
        for j in range(node_count):
            #p = G.nodes[j]['refs'] / len(G.edges)
            p = len(G.nodes[j]) / len(G.edges)
            if random.random() < p:
                G.add_edge(m + i, j)
                #G.nodes[j]['refs'] += 1
            #else:
                #print(i,' ',j,' ',p,'\n')
    return G

#G = my_bag(150, 1)



#pos = nx.spring_layout(G)
#nx.draw(G, pos)
#node_labels = nx.get_node_attributes(G,'state')
#nx.draw_networkx_labels(G, pos, labels = node_labels)
#plt.savefig('this.png')
#plt.show()


if __name__=='__main__':
    k = 100
    l = 5
    x = []
    c = []
    for i in range(k):
        c.append(0)
        x.append(i)
    pool = multiprocessing.Pool(processes=8)
    for i in range(10):
        bag = pool.apply_async(my_bag(n = k, m = l))
        for i in bag.get.adjacency():
            c[len(i[1])]+=1
    print(c)
    for i in range(k):
        c[i]/=10


    #pylab.plot (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
    #pylab.semilogx (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
    pylab.loglog (x, c, color='red', marker='.', linestyle='-', linewidth=0.05, markersize=0.5)
    plt.savefig('this.png')
    pylab.show()