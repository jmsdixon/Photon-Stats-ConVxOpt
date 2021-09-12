# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 13:15:56 2021

Author: James Dixon
Date: Summer 2021

Choose samples from all coherences and corresponding eta combos written in
Coherences.py and save to txt files.

Samples chosen - 500 at random, 50 with lowest coherence and 50 with 
largest standard deviations


"""
import random
import numpy as np
from operator import itemgetter

# Set number of detectors
NumFocks = 10
NumEtasChosen = 6

# Read Eta combos and coherences from txt file written in Coherences.py
file_in = open('EtaSet10_Coherences.txt', 'r')
lines = file_in.read().split('\n')
file_in.close()
lines.pop()
data = []
for line in lines:
    for num in line.split(' '):
        data.append(float(num))
        
data = np.array(data)
data = data.reshape(len(lines),NumEtasChosen + 1)
coherences = data[:,NumEtasChosen]
EtaCombos = np.delete(data,NumEtasChosen,1)

# Pick 500 random eta combo sets and write to text file
indices500 = random.sample(range(len(coherences)), k=500)
Chosen_Combos500 = list(itemgetter(*indices500)(EtaCombos))
Chosen_Cohs500 = list(itemgetter(*indices500)(coherences))

File = open('Ran500_Etas_Cohs.txt','w')
for i in range(len(Chosen_Cohs500)):
    combo = Chosen_Combos500[i]
    #File.write(str(combos[index]) + " " + str(C[index]) + "\n")
    for j in range(0,NumEtasChosen):
        File.write(str(combo[j]) + " ")
    File.write(str(Chosen_Cohs500[i]) + "\n")
File.close()

    
# Form an ordered store of 50 smallest coherences and their
# corresponding combo
indices = np.argpartition(coherences, 50)[:50]

Chosen_Combos = list(itemgetter(*indices)(EtaCombos))
Chosen_Cohs = list(itemgetter(*indices)(coherences))


File = open('Mins_Etas_CohsTest.txt','w')
for i in range(len(Chosen_Cohs)):
    combo = Chosen_Combos[i]

    for j in range(0,NumEtasChosen):
        File.write(str(combo[j]) + " ")
    File.write(str(Chosen_Cohs[i]) + "\n")
File.close()

# Form a set of etas with the largest std dev
StdDevs = np.std(EtaCombos,axis=1)
std_indices = np.argpartition(StdDevs, 50)[-50:]

Chosen_CombosStd = list(itemgetter(*std_indices)(EtaCombos))
Chosen_CohsStd = list(itemgetter(*std_indices)(coherences))

File = open('LgStd_Etas_CohsTest.txt','w')
for i in range(len(Chosen_CohsStd)):
    combo = Chosen_CombosStd[i]

    for j in range(0,NumEtasChosen):
        File.write(str(combo[j]) + " ")
    File.write(str(Chosen_CohsStd[i]) + "\n")
File.close()