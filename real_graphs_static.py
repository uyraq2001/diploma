import igraph
import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing 
import math

def f(x, a, b):
    return pow(x * b, a)

def static(name):
    file = open('C:\\Users\\YURA\\source\\repos\\CSW\\real_graphs\\' + name + '.txt', 'r')
    res = []
    degrees = {}
    while True:
        line = file.readline()
        if not line:
            break
        edge = [int(j) for j in line.split(" ")]
        if not edge[0] in degrees:
            degrees[edge[0]] = 0
        degrees[edge[0]] += 1
        if not edge[1] in degrees:
            degrees[edge[1]] = 0
        degrees[edge[1]] += 1
    file.seek(0)
    sums = {}
    while True:
        line = file.readline()
        if not line:
            break
        edge = [int(j) for j in line.split(" ")]
        if not edge[0] in sums:
            sums[edge[0]] = 0
        sums[edge[0]] += degrees[edge[1]]
        if not edge[1] in sums:
            sums[edge[1]] = 0
        sums[edge[1]] += degrees[edge[0]]
    for i in degrees.keys():
        res.append(sums[i] / degrees[i] / degrees[i])
    
    file.close()
        
    bincnt = 1000
    ans = np.histogram(res, bincnt)
    x = ans[1]
    y = ans[0]
    x = np.resize(x, x.size - 1)
    plt.xscale("log")
    plt.yscale("log")
    plt.scatter(x, y, marker='.')
    a = -1.3
    b = 0.00006 
    xl = list(range(0, 10000))
    xl[0] = 0.1
    line = [f(i, a, b) for i in xl]
    plt.plot(xl, line, color = 'red')
    plt.legend(['friendship index ditribution', 'y = (x*' + str(b) + ')^' + str(a) + ''])
    # plt.bar(x[0:int(bincnt / 100 * 2)], y[0:int(bincnt / 100 * 2)])
    # plt.bar(x[0:int(bincnt / 1000 * 2)], y[0:int(bincnt / 1000 * 2)])
    plt.savefig("C:\\Users\\YURA\\source\\repos\\CSW\\diploma_results\\static_real_log\\" + name + ".png")
    plt.show()
    plt.clf()
    
    
def run_thread(namegroup, i, res):
    ans = []
    for j in namegroup:
        ans.append(static(j))
    res[i] = ans
def run(names):
    procs = []
    manager = multiprocessing.Manager()
    res = manager.dict()
    for (i, namegroup) in enumerate(names):
        p = multiprocessing.Process(target=run_thread, args=(namegroup, i, res))
        procs.append(p)
        p.start()
    for proc in procs:
        proc.join()
    ans = []
    for i in res.values():
        ans += i
    return ans
    
if __name__ == "__main__":
    static('twitter_combined')