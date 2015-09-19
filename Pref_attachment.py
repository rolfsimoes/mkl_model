# -*- coding: utf-8 -*-
import random
import pylab

N_slaves = 100 #Para visualizar bem a reta no log-log é preciso um valor grande
p_connect = 1.0
p_disconnect = 0.3
master_of = []
bag_of_masters = []
time_range = 10000 #Isto deve ser bem maior para capturar o comportamento

def setup(params):
    global N_slaves, master_of, bag_of_masters, p_connect, p_disconnect, time_range
    N_slaves = params["N"]
    master_of = [-1 for i in xrange(N_slaves)]
    bag_of_masters = []
    p_connect = params["connect_prob"]
    p_disconnect = params["disconnect_prob"]
    time_range = params["time_range"]

def step():
    for slave in xrange(N_slaves):
        if master_of[slave] == -1:
            if random.random() < p_connect:
                if len(bag_of_masters) > 0:
                    choosed_master = random.choice(bag_of_masters)
                else:
                    choosed_master = random.randint(0, N_slaves - 1)
                master_of[slave] = choosed_master
                bag_of_masters.append(choosed_master)
                bag_of_masters.append(slave)
        else:
            if random.random() < p_disconnect:
                bag_of_masters.remove(slave)
                bag_of_masters.remove(master_of[slave])
                master_of[slave] = -1

def run():
    for t in xrange(time_range):
        step()

def hist_masters_slave():
    master_count = [0 for i in xrange(N_slaves)]
    for slave in xrange(N_slaves):
        if master_of[slave] != -1:
            master_count[master_of[slave]] += 1
    hist_result = [0 for i in xrange(max(master_count) + 1)]
    for master in xrange(len(master_count)):
        hist_result[master_count[master]] += 1
    return hist_result

def plot(label):
    pylab.plot(hist_masters_slave(), "-o", label=label)
    pylab.yscale("log")
    pylab.xscale("log")

def experiment(params):
    setup(params)
    run()
    plot("disconnect_prob: " + str(params["disconnect_prob"]))

for i in xrange(0, 20, 2):
    params = {"N": 1000, "time_range": 1000, "connect_prob":1.0, "disconnect_prob":0.02 * i}
    experiment(params)
pylab.legend()
pylab.show()