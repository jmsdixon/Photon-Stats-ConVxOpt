# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 11:00:48 2021

@author: jmsdi
"""

import numpy as np
import random
import matplotlib.pyplot as plt

focks = np.arange(10)
signals = []

save = False

for i in range(10):
    signal = []
    signal.append(random.uniform(0,0.5))
    signal.append(random.uniform(0, 1))
    p = random.random()*signal[1]
    for j in range(8):
        signal.append(p*np.exp(-j))
    signal = signal/sum(signal)
    signals.append(signal)

avg_signal = np.average(signals,axis=0)

for s in signals:
    plt.figure()
    plt.bar(focks,s)

plt.figure()
plt.bar(focks,avg_signal)
plt.title('Average of 100 signals')
plt.xlabel('Fock states')
plt.ylabel('P(n)')

if save == True:
    File = open('Signals3.txt','w')
    for i in range(len(signals)):
        s = signals[i]
        for j in range(len(s) - 1):
            File.write(str(s[j]) + " ")
        File.write(str(s[len(s) - 1]))
        File.write("\n")
    File.close()