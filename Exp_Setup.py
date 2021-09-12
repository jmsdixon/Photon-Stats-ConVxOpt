# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 15:50:35 2021

Author: James Dixon
Date: Summer 2021

Simple program to model photodetection through a variable 
variable attenuator for a variety of detection efficiencies.  


User set: 
    Max Fock State 'MaxPhtnNum'', 
    Normal standard dev for experimental noise 'sigma_noise', 


"""

import numpy as np


# Set fock states parameters
MaxPhtnNum = 10 
Focks = np.arange(MaxPhtnNum)

# Measurement Noise, gaussian distributed about perfect measurement values
sigma_noise = 1e-4

# Set average dark count rate
dark_count = 1e-7
    

# USER DON'T CHANGE BELOW LINES
##########################################################################
##########################################################################

def ClickOptr(n, eta):
    # Click operator function, hat{Pi}.  Gives probability of 
    # a click given detector efficiency eta and n incident photons
    return 1-(1-dark_count)*(1-eta)**n


# Generate measurement matrix of measurement probabilities
# rows ~ detector efficiencies, columns ~ fock states
def FormMeasMtx(Focks,Etas):
    MeasMtx = np.empty(shape=(np.size(Etas),MaxPhtnNum))
    for i in range(0, np.size(Etas)):
        for j in range(0, MaxPhtnNum):
            MeasMtx[i,j] = ClickOptr(Focks[j],Etas[i])
    return MeasMtx
        

def Measure(MeasMatrix,signal):
    """
    Performs 'large number' of experimental measurements of noisy signal
    with specified selection of detector efficiencies
    
    Input: numpy array matrix - measurement matrix
    Returns: array of float - 'click probabilities'
    -------
    TYPE
        DESCRIPTION.

    """
    
    
    # Perform measurement of signal
    perfect_measurement = MeasMatrix@signal
    
    # Generate gaussian distributed statistical noise proportional to 
    # measurements
    Measurement_noise = (np.random.normal(0,perfect_measurement*sigma_noise))

    return perfect_measurement + Measurement_noise