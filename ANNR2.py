import networkx as nx
import matplotlib.pyplot as plt
import math
from ANND_ANNR import ANND, ANNR

graphCount = 30
n = 10#0#00
steps = [int(n / 3), int(2 * n / 3), n]

fig, (ax1) = plt.subplots(2, 1)

for step in steps:
    sequence = nx.utils.powerlaw_sequence(n, 1.5)
    sequence = [math.ceil(i) for i in sequence]
    if sum(sequence) % 2 == 1:
            sequence[0] += 1
        
    meanANND = {}
    meanANNR = {}
    countANND = {}
    countANNR = {}
    for _ in range(graphCount - 1):
        G = nx.configuration_model(sequence)
        # print(list(list(zip(*G.degree))[1]))
        # print([list(nbrs.keys()) for _, nbrs in G.adjacency()])
        # print(ANNR(list(list(zip(*G.degree))[1]), [list(nbrs.keys()) for _, nbrs in G.adjacency()]))
        annr = ANNR(list(list(zip(*G.degree))[1]), [list(nbrs.keys()) for _, nbrs in G.adjacency()])
        for k in annr.keys():
            if not k in meanANNR.keys():
                meanANNR[k] = 0
                countANNR[k] = 0  
            meanANNR[k] += annr[k]
            countANNR[k] += 1
        annd = ANND(list(list(zip(*G.degree))[1]), [list(nbrs.keys()) for _, nbrs in G.adjacency()])
        for k in annd.keys():
            if not k in meanANND.keys():
                meanANND[k] = 0 
                countANND[k] = 0 
            meanANND[k] += annd[k]
            countANND[k] += 1
            
            
    for i in meanANND.keys():
        meanANND[i] /= countANND[i]
    for i in meanANNR.keys():
        meanANNR[i] /= countANNR[i]
    # print(meanANND)
    # print(meanANNR)
    
    ax1[0].set_title("ANND")
    x, y = zip(*sorted(meanANND.items()))
    ax1[0].plot(x, y)
    ax1[1].set_title("ANNR")
    x, y = zip(*sorted(meanANNR.items()))
    ax1[1].plot(x, y)

plt.show()