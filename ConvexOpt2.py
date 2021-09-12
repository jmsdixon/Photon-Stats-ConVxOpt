# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 16:52:41 2021

Author: James Dixon
Date: Summer 2021

Convex Optimisation 2 program

's' is signal estimate

"""
import numpy as np
from scipy.optimize import minimize

def Opt(MeasMtx,y,Errorbars,MaxPhtnNum):
    
    
    def objective(s):
        "minimise l1 norm of P_0 and P_1"
        p01s = s[:2]
        return np.sum(p01s)
        
    def EqCons(s):
        "sum of elements of x is 1; normalised"
        return (1 - np.sum(s))*1000

        
    # Store constratints
    con1 = {'type': 'eq', 'fun': EqCons}
    cons = [con1]
    

    for i in range(np.size(y)):
        def IneqCon(s, i = i):
            """
            The difference bewtween a measurement y_i and the modelled y_i 
            is to be less than the corresponding element of the Errorbars 
            """
            delta = y[i]-np.dot(MeasMtx[i], s)
            return Errorbars[i]-np.abs(delta)
        cons.append({'type': 'ineq', 'fun': IneqCon})
        
    # Set bounds for elements of estimate s_i>=0
    b = (0., 1.0)
    bnds = ([])
    for i in range(0, MaxPhtnNum):
        bnds.append(b)
        
    # Define intitial guess for signal
    s_initial = np.random.rand(MaxPhtnNum)
    s_initial = s_initial/np.sum(s_initial)
    
    # Optimise
    solution = minimize(objective,s_initial,method='SLSQP',\
                        bounds=bnds,constraints=cons)
        
    # Re-optimise
    solution = minimize(objective,solution.x,method='SLSQP',\
                        bounds=bnds,constraints=cons)
    
    # Re-re-optimse
    solution = minimize(objective,solution.x,method='SLSQP',\
                        bounds=bnds,constraints=cons)
        
    # Triple-Re-optimse
    solution = minimize(objective,solution.x,method='SLSQP',\
                        bounds=bnds,constraints=cons)
        
    # Quadruple-Re-optimse
    solution = minimize(objective,solution.x,method='SLSQP',\
                        bounds=bnds,constraints=cons)
        
    # Quintuple-Re-optimse
    solution = minimize(objective,solution.x,method='SLSQP',\
                        bounds=bnds,constraints=cons)
        
    return solution.x

