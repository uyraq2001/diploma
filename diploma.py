from multiprocessing.dummy import current_process
from statistics import mean
from copy import deepcopy

import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import random
import pylab
import multiprocessing
import datetime
import numpy as np
import json

def my_bag_poisson(n, args, funcs, dts):
    m = args[0]
    ans = [[] for _ in range(len(dts))]
    m0 = np.random.poisson(m)
    degrees = list(np.full(m0 + 1, m0))
    neibours = [list(np.delete(np.arange(m0 + 1), i)) for i in np.arange(m0 + 1)]
    nodes = np.arange(m0 + 1)
    used = np.full(n, False)
    for i in range(m0, n):
        mi = max(1, min(np.random.poisson(m), nodes.shape[0]))
        conections = []
        j = 0
        while j < mi:
            choosen = random.choices(nodes, weights = degrees, k = 1)[0]
            if not used[choosen]:
                j += 1
                conections.append(choosen)
                used[choosen] = True
        neibours.append([])
        for j in conections:
            used[j] = False
            neibours[i + 1].append(j)
            neibours[j].append(i)
            degrees[j] += 1
        degrees.append(mi)
        nodes = np.append(nodes, nodes.shape[0])
        for j in range(len(dts)):
            if i % dts[j] == 0:
                ans[j].append(funcs[j](degrees, neibours))
    return ans

def my_triad(n, args, funcs, dts):
    m = args[0]
    p = args[1]
    ans = [[] for _ in range(len(dts))]
    degrees = list(np.full(m + 1, m))
    neibours = [list(np.delete(np.arange(m + 1), i)) for i in np.arange(m + 1)]
    nodes = np.arange(m + 1)
    used = np.full(n, False)
    for i in range(m, n):
        conections = []
        j = 0
        while j < m:
            if j == 0 or np.random.rand() > p:
                choosen = random.choices(nodes, weights = degrees, k = 1)[0]
            else:
                choosen = random.choices(neibours[conections[0]], k = 1)[0]
            if not used[choosen]:
                j += 1
                conections.append(choosen)
                used[choosen] = True
        neibours.append([])
        for j in conections:
            used[j] = False
            neibours[i + 1].append(j)
            neibours[j].append(i)
            degrees[j] += 1
        degrees.append(m)
        nodes = np.append(nodes, nodes.shape[0])
        for j in range(len(dts)):
            if i % dts[j] == 0:
                ans[j].append(funcs[j](degrees, neibours))
    return ans


def my_bag(n, args, funcs, dts):
    m = args[0]
    ans = [[] for _ in range(len(dts))]
    degrees = list(np.full(m + 1, m))
    neibours = [list(np.delete(np.arange(m + 1), i)) for i in np.arange(m + 1)]
    nodes = np.arange(m + 1)
    used = np.full(n, False)
    for i in range(m + 1, n):
        conections = []
        j = 0
        while j < m:
            choosen = random.choices(nodes, weights = degrees, k = 1)[0]
            if not used[choosen]:
                j += 1
                conections.append(choosen)
                used[choosen] = True
        neibours.append([])
        for j in conections:
            used[j] = False
            neibours[i].append(j)
            neibours[j].append(i)
            degrees[j] += 1
        degrees.append(m)
        nodes = np.append(nodes, nodes.shape[0])
        for j in range(len(dts)):
            if i % dts[j] == 0:
                ans[j].append(funcs[j](degrees, neibours))
    return ans

def run_thread(N, i, res, model, n, args, funcs, dts):
    ans = []
    for j in range(N):
        ans.append(model(n, args, funcs, dts))
    res[i] = ans
def run(N, treads, model, n, args, funcs, dts):
    procs = []
    manager = multiprocessing.Manager()
    res = manager.dict()
    for i in range(treads):
        curn = min(N, math.ceil(N / (treads - i)))
        p = multiprocessing.Process(target=run_thread, args=(curn, i, res, model, n, args, funcs, dts))
        N -= curn
        procs.append(p)
        p.start()
    for proc in procs:
        proc.join()
    ans = []
    for i in res.values():
        ans += i
    return ans
def d (degrees, neibours):
    return deepcopy(degrees)
def neibours (degrees, neibours):
    return deepcopy(neibours)
def index (degrees, neibours):
    return np.arange(len(neibours))
def s (degrees, neibours):
    return [sum([degrees[i] for i in j]) for j in neibours]
def alfa (degrees, neibours):
    return [si / di for (si, di) in zip(s(degrees, neibours), d(degrees, neibours))]
