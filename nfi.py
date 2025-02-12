from diploma import d, neibours, index, my_bag, run, s, beta, mean_beta, my_triad
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from statistics import mean

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

def mean_mfi1 (degrees, neibours):
    return [mean(mfi1(degrees, neibours))]
    
def mean_mfi2 (degrees, neibours):
    return [mean(mfi2(degrees, neibours))]

if __name__ == "__main__":
    n = 10000
    m = 5
    p = 0.25
    graphCount = 10
    histBins = 50
    steps = [n // 3, 2 * n // 3, n]

    fig = plt.figure()
    gs = fig.add_gridspec(3, 1, hspace=0, wspace=0)
    ax1, ax2, ax3 = gs.subplots()
    bag_graphs = run(graphCount, 6, my_bag, n, [m, p], [mean_beta, mean_mfi1, mean_mfi2], [n // 1000, n // 1000, n // 1000])
    triad_graphs = run(graphCount, 6, my_triad, n, [m, p], [mean_beta, mean_mfi1, mean_mfi2], [n // 1000, n // 1000, n // 1000])
    
    ax1.set_title("BAG_loglog")
    
    ax1.set_ylabel("FI")
    mean_beta_data = np.array([i[0] for i in bag_graphs])
    mean_beta_data = np.apply_along_axis(arr=mean_beta_data, axis=2, func1d=lambda x: x[0])
    mean_beta_data = mean_beta_data.T
    mean_beta_data = np.apply_along_axis(arr=mean_beta_data, axis=1, func1d=mean)
    ax1.loglog(list(range(len(mean_beta_data) - 1)), mean_beta_data[:-1])
    
    ax2.set_ylabel("MFI_1")
    mean_mfi1_data = np.array([i[1] for i in bag_graphs])
    mean_mfi1_data = np.apply_along_axis(arr=mean_mfi1_data, axis=2, func1d=lambda x: x[0])
    mean_mfi1_data = mean_mfi1_data.T
    mean_mfi1_data = np.apply_along_axis(arr=mean_mfi1_data, axis=1, func1d=mean)
    ax2.loglog(list(range(len(mean_mfi1_data) - 1)), mean_mfi1_data[:-1])
    
    ax3.set_ylabel("MFI_2")
    mean_mfi2_data = np.array([i[2] for i in bag_graphs])
    mean_mfi2_data = np.apply_along_axis(arr=mean_mfi2_data, axis=2, func1d=lambda x: x[0])
    mean_mfi2_data = mean_mfi2_data.T
    mean_mfi2_data = np.apply_along_axis(arr=mean_mfi2_data, axis=1, func1d=mean)
    ax3.loglog(list(range(len(mean_mfi2_data) - 1)), mean_mfi2_data[:-1])
    
    plt.show()
    
    
    fig = plt.figure()
    gs = fig.add_gridspec(3, 1, hspace=0, wspace=0)
    ax1, ax2, ax3 = gs.subplots()
    
    ax1.set_title("BAG")
    
    ax1.set_ylabel("FI")
    ax1.plot(list(range(len(mean_beta_data) - 1)), mean_beta_data[:-1])
    
    ax2.set_ylabel("MFI_1")
    ax2.plot(list(range(len(mean_mfi1_data) - 1)), mean_mfi1_data[:-1])
    
    ax3.set_ylabel("MFI_2")
    ax3.plot(list(range(len(mean_mfi2_data) - 1)), mean_mfi2_data[:-1])

    plt.show()