# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 17:40:15 2021

Author: James Dixon
Date: Summer 2021

Interface between measurement, optimisation, analysis and plotting/saving
results

Choose experimental settings in Exp_Setup.py

Read and choose settings down to 'User don't change below lines'

"""
import numpy as np
import matplotlib.pyplot as plt
import ConvexOpt2 as COpt2
import ConvexOpt as COpt1
import Exp_Setup as setup
import Functions as funcs
import Fock_distributions as dists

# User settings:

NumIters_perCombo = 1
Iter_print = True # Every 100 measurements

# Set to save or just present data
SaveData = False

# Single or multiple signals
# Single signal as in report - can be changed to any in 'Fock_distributions.py'
# see line 80
single_signal = True
# If false, specify signals file name
signals_filename = 'Signals100'

# Single or multiple sets of Etas
OneEtasCombo = True
# If false, choose file to read Etas from
# copy/paste:
# coherence files - Mins_Etas_Cohs  Ran500_Etas_Cohs  LgStd_Etas_Cohs
# practical eta files - Rand500_HalvesEtas  BestCombos_Halves
SetName = 'Ran500_Etas_Cohs'
# Choose Eta set number - for coherence consideration files only
SetNum = 10

# Enter number of etas in each combo in file
NumEtas = 6

# Set single combination of Etas:
# Evenly spaced combination -
#ChooseEtas = np.array([0.8 - i*0.8/(NumEtas) for i in range(NumEtas)])
#
# 'best' combination - 
ChooseEtas = np.array([4.000000e-01, 2.000000e-01, 1.000000e-01, 5.000000e-02,
       9.765625e-05, 8.000000e-01])


# Optimisation method:
CvxOpt_Method = 2    # 1, 2 or 3



# USER DON'T CHANGE BELOW LINES
###############################################################################
###############################################################################
# Open files, prepare variables and storage arrays for measurement/data 
# colletion

MaxPhtnNum = setup.MaxPhtnNum
Focks = np.arange(MaxPhtnNum)

# Set signal(s):
# Single signal setting
if single_signal == True:
    single_signal_in = np.zeros(MaxPhtnNum)
    for i in range(0, MaxPhtnNum):
        single_signal_in[i] = dists.SubPoissDist(i)
    single_signal_in = single_signal_in/np.sum(single_signal_in)
    signal_set = single_signal_in
    num_signals = 1
# Read multiple signals from file
else:
    file = open(signals_filename + '.txt','r')
    ls = file.read().split('\n')
    file.close()
    ls.pop()
    signals = []
    for line in ls:
        for num in line.split(' '):
            signals.append(float(num))      
    signals = np.array(signals)
    signals = signals.reshape(len(ls),(MaxPhtnNum))
    signal_set = signals
    num_signals = len(signal_set)

# If considering eta combo coherences for multiple eta combos,
# read Eta combos/ coherences from txt file
if SetNum == None:
    filename = SetName + '.txt' 
else:
    filename = SetName + str(SetNum) + '.txt' 
    
if 'Cohs' in filename and OneEtasCombo == False:
    cohconsider = True
else:
    cohconsider = False
    SetNum = None

if OneEtasCombo == False:
    file_in = open(filename, 'r')
    lines = file_in.read().split('\n')
    file_in.close()
    lines.pop()
    data = []
    for line in lines:
        for num in line.split(' '):
            data.append(float(num))        
    data = np.array(data)
    if cohconsider == True:
        data = data.reshape(len(lines),(NumEtas+1))
        coherences = data[:,NumEtas]
        EtaCombos = np.delete(data,NumEtas,1)
    
        NumEtaCombos,NumEtas = EtaCombos.shape
    else:
        EtaCombos = data.reshape(len(lines),(NumEtas))
    
        NumEtaCombos,NumEtas = EtaCombos.shape

# Set to one etas combo
if OneEtasCombo == True:
    EtaCombos = ChooseEtas
    NumEtas = np.size(EtaCombos)
    NumEtaCombos = 1

###############################################################################
# Define Storage arrays for iterating EACH Etas combo
P01_Estimates = np.zeros(shape=(NumIters_perCombo,2))
Signal_Estimates = np.zeros(shape=(NumIters_perCombo,MaxPhtnNum))
Err_Dists = np.zeros(shape=(NumIters_perCombo,MaxPhtnNum))
Rltv_Errors = np.zeros(shape=(NumIters_perCombo,MaxPhtnNum))
RMS_Error = np.zeros(NumIters_perCombo)
#MA_Error = np.zeros(NumIters_perCombo)
CtvMultiPh_ErrorProbs = np.zeros(NumIters_perCombo)
Errors = np.zeros((NumIters_perCombo,MaxPhtnNum))
p_01_rltv_err_per_sigcombo = np.zeros(NumIters_perCombo)


# Define storage arrays for iterating over multiple signals
P01Est_sigs = np.zeros((NumEtaCombos,num_signals,2))
SigEst_Sigs = np.zeros((NumEtaCombos,num_signals,MaxPhtnNum))
RMS_Err_Sigs = np.zeros((NumEtaCombos,num_signals))
Rltv_Err_Sigs = np.zeros((NumEtaCombos,num_signals,MaxPhtnNum))
Avg_CtvMultiPh_Error_Probs = np.zeros((NumEtaCombos,num_signals))
Avg_Errors = np.zeros((NumEtaCombos,num_signals,MaxPhtnNum))
stds_CtvMultiPh_Error_Probs = np.zeros((NumEtaCombos,num_signals))
SigEst_Sigs_std = np.zeros((NumEtaCombos,num_signals,MaxPhtnNum))
P01_Ests_sum_std = np.zeros((NumEtaCombos,num_signals))
P_01_Rltv_avgs = np.zeros((NumEtaCombos,num_signals))
P_01_Rltv_stds = np.zeros((NumEtaCombos,num_signals))
Std_AvgErrs_P01 = np.zeros((NumEtaCombos,num_signals))

###############################################################################
###############################################################################
# For all signals and eta combos, take measurements and save/
# present data

signal_idx = - 1
breakloop = False
for signal in signal_set:
    # End loop for single signal
    if breakloop == True:
        print('breaking...')
        break
    signal_idx = signal_idx + 1
    print('Signal : ',signal_idx + 1)

    if num_signals == 1:
        signal = signal_set
        breakloop = True
        
    # Take NumIters_perCombo measurements for all eta combos
    # and store/present data
    #EtaCombo_idx = - 1
    for EtaSet_idx in range(NumEtaCombos):
        #EtaCombo_idx = EtaCombo_idx + 1
        
        # Set Eta combo
        if OneEtasCombo == True:
            TheseEtas = EtaCombos
        else:
            TheseEtas = EtaCombos[EtaSet_idx,:]
        
        # Form meaurement matrix given the combination of detection efficiencies
        MeasMatrix = setup.FormMeasMtx(Focks, TheseEtas)
        
        # For the specified number of iterations, call for a measurement
        # from the Exp_Setup, calculate the Errorbars and optimise to 
        # estimate the signal and store results
        for meas_num in range(0,NumIters_perCombo):
            if Iter_print == True and np.mod(meas_num,100) == 0:
                print('Measurement : ',meas_num)
            
            # Call for measurement from experimental setup
            y = setup.Measure(MeasMatrix,signal)
            
            
            # Errorbars = standard error of measurement means. form vector for 
            # experimentors' errorbars proportional to means
            noise = 1e-4
            sigma = noise*y
            Errorbars = sigma
            
            # Convex Optimise to estimate signal
            if CvxOpt_Method == 1:
                Est_x = COpt1.Opt(MeasMatrix, y, Errorbars, MaxPhtnNum)
            else:
                Est_x = COpt2.Opt(MeasMatrix, y, Errorbars, MaxPhtnNum)
            
            # Store results
            P01_Estimates[meas_num,:] = Est_x[:2]
            Signal_Estimates[meas_num,:] = Est_x
            Rltv_Errors[meas_num,:] = funcs.Rtv_Errors(signal, Est_x)
            Err_Dists[meas_num,:] = funcs.Err_ProbDist(signal, Est_x)
            RMS_Error[meas_num] = funcs.RMS_Err(signal, Est_x)
            CtvMultiPh_ErrorProbs[meas_num] = np.sum(funcs.Err_ProbDist(signal, Est_x)[2:])
            Errors[meas_num,:] = funcs.Errors(signal, Est_x)
            p_01_rltv_err_per_sigcombo[meas_num] = funcs.P_01_Rltv_Errs(signal,Est_x)
            # End of measurement loops
        
        # Store/present data for ONE SIGNAL
        if num_signals == 1:
        
            # Get/present data for ONE SIGNAL, MULTIPLE MEASUREMENTS per combo of 
            # either one or multiple eta combos
            if NumIters_perCombo>1:
                
                # Averages of iteration over Etas combo data
                Avg_P01_Est = np.average(P01_Estimates, axis=0)
                Avg_Signal_Estimates = np.average(Signal_Estimates, axis=0)
                Avg_Rltv_Errors = np.average(Rltv_Errors, axis=0)
                Avg_Err_Dists = np.average(Err_Dists, axis=0)
                Avg_RMS_Error = np.average(RMS_Error)
                Avg_CtvMultiPh_Error_Probs = np.average(CtvMultiPh_ErrorProbs)

                P_01_Rltv_avgs[EtaSet_idx,signal_idx] = np.average(p_01_rltv_err_per_sigcombo)
                
                # Standard deviations
                Stdev_P01_Est = np.std(P01_Estimates, axis=0)
                Stdev_Signal_Estimates = np.std(Signal_Estimates, axis=0)
                Stdev_Rltv_Errors = np.std(P01_Estimates, axis=0)
                Stdev_Err_Dists = np.std(Err_Dists, axis=0)
                Stdev_RMS_Error = np.std(RMS_Error)
                Stdev_CtvMultiPh_Error_Probs = np.std(CtvMultiPh_ErrorProbs)
                
                P_01_Rltv_stds[EtaSet_idx,signal_idx] = np.std(p_01_rltv_err_per_sigcombo)
                
                # Standard Error of means
                StErr_RMS_Error = Stdev_RMS_Error/np.sqrt(NumIters_perCombo)
                
                # For ONE SIGNAL, ONE ETA COMBO, MULTIPLE MEASUREMENTS
                # for plot/print results 
                if OneEtasCombo == True:
                    
                    plt.figure()
                    plt.hist(np.sum(P01_Estimates,axis=1),edgecolor="red", bins=20)
                    plt.axvline(x=np.sum(signal[:2]), color='r', linestyle='dashed', linewidth=2)
                    plt.title('Histogram sum(P01) ests - CVxOpt' + str(CvxOpt_Method) + '. Noise - ' + str(noise) + '. msmnts - ' + str(NumIters_perCombo))
                    plt.legend(["Actual value","Estimates"])
                    plt.xlabel('Estimated P_01')
                    plt.ylabel('Number of occurences')
                    plt.show
                    
                    plt.figure()
                    plt.bar(Focks - 0.2, signal, 0.2, label = 'Signal')
                    plt.bar(Focks + 0.2, Avg_Signal_Estimates, 0.2, label = 'Avg Est Signal')
                    plt.xticks(Focks)
                    plt.xlabel('Fock State (|n>)')
                    plt.ylabel('P(n)')
                    plt.title('CVxOpt' + str(CvxOpt_Method) + '. Noise - ' + str(noise) + '. msmnts - ' + str(NumIters_perCombo))
                    plt.legend()
                    plt.show
                    
                    #plt.figure()
                    #plt.bar(Focks,Avg_Err_Dists)
                    #plt.xticks(Focks)
                    #plt.xlabel('Fock State (|n>)')
                    #plt.ylabel('P(n)')
                    #plt.title('Est err distribution - CVxOpt' + str(CvxOpt_Method) + '. Noise - ' + str(noise) + '. msmnts - ' + str(NumIters_perCombo))
                    #plt.show()
                    
                    P01_Ests_sum = np.sum(P01_Estimates,axis=1)
                    inds = np.array(np.where(P01_Ests_sum > np.sum(signal_set[:2])))
                    
                    print('Sum of P_0 and P_1 Signals = ',np.sum(signal[:2]))
                    print('Sum of P_0 and P_1 avg_estimates = ',np.sum(Avg_P01_Est))
                    print('Avg_RMS_Error = ',Avg_RMS_Error)
                    print('Avg cumulative multiphoton error prob = ',Avg_CtvMultiPh_Error_Probs)
                    print('% P_01 Ests > Signal P_01 = ',np.size(inds)/NumIters_perCombo)
                    print('Average P_01 relative errors = ',P_01_Rltv_avgs[EtaSet_idx,signal_idx])
                    
                # Store for ONE SIGNAL, MULTIPLE MEASUREMENTS, MULTIPLE COMBOS
                else:
                    print('EtasCombos index: ',EtaSet_idx)
                    P01Est_sigs[EtaSet_idx,signal_idx,:] = Avg_P01_Est
                    SigEst_Sigs[EtaSet_idx,signal_idx,:] = Avg_Signal_Estimates
                    RMS_Err_Sigs[EtaSet_idx,signal_idx] = Avg_RMS_Error
            
            
            # Get/present data for ONE SIGNAL, ONE MEASUREMENT per combo of 
            # either one or multiple eta combos
            else: 
                if OneEtasCombo == True:
                    # Results for ONE SIGNAL, ONE MEASUREMENT of ONE COMBO
                    plt.figure()
                    plt.bar(Focks - 0.2, signal, 0.2, label = 'Signal')
                    plt.bar(Focks + 0.2, Est_x, 0.2, label = 'Est Signal')
                    plt.xticks(Focks)
                    plt.xlabel('Fock State (|n>)')
                    plt.ylabel('P(n)')
                    plt.title('Uncorrupted signal and estimated signal')
                    plt.legend()
                    plt.show
                    
                    plt.figure()
                    plt.bar(Focks,Err_Dists[0,:])
                    plt.xticks(Focks)
                    plt.xlabel('Fock State (|n>)')
                    plt.ylabel('P(n)')
                    plt.title('Estimation error distribution')
                    plt.show()
                    
                    
                    print('Sum of P_0 and P_1 Signals = ',np.sum(signal[:2]))
                    print('Sum of P_0 and P_1 estimates = ',np.sum(Est_x[:2]))
                    print('Sum of estimated signal elements = ',np.sum(Est_x))
                    print('RMS_Error = ',RMS_Error)
                    print('Cumulative multiphoton error prob = ',CtvMultiPh_ErrorProbs)
                    print('P_01_Rltv_Err = ',p_01_rltv_err_per_sigcombo)

                # Store results for ONE SIGNAL, ONE MEASUREMENT of MULTIPLE 
                # COMBOS
                else:
                    print("we're gettin there...")
                    P_01_Rltv_avgs[EtaSet_idx,signal_idx] = p_01_rltv_err_per_sigcombo
        
        # Store data for multiple signals
        if num_signals > 1:
            
            # Averages of measurements
            P_01_Rltv_avgs[EtaSet_idx,signal_idx] = np.average(p_01_rltv_err_per_sigcombo)
            SigEst_Sigs[EtaSet_idx,signal_idx,:] = np.average(Signal_Estimates,axis=0)
            RMS_Err_Sigs[EtaSet_idx,signal_idx] = np.average(RMS_Error)
            Rltv_Err_Sigs[EtaSet_idx,signal_idx,:] = np.average(Rltv_Errors,axis=0)
            Avg_CtvMultiPh_Error_Probs[EtaSet_idx,signal_idx] = np.average(CtvMultiPh_ErrorProbs)
            Avg_Errors[EtaSet_idx,signal_idx,:] = np.average(Errors,axis=0)
            # Std devs of measurements
            SigEst_Sigs_std[EtaSet_idx,signal_idx,:] = np.std(Signal_Estimates,axis=0)
            stds_CtvMultiPh_Error_Probs[EtaSet_idx,signal_idx] = np.std(CtvMultiPh_ErrorProbs)
            P01_Ests_sum_std[EtaSet_idx,signal_idx] = np.std(np.sum(P01_Estimates,axis=1))
            P_01_Rltv_stds[EtaSet_idx,signal_idx] = np.std(p_01_rltv_err_per_sigcombo)
            Std_AvgErrs_P01[EtaSet_idx,signal_idx] = np.std(np.sum(Errors[:,:2],axis=1))
            
# Plot and save data for 1 signal and multiple eta combos
if OneEtasCombo == False and num_signals == 1:
    
    if cohconsider == True:
    
        plt.figure()
        plt.scatter(coherences,RMS_Err_Sigs.reshape(NumEtaCombos))
        plt.title(SetName + str(SetNum) + ' RMS err vs coherence')
        plt.xlabel('Coherence')
        plt.ylabel('Average RMS Error')
        plt.show()
        
        plt.figure()
        plt.scatter(coherences,P_01_Rltv_avgs.reshape(NumEtaCombos))
        plt.title(SetName + str(SetNum) + ' P_01 rltv err vs coherence')
        plt.xlabel('Coherence')
        plt.ylabel('P_01_Rltv_avgs')
        plt.show()
        
        plt.figure()
        plt.scatter(np.repeat(RMS_Err_Sigs.reshape(NumEtaCombos), len(EtaCombos[0])), EtaCombos)
        plt.title(SetName + str(SetNum) + ' eta combos vs RMS')
        plt.xlabel('Average RMS Error')
        plt.ylabel('Eta')
        plt.show()
        
        # Save selected data if set to do so
        if SaveData == True:
            File = open(SetName + str(SetNum) + 'C'+ str(CvxOpt_Method)+'_Data.txt','w')
            File.write('NumEtas 6, NumFocks 10, dark count 1e-7, noise/errorbars 1e-4, iterations per set '+str(NumIters_perCombo)+', convx opt 2' + "\n" + "\n")
            for i in range(len(coherences)):
                combo = EtaCombos[i]
                for j in range(0,NumEtas):
                    File.write(str(combo[j]) + " ")
                for k in range(0,np.size(Focks)):
                    File.write(str(SigEst_Sigs[i,signal_idx,k]) + " ")
                File.write(str(coherences[i]) + "\n")
            File.close()
    
    else:
        
        plt.figure()
        plt.scatter(np.repeat(P_01_Rltv_avgs.reshape(NumEtaCombos), len(EtaCombos[0])), EtaCombos)
        plt.title(SetName+' eta combos vs P_01 rltv errs,'+ str(NumIters_perCombo)+' measmnts')
        plt.xlabel('P01 Rltv Errs (-ve : under-estimated)')
        plt.ylabel('Eta')
        plt.show()
        
        # Store selected data
        if SaveData == True:
            File = open(SetName + str(SetNum) + 'C'+ str(CvxOpt_Method)+'_Data.txt','w')
            File.write('NumEtas 6, NumFocks 10, dark count 1e-7, noise/errorbars 1e-4, iterations per set '+str(NumIters_perCombo)+', convx opt 2' + "\n" + "\n")
            for i in range(len(coherences)):
                combo = EtaCombos[i]
                for j in range(0,NumEtas):
                    File.write(str(combo[j]) + " ")
                for k in range(0,np.size(Focks)):
                    File.write(str(SigEst_Sigs[i,signal_idx,k]) + " ")
                File.write(str(coherences[i]) + "\n")
            File.close()
           
            
# Plot and save data for multiple signals and eta combos
if num_signals > 1:
    
    Avg_RMS_Err_Sigs = np.average(RMS_Err_Sigs,axis=1)
    Avg_Rltv_Err_Sigs = np.average(Rltv_Err_Sigs,axis=1)
    SigsAvg_CtvMultiPh_Error_Probs = np.average(Avg_CtvMultiPh_Error_Probs,axis=1)
    Avg_Errors_Sigs = np.average(Avg_Errors,axis=1)
    
    Avg_P_01_Rltv_avgs = np.average(P_01_Rltv_avgs,axis=1)
    #Avg_P_01_Rltv_stds = np.average(P_01_Rltv_stds,axis=1)
    
    Std_RMS_Err_Sigs = np.std(RMS_Err_Sigs,axis=1)
    Std_Rltv_Err_Sigs = np.std(Rltv_Err_Sigs,axis=1)
    SigsStd_CtvMultiPh_ProbErrors = np.std(Avg_CtvMultiPh_Error_Probs,axis=1)
    Std_Errors_Sigs = np.std(Avg_Errors,axis=1)
    
    Std_P_01_Rltv_avgs = np.std(P_01_Rltv_avgs,axis=1)

    
    # For one combo present results
    if OneEtasCombo == True:
        
        Sig_Nums = np.arange(num_signals) + 1
        P_01_AbsErr = np.sum(Avg_Errors[:,:,:2],axis=2).reshape(num_signals)
        
        plt.figure()
        plt.bar(Sig_Nums,P_01_Rltv_avgs.reshape(num_signals),0.663)
        plt.errorbar(Sig_Nums,P_01_Rltv_avgs.reshape(num_signals),yerr=P_01_Rltv_stds.reshape(num_signals)/np.sqrt(NumIters_perCombo),fmt=".",ecolor="r",capsize=1.5)
        plt.xlabel('Signals')
        plt.ylabel('Avg P_01 relative error')
        plt.title('P01_RltvErr for each signal')
        
        pstv_indices = np.array(np.where(P_01_Rltv_avgs.reshape(num_signals) > 0))
        colour = np.zeros(num_signals)
        if np.any(pstv_indices):
            colour[pstv_indices] = 1
        
        P_01_All_Sigs = signal_set[:,0].reshape(num_signals) + signal_set[:,1].reshape(num_signals)
        
        plt.figure()
        plt.scatter(P_01_All_Sigs,P_01_Rltv_avgs.reshape(num_signals),c=colour,cmap='bwr')
        plt.errorbar(P_01_All_Sigs,P_01_Rltv_avgs.reshape(num_signals),yerr=P_01_Rltv_stds.reshape(num_signals)/np.sqrt(NumIters_perCombo),fmt=".",ecolor="r",capsize=1.5)
        plt.xlabel("P_01")
        plt.ylabel('Avg P_01 Relative Error')
        plt.title('P_01 relative error vs P_01, all signals')
        
        #plt.figure()
        #plt.scatter(signal_set[:,0].reshape(num_signals),P_01_Rltv_avgs.reshape(num_signals),c=colour,cmap='bwr')
        #plt.xlabel("P_0")
        #plt.ylabel('P_01 relative error')
        #plt.title('P_01 relative error vs P_0')
        #
        #plt.figure()
        #plt.scatter(signal_set[:,1].reshape(num_signals),P_01_Rltv_avgs.reshape(num_signals),c=colour,cmap='bwr')
        #plt.xlabel("P_1")
        #plt.ylabel('P_01 relative error')
        #plt.title('P_01 relative error vs P_1')
        
        plt.figure()
        plt.scatter(np.abs(P_01_AbsErr),P_01_Rltv_avgs.reshape(num_signals))
        plt.errorbar(np.abs(P_01_AbsErr),P_01_Rltv_avgs.reshape(num_signals),xerr=Std_AvgErrs_P01.reshape(num_signals)/np.sqrt(NumIters_perCombo),yerr=P_01_Rltv_stds.reshape(num_signals)/np.sqrt(NumIters_perCombo),fmt=".",ecolor="r",capsize=1.5)
        plt.xlabel('Avg P_01 Absolute Error')
        plt.ylabel('Avg P_01 Relative Error')
        plt.title('P_01 Relative Errs vs Abs Err')
        
        plt.figure() 
        plt.scatter(Sig_Nums,Avg_CtvMultiPh_Error_Probs.reshape(num_signals),s=3)
        plt.errorbar(Sig_Nums,Avg_CtvMultiPh_Error_Probs.reshape(num_signals),yerr=stds_CtvMultiPh_Error_Probs.reshape(num_signals)/np.sqrt(NumIters_perCombo),fmt=".",ecolor="r",capsize=1.5)
        plt.xlabel('Signal number')
        plt.ylabel('Fraction of total signal error')
        plt.title('Fraction of signal err from multiphoton err')
        
        plt.figure()
        plt.scatter(P_01_All_Sigs,np.abs(P_01_AbsErr))
        plt.errorbar(P_01_All_Sigs,np.abs(P_01_AbsErr),yerr=Std_AvgErrs_P01.reshape(num_signals)/np.sqrt(NumIters_perCombo),fmt=".",ecolor="r",capsize=1.5)
        plt.xlabel('P_01')
        plt.ylabel('Avg P_01 Absolute Error')
        plt.title('Absolute errs vs signal P_01')
        
        if pstv_indices.size > 0:
            plt.figure()
            plt.scatter(pstv_indices,signal_set[pstv_indices,0])
            plt.axhline(y=np.average(signal_set[:,0]), color='red', linestyle='--')
            plt.xlabel("signals P_0")
            plt.ylabel('P_0')
            plt.legend(['Average P_0 for all signals','P_0'])
            plt.title('Signal P_0 for +ve P_01 rltv err signals')
        
        plt.figure()
        plt.scatter(Sig_Nums,signal_set[:,0].reshape(num_signals),s=3,c=colour,cmap='bwr')
        plt.axhline(y=np.average(signal_set[:,0]), color='red', linestyle='--')
        plt.xlabel("Signal")
        plt.ylabel('P_0')
        plt.legend(['Average P_0 for all signals','P_0'])
        plt.title('Signal P_0 - red, +ve P_01 rltv errs')
        
        std_errs = (P01_Ests_sum_std.reshape(num_signals))/np.sqrt(NumIters_perCombo)
        plt.figure()
        plt.bar(Sig_Nums, np.sum(SigEst_Sigs[0,:,:2],axis=1), 0.35, label = 'Avg Est Signal')
        plt.errorbar(Sig_Nums, np.sum(SigEst_Sigs[0,:,:2],axis=1), yerr=std_errs, fmt=".", color="r",linewidth=0.01,capsize=3)
        plt.xlabel('Signals')
        plt.ylabel('P_01')
        plt.title('CVxOpt' + str(CvxOpt_Method) + '. Noise - ' + str(noise) + '. msmnts - ' + str(NumIters_perCombo))
        plt.show()
        
        if cohconsider == True:
            plt.figure()
            plt.scatter(coherences,Avg_P_01_Rltv_avgs)
            plt.title('P_01 rltv err avg over signals vs coherence')
            plt.xlabel('Coherence')
            plt.ylabel('P_01 rtlv err')
            plt.show()
    
    # For MULTIPLE COMBOS, present/save results
    else:
        
        plt.figure()
        plt.scatter(np.repeat(Avg_P_01_Rltv_avgs, len(EtaCombos[0])), EtaCombos)
        plt.title('eta combos vs Avg_P01_RltvErr_Sum')
        plt.xlabel('Avg_P01_RltvErr_Sum')
        plt.ylabel('Eta')
        plt.show()
        
        
        if cohconsider == True:
            plt.figure()
            plt.scatter(coherences,Avg_P_01_Rltv_avgs)
            plt.title('P_01 rltv err avg over signals vs coherence')
            plt.xlabel('Coherence')
            plt.ylabel('P_01 rtlv err')
            plt.show()
        
        
        # Store selected data
        if SaveData == True and cohconsider == True:
            File = open(SetName + str(SetNum) + 'C'+ str(CvxOpt_Method)+'100Sigs_Data.txt','w')
            File.write('Signals 100, NumEtas 6, NumFocks 10, dark count 1e-7, noise/errorbars 1e-4, measurements per set '+str(NumIters_perCombo)+', convx opt'+ str(CvxOpt_Method) + "\n" + "\n")
            for i in range(len(EtaCombos)):
                combo = EtaCombos[i]
                for j in range(0,NumEtas):
                    File.write(str(combo[j]) + " ")
                for m in range(MaxPhtnNum):
                    File.write(str(Avg_Errors_Sigs[i,m]) + " ")
                for n in range(MaxPhtnNum):
                    File.write(str(Std_Errors_Sigs[i,n]) + " ")
                for k in range(MaxPhtnNum):
                    File.write(str(Avg_Rltv_Err_Sigs[i,k]) + " ")
                File.write(str(Avg_RMS_Err_Sigs[i]) + " ")    
                File.write(str(Avg_P_01_Rltv_avgs[i]) + " ")
                File.write(str(SigsAvg_CtvMultiPh_Error_Probs[i]) + " ")
                for l in range(MaxPhtnNum):
                    File.write(str(Std_Rltv_Err_Sigs[i,l]) + " ")
                File.write(str(Std_RMS_Err_Sigs[i])+" ")
                File.write(str(Std_P_01_Rltv_avgs[i])+" ")
                File.write(str(SigsStd_CtvMultiPh_ProbErrors[i])+" ")
                File.write(str(coherences[i]))
                File.write("\n")
            File.close()
        elif SaveData == True and cohconsider == False:
            File = open(SetName + str(SetNum) + 'C'+ str(CvxOpt_Method)+'100Sigs_Data.txt','w')
            File.write('Signals 100, NumEtas 6, NumFocks 10, dark count 1e-7, noise/errorbars 1e-4, measurements per set '+str(NumIters_perCombo)+', convx opt'+ str(CvxOpt_Method) + "\n" + "\n")
            for i in range(len(EtaCombos)):
                combo = EtaCombos[i]
                for j in range(0,NumEtas):
                    File.write(str(combo[j]) + " ")
                for m in range(MaxPhtnNum):
                    File.write(str(Avg_Errors_Sigs[i,m]) + " ")
                for n in range(MaxPhtnNum):
                    File.write(str(Std_Errors_Sigs[i,n]) + " ")
                for k in range(MaxPhtnNum):
                    File.write(str(Avg_Rltv_Err_Sigs[i,k]) + " ")
                File.write(str(Avg_RMS_Err_Sigs[i]) + " ")    
                File.write(str(Avg_P_01_Rltv_avgs[i]) + " ")
                File.write(str(SigsAvg_CtvMultiPh_Error_Probs[i]) + " ")
                for l in range(MaxPhtnNum):
                    File.write(str(Std_Rltv_Err_Sigs[i,l]) + " ")
                File.write(str(Std_RMS_Err_Sigs[i])+" ")
                File.write(str(Std_P_01_Rltv_avgs[i])+" ")
                File.write(str(SigsStd_CtvMultiPh_ProbErrors[i]))
                File.write("\n")
            File.close()
    


