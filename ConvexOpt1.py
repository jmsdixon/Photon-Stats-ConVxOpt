# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 17:05:27 2021

Author: James Dixon
Date: Summer 2021

Convex Optimisation program

's' is signal estimate

"""
import numpy as np
from scipy.optimize import minimize

def Opt(MeasMtx,y,Errorbars,MaxPhtnNum):
    

    # Generate error bound
    epsilon = min(Errorbars)
    
    def objective(s):
        " minimise sum of P_0 and P_1"
        p01s = s[:2]
        return np.sum(p01s)
    
    def IneqCons(s):
        # some f(x)>=0
        # y=Theta*s + e --> e-(y-Theta*s)>=0
        """
        l2 norm of differences between modelled measuremnents and measurements
        is less than the minimum element of the errorbars
        """
        delta = y-np.dot(MeasMtx, s)
        return epsilon-np.linalg.norm(delta, ord=2)
    
        
    def EqCons(s):
        "sum of elements of s should be 1, normalisation"
        return (1 - np.sum(s))*1000
    

    # Define intitial guess for signal
    s_initial = np.random.rand(MaxPhtnNum)
    s_initial = s_initial/np.sum(s_initial)
    
    # Set bounds for elements of estimate s_i>=0
    b = (0., 1.0)
    bnds = ([])
    for i in range(0, MaxPhtnNum):
        bnds.append(b)
        
    # Store constratints
    con2 = {'type': 'ineq', 'fun': IneqCons}
    con1 = {'type': 'eq', 'fun': EqCons}
    cons = [con1,con2]
    
    
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