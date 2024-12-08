import os
import json
import matplotlib.pyplot as plt
import numpy as np
import math

def f(x, a, b):
    return pow(x * b, a)

def read(name):
    file = open('c:\\Users\\YURA\\source\\repos\\CSW\\util_storage\\' + name + '.json')
    data = json.load(file)
    bincnt = 1000
    # ans = np.histogram(data, bincnt)
    x = data[1]
    y = data[0]
    x = np.resize(x, 100)
    y = np.resize(y, 100)
    xl = list(range(0, 100))
    xl[0] = 0.1
    # y = data
    # plt.xscale("log")
    # plt.yscale("log")
    plt.bar(x, y)
    a = -0.6
    b = 0.01
    # line = [f(i, a, b) for i in xl]
    # plt.plot(xl, line, color = 'red')
    # plt.legend(['friendship index distribution', 'y = (x*' + str(b) + ')^' + str(a) + ''])
    # plt.savefig("C:\\Users\\YURA\\source\\repos\\CSW\\diploma_results\\static_log\\" + name + ".png")
    plt.show()
    plt.clf()
        
        
if __name__ == "__main__":
    read('bap_dist_beta_4')