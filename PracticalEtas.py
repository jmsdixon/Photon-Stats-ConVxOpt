# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 09:44:55 2021


Author: James Dixon
Date: Summer 2021

Form sets of practical detection efficiencies, choose 500 at random and write
to txt file

"""

import itertools as it
import random
from operator import itemgetter

NumFocks = 10
NumEtasChosen = 6


# Halves
Etas = [0.4*(0.5)**i for i in range(14)]

# Form all combinations of NumEtasChosen - 1 detection efficiencies from Etas
combos = list(it.combinations(Etas, NumEtasChosen - 1))


# Pick 500 random eta combo sets and write to text file
indices500 = random.sample(range(len(combos)), k=500)
Chosen_Combos500 = list(itemgetter(*indices500)(combos))

# Write to file.  Include largest efficiency 0.8 to ensure large spread
# of efficiencies
File = open('Rand500_HalvesEtas.txt','w')
for i in range(len(Chosen_Combos500)):
    combo = Chosen_Combos500[i]
    for j in range(NumEtasChosen - 1):
        File.write(str(combo[j]) + " ")
    File.write("0.8")
    File.write("\n")
File.close()