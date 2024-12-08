import igraph
import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing 
import math
import datetime

def f(x, a, b):
    return pow(x * b, a)

# directory = os.fsencode("C:\\Users\\YURA\\source\\repos\\CSW\\real_graphs\\as-733-no-comments")

# mean_beta = []
# sizes = []

# k = 0
# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     graph = igraph.Graph.Read("C:\\Users\\YURA\\source\\repos\\CSW\\real_graphs\\as-733-no-comments" + "\\" + filename,
#                               format= "edgelist")
#     degrees = np.array([i.degree() for i in graph.vs])
#     sums = np.array([sum([j.degree() for j in i.neighbors()]) for i in graph.vs])
#     degrees = degrees[degrees != 0]
#     sums = sums[sums != 0]
#     res = np.mean((sums / degrees) / degrees)
#     mean_beta.append(res)
#     sizes.append(graph.vcount())
#     k+= 1
#     if k == 500:break
    
# plt.scatter(sizes, mean_beta)
# plt.savefig("C:\\Users\\YURA\\source\\repos\\CSW\\diploma_results\\as_dynamics.jpg")
# plt.clf()

def dynamics(name):
    file = open('C:\\Users\\YURA\\source\\repos\\CSW\\real_graphs\\' + name + '.txt', 'r')
    time_file = open('C:\\Users\\YURA\\source\\repos\\CSW\\real_graphs\\' + name + '-dates.txt', 'r')
    times = {}
    while True:
        line = time_file.readline()
        if not line:
            break
        line = line.split("\t")
        line = [int(line[0]), int(line[1].replace('-', ''))]
        times[line[0]] = line[1]
    edge_list = []
    while True:
        line = file.readline()
        edge_list.append(line.split("\t"))
        if not line:
            break
    edge_list.pop()
    edge_list = [[int(j) for j in i] for i in edge_list]
    file.close()
    time_file.close()
    edge_list.sort(key = lambda i: times[i[0]] if i[0] in times else 100000000)
    step = 1000
    # base = edge_list[0][2]
    res = []
    degrees = {}
    neibours_degrees = {}
    neibours = {}
    cnt = 0
    for i in edge_list:
        cnt += 1
        if not i[0] in degrees:
            degrees[i[0]] = 0
            neibours[i[0]] = set()
            neibours_degrees[i[0]] = 0
        if not i[1] in degrees:
            degrees[i[1]] = 0
            neibours[i[1]] = set()
            neibours_degrees[i[1]] = 0
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
            for j in neibours[i[1]]:
                neibours_degrees[j] += 1
            neibours[i[0]].add(i[1])
            neibours[i[1]].add(i[0])
        # if (i[2] - base) >= step:
        #     base = step * math.ceil(i[2] / step)
        #     ans = []
        #     for j in degrees.keys():
        #         ans.append(neibours_degrees[j] / degrees[j] / degrees[j])
        #     res.append(np.mean(ans))
        if cnt % step == 0:
            ans = []
            for j in degrees.keys():
                ans.append(neibours_degrees[j] / degrees[j] / degrees[j])
            res.append(np.mean(ans))
    plt.xscale('log')
    plt.yscale('log')
    plt.plot(res)
    a = 0.12
    b = 11000
    x = range(1, 1000)
    line = [f(i, a, b) for i in x]
    plt.plot(x, line, color = 'red')
    plt.legend(['mean friendship index', 'y = (x*' + str(b) + ')^' + str(a) + ''])
    # plt.savefig("C:\\Users\\YURA\\source\\repos\\CSW\\diploma_results\\" + name + "_iterational_dynamics.jpg")
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
    # run([['askubuntu', 'askubuntu-a2q'], ['askubuntu-c2a', 'askubuntu-c2q'], ['mathoverflow', 'mathoverflow-a2q'], 
    #      ['mathoverflow-c2a', 'mathoverflow-c2q'], ['superuser', 'superuser-a2q'], ['superuser-c2a', 'superuser-c2q']])
    dynamics('cit-HepPh')