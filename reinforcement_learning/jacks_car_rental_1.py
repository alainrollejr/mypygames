# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 18:31:43 2019

@author: aro
"""

import os
import sys
import pickle

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import numpy as np
from scipy.special import factorial

MAX_CARS_ON_LOCATION = 20
MAX_TRANSFER = 5
REWARD_FOR_RENTAL = 10
REWARD_FOR_TRANSFER = -2
PRACTICAL_PROB_THRESHOLD = 0.001 # we won't care about events that have less probability than this

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

def transition_possible(s,s_prime_candidate,x,y,a):    
    s_prime_calculated = s_prime(s,x,y,a)
    if np.array_equal(s_prime_candidate,s_prime_calculated) == False:
        return False  
    return True

# calculate p(s',r | s, a)
def mdp_prob(s_prime, s, a):
    mdp_elements = []
    for y1 in range(MAX_CARS_ON_LOCATION):
        if p_y1(y1) > PRACTICAL_PROB_THRESHOLD:
            for y2 in range(MAX_CARS_ON_LOCATION):
                if p_y1(y1)*p_y2(y2) > PRACTICAL_PROB_THRESHOLD:
                    r = reward(np.array([y1,y2]),a)
                    p = 0
                    for x1 in range(MAX_CARS_ON_LOCATION):
                        if p_x1(x1)*p_y2(y2)*p_y1(y1) > PRACTICAL_PROB_THRESHOLD:
                            for x2 in range(MAX_CARS_ON_LOCATION):
                                if p_x1(x1)*p_x2(x2)*p_y1(y1)*p_y2(y2) > PRACTICAL_PROB_THRESHOLD:
                                    x = np.array([x1,x2])
                                    y = np.array([y1, y2])                    
                                    if transition_possible(s,s_prime,x,y,a) == True:
                                        p += p_x1(x1)*p_x2(x2)*p_y1(y1)*p_y2(y2)
                    if p > 0:
                        mdp_elements.append([s_prime, s, r, a,p])
    return mdp_elements

def build_mdp():
    state_space = []
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            state_space.append(np.array([n1,n2]))
            
    mdp = []
    cnt=0
    possibilities = 11*pow(MAX_CARS_ON_LOCATION,4)
    for a in range(-MAX_TRANSFER,MAX_TRANSFER+1,1):
        for s in state_space:
            for s_prime in state_space:
                cnt +=1                
                elements = mdp_prob(s_prime, s, a)
                if len(elements) > 0:
                    mdp.append(elements)                
                    print('mdp scan ',100.0*cnt/possibilities,' percent complete', end='\n')
                    print("mdp grown with " + str(elements))
                    # on every update store the mdp as currently known
                    with open('mdp.data', 'wb') as filehandle: 
                        pickle.dump(mdp, filehandle)
    return mdp
                        
                    
        
    
    

def main(argv):
    
    # manual checks: should be true
    print(transition_possible(np.array([10,8]),
                               np.array([12,7]),
                               np.array([3,0]),
                               np.array([0,2]),1))
    
    # manual check: should yield non empty list when PRACTICAL_PROB_THRESHOLD <= 0.001
    print(mdp_prob(np.array([12,7]), np.array([10,8]),1))
    
    # on with the real job
    mdp = build_mdp()
    
    
    
    
    
if __name__ == "__main__":
    main(sys.argv)