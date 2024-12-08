import multiprocessing, datetime
def f(i, res):
    t1 = datetime.datetime.now()
    x = 0
    for _ in range(10000000):
        x += 1
    t2 = datetime.datetime.now()
    res[i] = datetime.timedelta(microseconds=0) + (t2 - t1)

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    procs = []
    res = manager.dict()
    t3 = datetime.datetime.now()
    for t in [1, 2, 4, 6]:
        for i in range(24//t):
            p = multiprocessing.Process(target = f, args = (i, res))
            procs.append(p)
            p.start()
        for p in procs:
            p.join()
    t4 = datetime.datetime.now()
    
    
    # print(list(map((lambda x:datetime(x)), res.values())))
    print(sum(res.values(), datetime.timedelta()))
    print(datetime.timedelta() + (t4 - t3))