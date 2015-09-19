# -*- coding: utf-8 -*-
import random
import pylab

N_slaves = 5000 #Para visualizar bem a reta no log-log é preciso um valor grande
p_connect = 1.0
p_disconnect = 0.2
master_of = []
bag_of_masters = []
time_range = 100 #Isto deve ser bem maior para capturar o comportamento

def setup():
    global master_of, bag_of_masters
    master_of = [-1 for i in xrange(N_slaves)]

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

def plot():
    pylab.plot(hist_masters_slave(), ".g")
    pylab.yscale("log")
    pylab.xscale("log")
    pylab.show()

setup()
run()
plot()
