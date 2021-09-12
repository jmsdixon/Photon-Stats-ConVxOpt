# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:54:38 2021

Author: James Dixon
Date: Summer 2021

Read and present data from files written by Interface.py

Below 'User don't change' lines, uncomment different plots as desired

"""

import numpy as np
import matplotlib.pyplot as plt
import Fock_distributions as dists
from operator import itemgetter

# Set to be consistent with read files
NumEtas = 6
MaxPhtnNum = 10

# Choose Eta combo set for file access and figure titles
# copy/paste name, add set num if necessary:   
# Mins_Etas_Cohs   LgStd_Etas_Cohs  Ran500_Etas_Cohs
# Rand500_PowerEtas100Sigs BestCombos_Powers100SigsMP14
# Rand500_HalvesEtas100Sigs   BestCombos_Halves100Sigs
# Ran500_Etas_Cohs10100Sigs   Ran500_Etas_Cohs10100SigsCOpt3

FileName = 'Ran500_Etas_Cohs10C1'


#USER DON'T CHANGE BELOW LINES
######################################################################
######################################################################

if 'Cohs' in FileName:
    coherence_consider = True
    multiple_signals = False
    if '100Sigs' in FileName:
        multiple_signals = True
else:
    coherence_consider = False
    multiple_signals = False

if coherence_consider == True and multiple_signals == False:
    # Some indices
    Idx_sig_ests = NumEtas
    #Idx_P01 = NumEtas + 1
    #Idx_MultiP = NumEtas + 2
    #Idx_SigEsts = NumEtas + 3
    Idx_Cohs = Idx_sig_ests + MaxPhtnNum
    
    
    # Read Eta combos and coherences from txt file
    file_in = open(FileName + '_Data.txt', 'r')
    lines = file_in.readlines()[2:]
    file_in.close()
    #lines.pop()
    
    NumCombos = np.size(lines)
    
    Etas = np.zeros([NumCombos,NumEtas])
    RMS_Err = np.zeros(NumCombos)
    P01 = np.zeros(NumCombos)
    MultiPhtn_ErrProb = np.zeros(NumCombos)
    Signal_Estimates = np.zeros([NumCombos,MaxPhtnNum])
    coherences = np.zeros(NumCombos)
    CumMulti_ErrorProb = np.zeros(NumCombos)
    
    line_count = 0
    for line in lines:
        Etas[line_count,:] = line.split(' ')[0:Idx_sig_ests]
        #RMS_Err[line_count] = line.split(' ')[NumEtas]
        #P01[line_count] = line.split(' ')[Idx_P01]
        #MultiPhtn_ErrProb[line_count] = line.split(' ')[Idx_MultiP]
        Signal_Estimates[line_count,:] = line.split(' ')[Idx_sig_ests:Idx_Cohs]
        coherences[line_count] = line.split(' ')[Idx_Cohs]
        
        line_count = line_count + 1
          
    signal = np.zeros(MaxPhtnNum)
    for i in range(0, MaxPhtnNum):
        signal[i] = dists.SubPoissDist(i)   
    signal = signal/np.sum(signal)
    
    signal_P01 = np.sum(signal[:2])
    est_P01 = np.sum(Signal_Estimates[:,:2],axis=1)
    P01_Rltv_Err = (est_P01 - signal_P01)/signal_P01
    
    Etas_StdDev = np.std(Etas, axis=1)
    
    #Etas_spacing = np.apply_along_axis(funcs.Spacing, 1, Etas)
    
    # Get EtaCombos with 30 lowest RMS errors and RMS errors
    indices = np.argpartition(RMS_Err, 10)[:10]
    LoRMS_Combos = list(itemgetter(*indices)(Etas))
    LoRms_RMS = list(itemgetter(*indices)(RMS_Err))
    LoRMS_P01 = list(itemgetter(*indices)(P01))
    
    
    
    # Store selected data - append to file
    #File = open('AllMins' + '_Data.txt','a')
    #File.write(str(np.mean(coherences)) + " ")
    #File.write(str(np.mean(RMS_Err)) + "\n") 
    #File.close()
    #File = open('AllLgStd' + '_Data.txt','a')
    #File.write(str(np.mean(RMS_Err)) + " ")
    #File.write(str(np.mean(Etas_StdDev)) + "\n") 
    #File.close()
    
    
    
    # Plot eta data
    #plt.figure()
    #plt.scatter(coherences,RMS_Err)
    #plt.title(FileName + ' RMS err vs coherence [1]')
    #plt.xlabel('Coherence')
    #plt.ylabel('Average RMS Error')
    #plt.show()
    
    #plt.figure()
    #plt.scatter(np.repeat(RMS_Err, len(Etas[0])), Etas)
    #plt.title(FileName + ' eta combos vs RMS [2]')
    #plt.xlabel('Average RMS Error')
    #plt.ylabel('Eta')
    #plt.show()
    
    #plt.figure()
    #i = 0
    #for combo in Etas:
    #    plt.scatter(np.repeat(RMS_Err[i],len(combo)),combo)
    #    i = i + 1
    #plt.title(' Eta Combos')
    #plt.xlabel('Combo')
    #plt.ylabel('Etas')
    #plt.show()
    
    #plt.figure()
    #plt.scatter(Etas_StdDev,coherences)
    #plt.title(FileName + ' Coherence vs Etas spread [3]')
    #plt.xlabel('Etas Std dev')
    #plt.ylabel('Coherence')
    #plt.show()
    
    #plt.figure()
    #plt.scatter(Etas_StdDev,RMS_Err)
    #plt.title(FileName + ' RMS Err vs Etas Std dev [4]')
    #plt.xlabel('Etas Std dev')
    #plt.ylabel('RMS Err')
    #plt.show()
    
    #plt.figure()
    #plt.scatter(Etas_StdDev,MultiPhtn_ErrProb)
    #plt.title(FileName + ' MultiPhtn_ErrProb vs Etas spread [5]')
    #plt.xlabel('Etas Std dev')
    #plt.ylabel('MultiPhtn_ErrProb')
    #plt.show()
    
    plt.figure()
    plt.scatter(coherences,MultiPhtn_ErrProb)
    plt.title(FileName + ' MultiPhtn_ErrProb vs coherences [6]')
    plt.xlabel('coherences')
    plt.ylabel('MultiPhtn_ErrProb')
    plt.show()
    
    plt.figure()
    plt.scatter(P01_Rltv_Err,MultiPhtn_ErrProb)
    plt.title(FileName + ' MultiPhtn_ErrProb vs P01_Rltv_Err [7]')
    plt.xlabel('P01_Rltv_Err')
    plt.ylabel('MultiPhtn_ErrProb')
    plt.show()
    
    #plt.figure()
    #plt.scatter(coherences,P01)
    #plt.axhline(y=signal_P01, color='r', linestyle='dashed', linewidth=2)
    #plt.title(FileName + ' P01 vs coherences [8]')
    #plt.xlabel('coherences')
    #plt.ylabel('P01')
    #plt.show()
    
    #plt.figure()
    #plt.scatter(Etas_StdDev,P01)
    #plt.axhline(y=signal_P01, color='r', linestyle='dashed', linewidth=2)
    #plt.title(FileName + ' P01 vs Etas_StdDev [9]')
    #plt.xlabel('Etas_StdDev')
    #plt.ylabel('P01')
    #plt.show()
    
    #plt.figure()
    #plt.scatter(RMS_Err,P01_Rltv_Err)
    #plt.title(FileName + ' P01_Rltv_Err vs RMS_Err [10]')
    #plt.xlabel('RMS_Err')
    #plt.ylabel('P01_Rltv_Err')
    #plt.show()
    
    #plt.figure()
    #plt.scatter(Etas_StdDev,P01_Rltv_Err)
    #plt.title(FileName + ' P01_Rltv_Err vs Etas_StdDev [11]')
    #plt.xlabel('Etas_StdDev')
    #plt.ylabel('P01_Rltv_Err')
    #plt.show()
    
    plt.figure()
    plt.scatter(coherences,P01_Rltv_Err)
    plt.title(FileName + ' P01_Rltv_Err vs coherences [12]')
    plt.xlabel('coherences')
    plt.ylabel('P01_Rltv_Err')
    plt.show()
    
    #plt.figure()
    #plt.scatter(Etas_spacing,P01_Rltv_Err)
    #plt.title(FileName + ' P01_Rltv_Err vs Etas_spacing [12]')
    #plt.xlabel('Etas_spacing')
    #plt.ylabel('P01_Rltv_Err')
    #plt.show()
    
    print('Avg P01_Rltv_Err: '+str(np.average(P01_Rltv_Err)))
    #print('Avg RMS_Err: '+str(np.average(RMS_Err)))
    print('Avg Coherence: '+str(np.average(coherences)))
    print('Avg std dev: '+str(np.average(Etas_StdDev)))
    
elif coherence_consider == True and multiple_signals == True:
    
    # Some indices
    ErrInd = NumEtas + MaxPhtnNum
    Std_ErrInd = ErrInd + MaxPhtnNum
    RltvInd = Std_ErrInd + MaxPhtnNum
    #Idx_SigEsts = NumEtas + 3
    #Idx_Cohs = Idx_SigEsts + MaxPhtnNum
    
    
    # Read Eta combos and coherences from txt file
    file_in = open(FileName + '_Data.txt', 'r')
    lines = file_in.readlines()[2:]
    file_in.close()
    #lines.pop()
    
    NumCombos = np.size(lines)
    
    Etas = np.zeros([NumCombos,NumEtas])
    Avg_Errors_Sigs = np.zeros([NumCombos,MaxPhtnNum])
    Std_Errors_Sigs = np.zeros([NumCombos,MaxPhtnNum])
    Avg_Rltv_Err_Sigs = np.zeros([NumCombos,MaxPhtnNum])
    Avg_RMS_Err_Sigs = np.zeros(NumCombos)
    Avg_P01_RltvErr = np.zeros(NumCombos)
    SigsAvg_CtvMultiPh_Error_Probs = np.zeros(NumCombos)
    Std_Rltv_Err_Sigs = np.zeros([NumCombos,MaxPhtnNum])
    Std_RMS_Err_Sigs = np.zeros(NumCombos)
    Std_P01_RltvErr = np.zeros(NumCombos)
    SigsStd_CtvMultiPh_Error_Probs = np.zeros(NumCombos)
    coherences = np.zeros(NumCombos)
    
    line_count = 0
    for line in lines:
        Etas[line_count,:] = line.split(' ')[0:NumEtas]
        Avg_Errors_Sigs[line_count,:] = line.split(' ')[NumEtas:ErrInd]
        Std_Errors_Sigs[line_count,:] = line.split(' ')[ErrInd:Std_ErrInd]
        Avg_Rltv_Err_Sigs[line_count,:] = line.split(' ')[Std_ErrInd:RltvInd]
        Avg_RMS_Err_Sigs[line_count] = line.split(' ')[RltvInd]
        Avg_P01_RltvErr[line_count] = line.split(' ')[RltvInd+1]
        SigsAvg_CtvMultiPh_Error_Probs[line_count] = line.split(' ')[RltvInd+2]
        Std_Rltv_Err_Sigs[line_count,:] = line.split(' ')[RltvInd+3:RltvInd+3+MaxPhtnNum]
        Std_RMS_Err_Sigs[line_count] = line.split(' ')[RltvInd+3+MaxPhtnNum]
        Std_P01_RltvErr[line_count] = line.split(' ')[RltvInd+4+MaxPhtnNum]
        SigsStd_CtvMultiPh_Error_Probs[line_count] = line.split(' ')[RltvInd+5+MaxPhtnNum]
        coherences[line_count] = line.split(' ')[RltvInd+6+MaxPhtnNum]
        
        line_count = line_count + 1
    
    
    # Some plots
    
    plt.figure()
    plt.scatter(np.repeat(Avg_P01_RltvErr, len(Etas[0])), Etas)
    plt.title('eta combos vs Avg_P01_RltvErr')
    plt.xlabel('Avg_P01_RltvErr (-ve -> under-estimated)')
    plt.ylabel('Eta')
    plt.show()
    
    plt.figure()
    plt.scatter(coherences, Avg_P01_RltvErr)
    plt.title('Avg P_01 Relative Error vs Coherence')
    plt.xlabel('Coherence')
    plt.ylabel('Avg Relative Error')
    plt.show()
    
    plt.figure()
    plt.scatter(SigsAvg_CtvMultiPh_Error_Probs, Avg_P01_RltvErr)
    plt.title('Avg_P01_RltvErr vs Fraction of signal err in MultiPhtn')
    plt.xlabel('Fraction of total signal err')
    plt.ylabel('Avg_P01_RltvErr')
    plt.show()
    
    plt.figure()
    plt.scatter(SigsAvg_CtvMultiPh_Error_Probs, Std_P01_RltvErr)
    plt.title('Std_P01_RltvErr_Sum vs Fraction of signal err in MultiPhtn')
    plt.xlabel('Fraction of total signal err')
    plt.ylabel('Std_P01_RltvErr')
    plt.show()
    
    plt.figure()
    plt.scatter(coherences, Avg_RMS_Err_Sigs)
    plt.title('Avg RMS Error vs Coherence')
    plt.xlabel('Coherence')
    plt.ylabel('Avg RMS Error')
    plt.show()
    
else:
    
    # Some indices
    ErrInd = NumEtas + MaxPhtnNum
    Std_ErrInd = ErrInd + MaxPhtnNum
    RltvInd = Std_ErrInd + MaxPhtnNum
    Idx_SigEsts = NumEtas + 3
    Idx_Cohs = Idx_SigEsts + MaxPhtnNum
    
    
    # Read Eta combos and coherences from txt file
    file_in = open(FileName + '_Data.txt', 'r')
    lines = file_in.readlines()[2:]
    file_in.close()
    #lines.pop()
    
    NumCombos = np.size(lines)
    
    Etas = np.zeros([NumCombos,NumEtas])
    Avg_Errors_Sigs = np.zeros([NumCombos,MaxPhtnNum])
    Std_Errors_Sigs = np.zeros([NumCombos,MaxPhtnNum])
    Avg_Rltv_Err_Sigs = np.zeros([NumCombos,MaxPhtnNum])
    Avg_RMS_Err_Sigs = np.zeros(NumCombos)
    Avg_P01_RltvErr = np.zeros(NumCombos)
    SigsAvg_CtvMultiPh_Error_Probs = np.zeros(NumCombos)
    Std_Rltv_Err_Sigs = np.zeros([NumCombos,MaxPhtnNum])
    Std_RMS_Err_Sigs = np.zeros(NumCombos)
    Std_P01_RltvErr = np.zeros(NumCombos)
    SigsStd_CtvMultiPh_Error_Probs = np.zeros(NumCombos)
    
    line_count = 0
    for line in lines:
        Etas[line_count,:] = line.split(' ')[0:NumEtas]
        Avg_Errors_Sigs[line_count,:] = line.split(' ')[NumEtas:ErrInd]
        Std_Errors_Sigs[line_count,:] = line.split(' ')[ErrInd:Std_ErrInd]
        Avg_Rltv_Err_Sigs[line_count,:] = line.split(' ')[Std_ErrInd:RltvInd]
        Avg_RMS_Err_Sigs[line_count] = line.split(' ')[RltvInd]
        Avg_P01_RltvErr[line_count] = line.split(' ')[RltvInd+1]
        SigsAvg_CtvMultiPh_Error_Probs[line_count] = line.split(' ')[RltvInd+2]
        Std_Rltv_Err_Sigs[line_count,:] = line.split(' ')[RltvInd+3:RltvInd+3+MaxPhtnNum]
        Std_RMS_Err_Sigs[line_count] = line.split(' ')[RltvInd+3+MaxPhtnNum]
        Std_P01_RltvErr[line_count] = line.split(' ')[RltvInd+4+MaxPhtnNum]
        SigsStd_CtvMultiPh_Error_Probs[line_count] = line.split(' ')[RltvInd+5+MaxPhtnNum]
        
        line_count = line_count + 1
    
    
    # Some plots
    plt.figure()
    plt.scatter(np.repeat(Avg_RMS_Err_Sigs, len(Etas[0])), Etas)
    plt.title('eta combos vs RMS')
    plt.xlabel('Average RMS Error')
    plt.ylabel('Eta')
    plt.show()
    
    plt.figure()
    plt.scatter(np.repeat(Avg_P01_RltvErr, len(Etas[0])), Etas)
    plt.title('eta combos vs Avg_P01_RltvErr')
    plt.xlabel('Avg_P01_RltvErr (-ve -> under-estimated)')
    plt.ylabel('Eta')
    plt.show()
    
    plt.figure()
    plt.scatter(SigsAvg_CtvMultiPh_Error_Probs, Avg_P01_RltvErr)
    plt.title('Avg P_01 Relative Err vs Fraction of signal err in P_m')
    plt.xlabel('Fraction of total signal err')
    plt.ylabel('Avg P_01 Relative Err')
    plt.show()
    
    plt.figure()
    plt.scatter(SigsAvg_CtvMultiPh_Error_Probs, Std_P01_RltvErr)
    plt.title('Std Dev P_01 Relative Err vs Fraction of signal err in P_m')
    plt.xlabel('Fraction of total signal err')
    plt.ylabel('Standard Deviation')
    plt.show()
    
