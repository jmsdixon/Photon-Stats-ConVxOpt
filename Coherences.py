# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:38:26 2021

Author: James Dixon
Date: Summer 2021

Form sets of detection efficiencies 'Etas' from which combinations 
are chosen.  Corresponding measurement matrices 'M' are formed and mutual
coherence between columns computed.  The combinations of Etas are saved 
to txt file along with their coherence

Choose a set of Etas by uncommenting below.
For set 7 only, comment out line 80

"""

import numpy as np
import itertools as it
import Functions as funcs


NumFocks = 10
NumEtasChosen = 6
LargestEta = 0.8

# Define measurement matrix: rows are etas, columns are fock states
M = np.empty(shape=(NumEtasChosen,NumFocks))

# Defined sets of Etas:
# Uncomment Etas set or define as desired
# Combos1:
#Etas = [(i + 1)*LargestEta/15 for i in range(15)]

# Combos2: 
#Etas = [ LargestEta/(2**i) for i in range(15)]

# Combos3: 
#Etas = [ LargestEta/(4**i) for i in range(15)]

# Combos4:
#Etas = [ LargestEta - 0.79/(2**i) for i in range(15)]

# Combos5:
#Etas = [ 0.5/(2**i) for i in range(15)]

# Combos6:
#Etas = [0.8 - 0.01*i for i in range(8)] + [0.01 + 0.01*i for i in range(7)]

# Combos7: COMMENT OUT LINE 80
#Etas7_1 = [0.8 - 0.01*i for i in range(25)]
#Etas7_2 = [0.01 + 0.01*i for i in range(25)]
#combos7_1 = np.array(list(it.combinations(Etas7_1, 3)))
#combos7_2 = np.array(list(it.combinations(Etas7_2, 3)))
#combos = np.concatenate((combos7_1,combos7_2),axis=1)
#rows,cols = np.shape(combos)


#Combos8:
#Etas = [0.3/(np.sqrt(2)**i) for i in range(15)]

# Combos9:
#Etas = [0.8,0.4] + [ 0.2/(2**i) for i in range(13)]

# Combos10: V. Low Coh
Etas = [ LargestEta/(np.sqrt(2)**i) for i in range(15)]

# Combos11:
#Etas = [0.8] + [(0.4/np.sqrt(2))/(np.sqrt(2)**i) for i in range(14)]

# Combos12:
#Etas = [0.8] + [0.1/(np.sqrt(2)**i) for i in range(14)]

# Combos13:
#Etas = [0.8 - 0.4/(np.sqrt(2)**i) for i in range(14)]


# Form all combinations of NumEtasChosen Etas without repeats from 
# specified set.  COMMENT OUT LINE BELOW FOR SET 7
combos = list(it.combinations(Etas, NumEtasChosen))


        
# Calculate coherence for every Etas combo's measurement matrix
C = []
for Etas in combos:
    # Generate Corresponding Measurement Matrix
    for i in range(0,np.size(Etas)):
        for j in range(0,NumFocks):
            M[i,j] = funcs.ClickOptr(j,Etas[i])
    # Normalise columns of M
    l2norms = np.linalg.norm(M, ord=2, axis = 0)
    where_0 = np.where(l2norms == 0)
    l2norms[where_0] = 1
    M_norm = M/l2norms
    # Now find largest coherence between columns.
    # Calc Gram matrix of M and set diagonals to zero
    Gram = M_norm.transpose()@M_norm
    np.fill_diagonal(Gram,0)
    # Store largest coherence of each combo in order
    C.append(np.max(Gram))
    
# Write combos and coherences to file
File = open('.txt','w')
for i in range(len(C)):
    combo = combos[i]
    for j in range(0,NumEtasChosen):
        File.write(str(combo[j]) + " ")
    File.write(str(C[i]) + "\n")
File.close()