def beta (degrees, neibours):
    return [ai / di for (ai, di) in zip(alfa(degrees, neibours), d(degrees, neibours))]
def mean_beta (degrees, neibours):
    return [mean(beta(degrees, neibours))]

if __name__ == "__main__":
    n = 10000
    m = 5
    p = 0.25
    
    for m in [3, 5]:
        for p in [0.25, 0.5, 0.75]:
            ans = run(10, 6, my_triad, n, [m, p], [beta, mean_beta], [n - 1, 100])
            beta_data = np.array([i[0] for i in ans])
            beta_data = [np.histogram(i[0], bins=1000) for i in beta_data]
            beta_data = [[i[0], np.delete(i[1], 1000)] for i in beta_data]
            beta_data = np.array(beta_data)
            beta_data = beta_data.transpose((1, 2, 0))
            beta_data = np.apply_along_axis(arr = beta_data, axis = 2, func1d = np.mean)
            with open('C:\\Users\\YURA\\source\\repos\\CSW\\util_storage\\triad_dist_beta_' + str(m) + '_' + str(p) + '.json', 'w') as f:
                json.dump(beta_data.tolist(), f)
                f.close()
            mean_beta_data = np.array([i[1] for i in ans])
            mean_beta_data = np.apply_along_axis(arr=mean_beta_data, axis=2, func1d=lambda x: x[0])
            mean_beta_data = mean_beta_data.transpose((1, 0))
            mean_beta_data = np.apply_along_axis(arr=mean_beta_data, axis=1, func1d=mean)
            with open('C:\\Users\\YURA\\source\\repos\\CSW\\util_storage\\triad_mean_beta_' + str(m) + '_' + str(p) + '.json', 'w') as f:
                json.dump(mean_beta_data.tolist(), f)
                f.close()
            
    for m in [4, 5, 6]:
        ans = run(10, 6, my_bag_poisson, n, [m, p], [beta, mean_beta], [n - 1, 100])
        beta_data = np.array([i[0] for i in ans])
        beta_data = [np.histogram(i[0], bins=1000) for i in beta_data]
        beta_data = [[i[0], np.delete(i[1], 1000)] for i in beta_data]
        beta_data = np.array(beta_data)
        beta_data = beta_data.transpose((1, 2, 0))
        beta_data = np.apply_along_axis(arr = beta_data, axis = 2, func1d = np.mean)
        with open('C:\\Users\\YURA\\source\\repos\\CSW\\util_storage\\bap_dist_beta_' + str(m) + '.json', 'w') as f:
            json.dump(beta_data.tolist(), f)
            f.close()
        mean_beta_data = np.array([i[1] for i in ans])
        mean_beta_data = np.apply_along_axis(arr=mean_beta_data, axis=2, func1d=lambda x: x[0])
        mean_beta_data = mean_beta_data.transpose((1, 0))
        mean_beta_data = np.apply_along_axis(arr=mean_beta_data, axis=1, func1d=mean)
        with open('C:\\Users\\YURA\\source\\repos\\CSW\\util_storage\\bap_mean_beta_' + str(m) + '.json', 'w') as f:
            json.dump(mean_beta_data.tolist(), f)
            f.close()
                
    for m in [3, 5]:
        ans = run(10, 6, my_bag, n, [m, p], [beta, mean_beta], [n - 1, 100])
        beta_data = np.array([i[0] for i in ans])
        beta_data = [np.histogram(i[0], bins=1000) for i in beta_data]
        beta_data = [[i[0], np.delete(i[1], 1000)] for i in beta_data]
        beta_data = np.array(beta_data)
        beta_data = beta_data.transpose((1, 2, 0))
        beta_data = np.apply_along_axis(arr = beta_data, axis = 2, func1d = np.mean)
        with open('C:\\Users\\YURA\\source\\repos\\CSW\\util_storage\\ba_dist_beta_' + str(m) + '.json', 'w') as f:
            json.dump(beta_data.tolist(), f)
            f.close()
        mean_beta_data = np.array([i[1] for i in ans])
        mean_beta_data = np.apply_along_axis(arr=mean_beta_data, axis=2, func1d=lambda x: x[0])
        mean_beta_data = mean_beta_data.transpose((1, 0))
        mean_beta_data = np.apply_along_axis(arr=mean_beta_data, axis=1, func1d=mean)
        with open('C:\\Users\\YURA\\source\\repos\\CSW\\util_storage\\ba_mean_beta_' + str(m) + '.json', 'w') as f:
            json.dump(mean_beta_data.tolist(), f)
            f.close()