# -*- coding: utf-8 -*-
"""A collection of common dynamical systems stored as functions."""


import math

#------------------------------------------------------------------------------
#           LORENZ '63 ("butterfly") - define system
#------------------------------------------------------------------------------
def Lorenz63(pos, *params, **t):        #where pos is an array of length 3, and params is rho, sigma, beta
    """System of equations resulting in a 'butterfly attractor'. Derived in Lorenz(1963). 
    
    Takes 3 parameters and 3-dimensional array of positions."""  
    #default values for params:
    #rho = 28
    #sigma = 10
    #beta = 8/3
    if type(params[0]) is list and len(params[0]) >= 3:
        rho = params[0][0]
        sigma = params[0][1]
        beta = params[0][2]
    else:
        rho = 28
        sigma = 10
        beta = 8/3
    
    v = [1,1,1]    #placeholder
    
    v[0] = sigma*(pos[1]-pos[0])
    v[1] = pos[0]*(rho-pos[2])-pos[1]
    v[2] = pos[0]*pos[1]-beta*pos[2] 
    
    return v    #returns instantaneous rate of change
    
    
    
    
def Lorenz63_4var(pos, *params, **t):        #where pos is an array of length 4, and params is rho, sigma, beta
    """System of equations resulting in a 'butterfly attractor'. Derived in Lorenz(1963). 
    
    Takes 3 parameters and 4-dimensional array of positions. pos[3] is time."""  
    #default values for params:
    #rho = 28
    #sigma = 10
    #beta = 8/3
    if type(params[0]) is list and len(params[0]) >= 3:
        rho = params[0][0]
        sigma = params[0][1]
        beta = params[0][2]
    else:
        rho = 28
        sigma = 10
        beta = 8/3
    
    v = [1,1,1,1]    #placeholder
    
    v[0] = sigma*(pos[1]-pos[0])
    v[1] = pos[0]*(rho-pos[2])-pos[1]
    v[2] = pos[0]*pos[1]-beta*pos[2] 
    
    return v    #returns instantaneous rate of change) 
    
    
    
    
    
#------------------------------------------------------------------------------
#           LORENZ '84 - define system
#------------------------------------------------------------------------------
def Lorenz84(pos, *params, **t):              #where pos is an array of length 3 and params is [a, b, F, G]
    """System of 3 equations with 3 variables and 4 parameters derived in Lorenz(1984)."""
    #default values for params:
    #a = 0.25
    #b = 4
    #F = 8
    #G = 1.25
    if type(params[0]) is list and len(params[0]) >= 4:
        a = params[0][0]
        b = params[0][1]
        F = params[0][2]
        G = params[0][3]
    else:
        a = 0.25
        b = 4
        F = 8
        G = 1.25
    
    v = [1,1,1]
    
    v[0] = -(pos[1]**2)-(pos[2]**2)-(a*pos[0])+(a*F)
    v[1] = (pos[0]*pos[1]) - (b*pos[0]*pos[2]) - pos[1] + G
    v[2] = (b*pos[0]*pos[1]) + (pos[0]*pos[2]) - pos[2]
    
    return v    #returns instantaneous rate of change
    
    
    
    
def Lorenz84_4var(pos, *params, **t):              #where pos is an array of length 3 and params is [a, b, F, G]
    """System of 3 equations with 3 variables and 4 parameters derived in Lorenz(1984). Pos[3] is time."""
    #default values for params:
    #a = 0.25
    #b = 4
    #F = 8
    #G = 1.25
    if type(params[0]) is list and len(params[0]) >= 4:
        a = params[0][0]
        b = params[0][1]
        F = params[0][2]
        G = params[0][3]
    else:
        a = 0.25
        b = 4
        F = 8
        G = 1.25
    
    v = [1,1,1, 1]
    
    v[0] = -(pos[1]**2)-(pos[2]**2)-(a*pos[0])+(a*F)
    v[1] = (pos[0]*pos[1]) - (b*pos[0]*pos[2]) - pos[1] + G
    v[2] = (b*pos[0]*pos[1]) + (pos[0]*pos[2]) - pos[2]
    
    return v    #returns instantaneous rate of change
    
    
    
    
        
#------------------------------------------------------------------------------
#           TEST 3-var
#------------------------------------------------------------------------------
def Test(pos, *params, **t):
    """Simple test function to verify that various functions work consistently."""
    #default values for params:
    #a = 1
    if type(params[0]) is list and len(params[0]) >= 1:
        a = params[0][0]
    else:
        a = 1
    
    v = [1,1,1]
    
    v[0] = a
    v[1] = a
    v[2] = a
    
    return v     #returns instantaneous rate of change


#-------------------------------------------------------------------------------
#           NO NEW SYSTEMS BEYOND THIS POINT!
#-------------------------------------------------------------------------------

methodsHash = {"L63" : Lorenz63, "L84" : Lorenz84, "Test" : Test, "L63+time" : Lorenz63_4var, "L84+time" : Lorenz84_4var}        #Stores all the systems as strings. 
