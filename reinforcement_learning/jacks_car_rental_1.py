# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 18:31:43 2019

@author: aro
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import numpy as np
from scipy.special import factorial

MAX_CARS_ON_LOCATION = 20
MAX_TRANSFER = 5
REWARD_FOR_RENTAL = 10
REWARD_FOR_TRANSFER = -2

def poisson(lmbd, k):
    return np.exp(-lmbd)*np.power(lmbd,k)/factorial(k)
    

# distribution of returned cars in location 1
def p_x1(k):
    return poisson(3,k)

# distribution of returned cars in location 2
def p_x2(k):
    return poisson(2,k)

# distribution of rented cars in location 1
def p_y1(k):
    return poisson(3,k)

# distribution of rented cars in location 2
def p_y2(k):
    return poisson(4,k)
"""
    2 most important transition equations
"""
def s_prime(s,x,y,a):
    s_prime = np.array([0,0])
    s_prime[0] = min(s[0] + x[0] - y[0] - a,MAX_CARS_ON_LOCATION)
    s_prime[1] = min(s[1] + x[1] - y[1] + a,MAX_CARS_ON_LOCATION)
    return s_prime

def reward(y,a):
    return (y[0]+y[1])*REWARD_FOR_RENTAL + abs(a)*REWARD_FOR_TRANSFER    

def transition_possible(r_candidate,s,s_prime_candidate,x,y,a):    
    s_prime_calculated = s_prime(s,x,y,a)
    if np.array_equal(s_prime_candidate,s_prime_calculated) == False:
        return False  
    if r_candidate != reward(y,a):
        return False
    return True

# calculate p(s',r | s, a)
def mdp_prob(s_prime, r, s, a):
    p = 0
    for x1 in range(MAX_CARS_ON_LOCATION):
        for x2 in range(MAX_CARS_ON_LOCATION):
            for y1 in range(MAX_CARS_ON_LOCATION):
                for y2 in range(MAX_CARS_ON_LOCATION):
                    x = np.array([x1,x2])
                    y = np.array([y1, y2])                    
                    if transition_possible(r,s,s_prime,x,y,a) == True:
                        p += p_x1(x1)*p_x2(x2)*p_y1(y1)*p_y2(y2)
    return p

def build_mdp():
    state_space = []
    for n1 in range(1,MAX_CARS_ON_LOCATION):
        for n2 in range(1,MAX_CARS_ON_LOCATION):
            state_space.append(np.array([n1,n2]))
            
    mdp = []
    for a in range(5):
        for r in range(-10,50,2):
            for s in state_space:
                for s_prime in state_space:
                    p = mdp_prob(s_prime, r, s, a)
                    if p > 0.0:
                        mdp.append([s_prime, s, r, a,p])
    return mdp
                        
                    
        
    
    

def main(argv):
    mdp = build_mdp()
    print('mdp:' + str(mdp))
    
    
    
if __name__ == "__main__":
    main(sys.argv)