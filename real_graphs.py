import igraph
import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing  
import math
import datetime
import json
def f(x, a, b):
    return pow(x * b, a)

def dynamics(name):
    file = open('C:\\Users\\YURA\\source\\repos\\CSW\\real_graphs\\' + name + '.txt', 'r')
    edge_list = []
    while True:
        line = file.readline()
        edge_list.append(line.split(" "))
        if not line:
            break
    edge_list.pop()
    edge_list = [[int(j) for j in i] for i in edge_list]
    # edge_list = [[i[0], 
    #               i[1], 
    #               datetime.datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S').timestamp()] 
    #              for i in edge_list]
    file.close()
    edge_list.sort(key = lambda i: i[2])
    step = 1000
    base = edge_list[0][2]
    res = []
    degrees = {}
    neibours_degrees = {}
    neibours = {}
    Ls = {}
    LTDSums = {}
    cnt = 0
    for i in edge_list:
        cnt += 1
        if not i[0] in degrees:
            degrees[i[0]] = 0
            neibours[i[0]] = set()
            neibours_degrees[i[0]] = 0
            LTDSums[i[0]] = 0
        if not i[1] in degrees:
            degrees[i[1]] = 0
            neibours[i[1]] = set()
            neibours_degrees[i[1]] = 0
            LTDSums[i[1]] = 0
        if i[0] == i[1]:
            degrees[i[0]] += 1
            neibours_degrees[i[0]] += degrees[i[0]]
            for j in neibours[i[0]]:
                neibours_degrees[j] += 1
            neibours[i[0]].add(i[0])
        else:
            degrees[i[0]] += 1
            degrees[i[1]] += 1
            if not i[1] in neibours[i[0]] and not i[0] in neibours[i[1]]:
                neibours_degrees[i[0]] += degrees[i[1]]
                neibours_degrees[i[1]] += degrees[i[0]]
            for j in neibours[i[0]]:
                neibours_degrees[j] += 1
                LTDSums[j] += 1
            for j in neibours[i[1]]:
                neibours_degrees[j] += 1
                LTDSums[j] += 1
            neibours[i[0]].add(i[1])
            neibours[i[1]].add(i[0])
            if (degrees[i[0]] >= degrees[i[1]]):
                LTDSums[i[0]] += degrees[i[1]]
            else:
                LTDSums[i[0]] -= degrees[i[1]]
            if (degrees[i[1]] >= degrees[i[0]]):
                LTDSums[i[1]] += degrees[i[0]]
            else:
                LTDSums[i[1]] -= degrees[i[0]]
        if (i[2] - base) >= step:
            base = step * math.ceil(i[2] / step)
            ans = []
            for j in degrees.keys():
                ans.append(neibours_degrees[j] / degrees[j] / degrees[j] * LTDSums[j] / neibours_degrees[j])
            res.append(np.mean(ans))
        # if cnt % step == 0:
        #     ans = []
        #     for j in degrees.keys():
        #         ans.append(neibours_degrees[j] / degrees[j] / degrees[j])
        #     res.append(np.mean(ans))
    with open('C:\\Users\\YURA\\source\\repos\\CSW\\util_storage\\' + name + '_mean_mfi.json', 'w') as f:
        json.dump(res, f)
        f.close()
    y = res
    plt.xscale("log")
    plt.yscale("log")
    # plt.ylim([0, 100])
    plt.plot(y)
    # line = [f(i, 2, 2.1) for i in range(1, 100000)]
    # plt.plot(line, color = 'red')
    # plt.legend(['friendship index distribution', 'y = (x*1)^0.45'])
    plt.show()
    plt.clf()
    
    
def run_thread(namegroup, i, res):
    ans = []
    for j in namegroup:
        ans.append(dynamics(j))
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
    # run([['sx-askubuntu'], ['sx-askubuntu-a2q'], ['sx-askubuntu-c2a', 'sx-askubuntu-c2q'],
    #      ['sx-superuser'], ['sx-superuser-a2q'], ['sx-superuser-c2a', 'sx-superuser-c2q']])
    # dynamics('sx-mathoverflow-c2q')
    # dynamics('sx-mathoverflow-a2q')
    # dynamics('sx-mathoverflow-c2a')
    # dynamics('sx-mathoverflow')
    dynamics('CollegeMsg')
        