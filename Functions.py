# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 10:04:21 2021


Author: James Dixon
Date: Summer 2021

Some functions. Mostly error calculations

"""
import numpy as np

dark_count = 1e-7

def ClickOptr(n, eta):
    # Click operator function, hat{Pi}.  Gives probability of 
    # a click given detector efficiency eta and n incident photons
    return 1-(1-dark_count)*(1-eta)**n

def Errors(signal, est_signal):
    """"Difference between estimated signal and signal elements
    returns: numpy array
    """
    return est_signal-signal

def Rtv_Errors(signal, est_signal):
    """Relative error between estimated signal and signal elements
    returns: numpy array
    """
    return Errors(signal, est_signal)/signal

def MA_Err(signal, est_signal):
    """ Mean absolute error between est_signal and signal
    returns: float
    """
    s = np.abs(Errors(signal, est_signal))
    return np.sum(s)/np.size(s)

def RMS_Err(signal, est_signal):
    """"RMS error between est_signal and signal
    returns: float
    """
    s = (Errors(signal, est_signal))**2
    return np.sqrt(np.sum(s)/np.size(s))

def Err_ProbDist(signal, est_signal):
    """
    Get disribution of error probabilities for each predicted fock state

    Parameters
    ----------
    signal : numpy array.
    est_signal : numpy array.

    Returns: numpy array
    -------
    None.

    """
    p = np.abs(Errors(signal, est_signal))
    return p/np.sum(p)

def P_01_Rltv_Errs(signal, est_signal):
    """
    

    Parameters
    ----------
    signal : TYPE
        DESCRIPTION.
    est_signal : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    p = Errors(signal[:2], est_signal[:2])
    return np.sum(p)/np.sum(signal[:2])
