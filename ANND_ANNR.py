from diploma import d, neibours, index, my_bag, run, s
import matplotlib.pyplot as plt
import math
import networkx as nx
import numpy as np

n = 100000
graphCount = 30

def measure_kvise (degrees, neibours, f):
    byDegree = {}
    for i in range(len(degrees)) :
        if degrees[i] in byDegree:
            byDegree[degrees[i]].append(i)
        else: 
            byDegree[degrees[i]] = [i]
        
    ans = {}
    for (k, vertexes) in byDegree.items():
        ans[k] = (f(degrees, neibours, vertexes, k))
    return ans

def ANND_helper (degrees, neibours, vertexes, k):
    if len(vertexes) == 0:
        return 0
    
    L = sum(degrees)
    f = len(vertexes) / len(degrees)
    fs = len(degrees) * k * f / L
    
    h = {}
    for v in vertexes:
        for nbr in neibours[v]:
            if degrees[nbr] in h:
                h[degrees[nbr]] += 1
            else:
                h[degrees[nbr]] = 1
    if k in h:
        h[k] -= len(vertexes)  # to fix dublicating edges 
    sumhl = 0
    for (key, val) in h.items():
        sumhl += key * val / L

    return sumhl / fs

def ANND(degrees, neibours): return measure_kvise(degrees, neibours, ANND_helper)

def ANND2_helper (degrees, neibours, vertexes, k):
    S = s(degrees, neibours)
    sum = 0
    for v in vertexes:
        sum += S[v]
    return sum / len(vertexes)

def ANND2(degrees, neibours): return measure_kvise(degrees, neibours, ANND2_helper)

def ANNR_helper (degrees, neibours, vertexes, k):
    if len(vertexes) == 0:
        return 0
    
    L = sum(degrees)
    f = len(vertexes) / len(degrees)
    fs = len(degrees) * k * f / L
    
    h = {}
    for v in vertexes:
        for nbr in neibours[v]:
            if degrees[nbr] in h:
                h[degrees[nbr]] += 1
            else:
                h[degrees[nbr]] = 1
    if k in h:
        h[k] -= len(vertexes)  # to fix dublicating edges 
    sumhFs = 0
    for (key, val) in h.items():
        sumD = 0
        for d in degrees:
            if d <= key:
                sumD += d
        sumFs = sumD / L
        sumhFs += sumFs * val / L
    
    res = sumhFs / fs
    
    return res

def ANNR(degrees, neibours): return measure_kvise(degrees, neibours, ANNR_helper)

def AFR_helper (degrees, neibours, vertexes, k):
    return ANNR_helper(degrees, neibours, vertexes, k) / k
def AFR(degrees, neibours): return measure_kvise(degrees, neibours, AFR_helper)

if __name__ == '__main__':
    # for m in [3, 5]:
        # for p in [0.25, 0.5, 0.75]:
    m = 3
    p = 0.25
    
    fig = plt.figure()
    gs = fig.add_gridspec(2, 2, hspace=0, wspace=0)
    ax1, ax2= gs.subplots(sharex='col', sharey='row')
    graphs = run(graphCount, 6, my_bag, n, [m, p], [ANND, ANNR, AFR], [n // 3, n // 3, n // 3])
    
    ax1[0].set_title("BAG")
    ax1[0].set_ylabel("ANND")
    mean = [{} for _ in graphs[0][0]]
    count = [{} for _ in graphs[0][0]]
    for graph in graphs[1:]:
        for (step, curMean, curCount) in zip(graph[0], mean, count):
            for k in step.keys():
                if not k in curMean.keys():
                    curMean[k] = 0 
                    curCount[k] = 0 
                curMean[k] += step[k]
                curCount[k] += 1
    for (curMean, curCount) in zip(mean, count):
        for k in curMean.keys():
            curMean[k] /= curCount[k]
    for curMean in mean:
        lst = sorted(curMean.items())
        x, y = zip(*lst)
        ax1[0].plot(x, y)
        
    ax2[0].set_ylabel("ANNR")
    mean = [{} for _ in graphs[0][1]]
    count = [{} for _ in graphs[0][1]]
    for graph in graphs[1:]:
        for (step, curMean, curCount) in zip(graph[1], mean, count):
            for k in step.keys():
                if not k in curMean.keys():
                    curMean[k] = 0 
                    curCount[k] = 0 
                curMean[k] += step[k]
                curCount[k] += 1
    for (curMean, curCount) in zip(mean, count):
        for k in curMean.keys():
            curMean[k] /= curCount[k]
    for curMean in mean:
        lst = sorted(curMean.items())
        x, y = zip(*lst)
        ax2[0].plot(x, y)
  
    # ax3[0].set_ylabel("AFR")
    # mean = [{} for _ in graphs[0][2]]
    # count = [{} for _ in graphs[0][2]]
    # for graph in graphs[1:]:
    #     for (step, curMean, curCount) in zip(graph[2], mean, count):
    #         for k in step.keys():
    #             if not k in curMean.keys():
    #                 curMean[k] = 0 
    #                 curCount[k] = 0 
    #             curMean[k] += step[k]
    #             curCount[k] += 1
    # for (curMean, curCount) in zip(mean, count):
    #     for k in curMean.keys():
    #         curMean[k] /= curCount[k]
    # for curMean in mean:
    #     lst = sorted(curMean.items())
    #     x, y = zip(*lst)
    #     ax3[0].plot(x, y)
  
  
    
    steps = [int(n / 3), int(2 * n / 3), n]
    for step in steps:
        meanANND = {}
        meanANNR = {}
        meanAFR = {}
        countANND = {}
        countANNR = {}
        countAFR = {}
        for _ in range(graphCount):
            sequence = list(np.rint((np.random.pareto(2.5, n) + 1)))
            if not(nx.algorithms.is_multigraphical(sequence)):
                sequence[0] += 1
            M = nx.configuration_model(sequence)
            G = nx.Graph()
            for u,v in M.edges():
                if not(G.has_edge(u,v)):
                    G.add_edge(u, v)
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
            afr = AFR(list(list(zip(*G.degree))[1]), [list(nbrs.keys()) for _, nbrs in G.adjacency()])
            for k in afr.keys():
                if not k in meanAFR.keys():
                    meanAFR[k] = 0 
                    countAFR[k] = 0 
                meanAFR[k] += afr[k]
                countAFR[k] += 1
                 
        for i in meanANND.keys():
            meanANND[i] /= countANND[i]
        for i in meanANNR.keys():
            meanANNR[i] /= countANNR[i]
        for i in meanAFR.keys():
            meanAFR[i] /= countAFR[i]
        # print(meanANND)
        # print(meanANNR)
        
        ax1[1].set_title("configuration")
        # ax1[1].set_ylabel("ANND")
        x, y = zip(*sorted(meanANND.items()))
        ax1[1].plot(x, y)
        # ax2[1].set_title("ANNR")
        x, y = zip(*sorted(meanANNR.items()))
        ax2[1].plot(x, y)
        # x, y = zip(*sorted(meanAFR.items()))
        # ax3[1].plot(x, y)
                
    
    plt.show()