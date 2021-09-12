# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 16:31:55 2021

Author: James Dixon
Date: Summer 2021

Define different signal fock distributions

"""

import numpy as np

def PoissonDist(mu, m):
    # Poisson distribution formula for signal vector formation
    return pow(mu,m)*np.exp(-mu)/np.math.factorial(m)

def ThermalDist(mu, m):
    # Geometric distribution formula for signal vector formation
    return 1/(mu + 1)*pow((mu/(mu + 1)),m)

def SubPoissDist(m):
    # P_0 and P_1 very high, P_m (m>1) low
    p0 = 0.3
    if m==0:
        p = p0
    else:
        p = 1.087313*np.exp(-m)
    return p

def LargeMultiDist(m):
    # P_0 and P_1 very low, P_m (m>1) high
    if m>1:
        p = np.random.uniform(0, 1)
    else:
        p = 0.01
    return p

def ArbitraryDist(m):
    d = np.array([0.35,0.45,0.1,0.05,0.025,0.01250,0.00625,0.003125,0.0015625,0.00078125,0.000390625,0.0001953125,9.765625*10**(-5),9.765625*10**(-5),0,0,0,0,0,0])
    return d[m]