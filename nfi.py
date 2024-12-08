from diploma import d, neibours, index, my_bag, run, s, beta
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def mfi1 (degrees, neibours):
    L = sum(degrees)
    sumLTD = []                         # sum of degrees Less Then Degree
    for (dgr, nbrs) in zip(degrees, neibours):
        sumLTD.append(sum([degrees[nbr] if degrees[nbr] <= dgr else 0 for nbr in nbrs]))
    return [bi * LTD / L for (bi, LTD) in zip(beta(degrees, neibours), sumLTD)]

def mfi2 (degrees, neibours):
    sumLTD = []                         # sum of degrees Less Then Degree
    for (dgr, nbrs) in zip(degrees, neibours):
        sumLTD.append(sum([degrees[nbr] if degrees[nbr] <= dgr else 0 for nbr in nbrs]))
    ans = []
    for (bi, LTD, nbrs) in zip(beta(degrees, neibours), sumLTD, neibours):
        L = sum(degrees[nbr] for nbr in nbrs)
        ans.append(bi * LTD / L)
    return ans

if __name__ == "__main__":
    n = 10000
    m = 5
    p = 0.25
    graphCount = 10
    histBins = 50
    steps = [n // 3, 2 * n // 3, n]

    fig = plt.figure()
    gs = fig.add_gridspec(3, 2, hspace=0, wspace=0)
    ax1, ax2, ax3 = gs.subplots()
    graphs = run(graphCount, 6, my_bag, n, [m, p], [beta, mfi1, mfi2], [n // 3, n // 3, n // 3])
    
    ax1[0].set_title("BAG")
    ax1[1].set_title("BAG and configuration")
    
    ax1[0].set_ylabel("FI")
    for i in range(len(graphs[0][0])):
        meanCount = np.zeros(shape = histBins)
        meanBeta = np.zeros(shape = histBins + 1)
        for graph in graphs:
            hist = np.histogram(graph[0][i], bins=histBins)
            meanCount += hist[0]
            meanBeta += hist[1]
        meanCount /= graphCount
        meanBeta /= graphCount
        ax1[0].plot(meanBeta[:-1], meanCount)
    ax1[1].plot(meanBeta[:-1], meanCount)
    
    ax2[0].set_ylabel("MFI_1")
    for i in range(len(graphs[1][0])):
        meanCount = np.zeros(shape = histBins)
        meanMFI = np.zeros(shape = histBins + 1)
        for graph in graphs:
            hist = np.histogram(graph[1][i], bins=histBins)
            meanCount += hist[0]
            meanMFI += hist[1]
        meanCount /= graphCount
        meanMFI /= graphCount
        ax2[0].plot(meanMFI[:-1], meanCount)
    ax2[1].plot(meanMFI[:-1], meanCount)
    
    ax3[0].set_ylabel("MFI_2")
    for i in range(len(graphs[2][0])):
        meanCount = np.zeros(shape = histBins)
        meanMFI = np.zeros(shape = histBins + 1)
        for graph in graphs:
            hist = np.histogram(graph[2][i], bins=histBins)
            meanCount += hist[0]
            meanMFI += hist[1]
        meanCount /= graphCount
        meanMFI /= graphCount
        ax3[0].plot(meanMFI[:-1], meanCount)
    ax3[1].plot(meanMFI[:-1], meanCount)
    
    meanBetaCount = np.zeros(shape = histBins)
    meanMFI1Count = np.zeros(shape = histBins)
    meanMFI2Count = np.zeros(shape = histBins)
    meanBeta = np.zeros(shape = histBins + 1)
    meanMFI1 = np.zeros(shape = histBins + 1)
    meanMFI2 = np.zeros(shape = histBins + 1)
    for _ in range(graphCount):
        sequence = list(np.rint((np.random.pareto(2.5, n) + 1)))
        if not(nx.algorithms.is_multigraphical(sequence)):
            sequence[0] += 1
        M = nx.configuration_model(sequence)
        G = nx.Graph()
        for u,v in M.edges():
            if not(G.has_edge(u,v)):
                G.add_edge(u, v)
        betaData = np.histogram(beta(list(list(zip(*G.degree))[1]), [list(nbrs.keys()) for _, nbrs in G.adjacency()]), bins=histBins)
        meanBetaCount += betaData[0]
        meanBeta += betaData[1]
        mfi1Data = np.histogram(mfi1(list(list(zip(*G.degree))[1]), [list(nbrs.keys()) for _, nbrs in G.adjacency()]), bins=histBins)
        meanMFI1Count += mfi1Data[0]
        meanMFI1 += mfi1Data[1]
        mfi2Data = np.histogram(mfi2(list(list(zip(*G.degree))[1]), [list(nbrs.keys()) for _, nbrs in G.adjacency()]), bins=histBins)
        meanMFI2Count += mfi2Data[0]
        meanMFI2 += mfi2Data[1]
    meanBetaCount /= graphCount
    meanBeta /= graphCount
    ax1[1].plot(meanBeta[:-1], meanBetaCount)
    meanMFI1Count /= graphCount
    meanMFI1 /= graphCount
    ax2[1].plot(meanMFI1[:-1], meanMFI1Count)
    meanMFI2Count /= graphCount
    meanMFI2 /= graphCount
    ax3[1].plot(meanMFI2[:-1], meanMFI2Count)

    plt.show()