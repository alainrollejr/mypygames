# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 18:31:43 2019

@author: aro
"""

import os
import sys
import pickle

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import numpy as np
from scipy.special import factorial

GAMMA = 0.9 # discount factor
POLICY_THETA = 0.01 # threshold on deviation of V from true V for policy
MAX_CARS_ON_LOCATION = 10
MAX_TRANSFER = 2
REWARD_FOR_RENTAL = 10
REWARD_FOR_TRANSFER = -2
MAX_SCAN_S_PRIME = 3
PRACTICAL_PROB_THRESHOLD = 0.01 # we won't care about events that have less probability than this
LAMBDA_X1 = 3/2.0
LAMBDA_X2 = 2/2.0
LAMBDA_Y1 = 3/2.0
LAMBDA_Y2 = 4/2.0

# ([s_prime, s, r, a,p])
S_PRIME_IND = 0
S_IND = 1
R_IND = 2
A_IND = 3
P_IND = 4


# global values
y1_range = []
y2_range = []
x1_range = []
x2_range = []
S = [] # state space
pi = [] # policy
V = [] # state value function

def visualise_value_function():
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    ind = 0
    X = np.empty([MAX_CARS_ON_LOCATION+1,1])
    Y = np.empty([MAX_CARS_ON_LOCATION+1,1])
    Z = np.empty([(MAX_CARS_ON_LOCATION+1),(MAX_CARS_ON_LOCATION+1)])
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            X[n1] = n1
            Y[n2] = n2
            Z[n1][n2] = V[ind]
            ind += 1
            
    X, Y = np.meshgrid(X, Y)
    print(X)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)         
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show() 
            
            
    

# function to get unique values 
def np_array_in_list(list,s):     
    for element in list:
        if element==s:
            return True
    return False
def state_is_negative(s):
    if s[0] < 0:
        return True
    if s[1] < 0:
        return True
    return False

    

def poisson(lmbd, k):
    return np.exp(-lmbd)*np.power(lmbd,k)/factorial(k)
    

# distribution of returned cars in location 1
def p_x1(k):
    return poisson(LAMBDA_X1,k)

# distribution of returned cars in location 2
def p_x2(k):
    return poisson(LAMBDA_X2,k)

# distribution of rented cars in location 1
def p_y1(k):
    return poisson(LAMBDA_Y1,k)

# distribution of rented cars in location 2
def p_y2(k):
    return poisson(LAMBDA_Y2,k)
"""
    2 most important transition equations
"""
def s_prime(s,x,y,a):
    s_prime = [0,0]
    s_prime[0] = min(s[0] + x[0] - y[0] - a,MAX_CARS_ON_LOCATION)
    s_prime[1] = min(s[1] + x[1] - y[1] + a,MAX_CARS_ON_LOCATION)
    return s_prime

def truncate_s(s):
    s[0] = min(s[0], MAX_CARS_ON_LOCATION)
    s[1] = min(s[1], MAX_CARS_ON_LOCATION)
    s[0] = max(s[0], 0)
    s[1] = max(s[1], 0)
    return s
    

def reward(y,a):
    return (y[0]+y[1])*REWARD_FOR_RENTAL + abs(a)*REWARD_FOR_TRANSFER    

def transition_possible(s,s_prime_candidate,x,y,a):    
    s_prime_calculated = s_prime(s,x,y,a)
    if s_prime_candidate != s_prime_calculated:
        return False  
    return True

# calculate p(s',r | s, a)
def mdp_prob(s_prime, s, a):
    mdp_elements = []
    for y1 in y1_range:        
        for y2 in y2_range:            
            r = reward([y1,y2],a)
            p = 0
            for x1 in x1_range:
                for x2 in x2_range:                    
                    x = [x1,x2]
                    y = [y1, y2]                 
                    if transition_possible(s,s_prime,x,y,a) == True:
                        p += p_x1(x1)*p_x2(x2)*p_y1(y1)*p_y2(y2)                        
                        if state_is_negative(s_prime) == True:
                            # you're out of business, give big negative reward
                            r = -1000
                        if p > PRACTICAL_PROB_THRESHOLD:
                            print('s=',s,'a=',a,'x1=',x1,'y1 =',y1,
                                  'x2=',x2,'y2 =', y2,'s_prime=',s_prime,'r = ', r)
            if p > PRACTICAL_PROB_THRESHOLD:
                mdp_elements.append([s_prime, s, r, a,p])
    return mdp_elements

def define_reasonable_xy_ranges():
    
    for y1 in range(MAX_CARS_ON_LOCATION):
        if p_y1(y1) > PRACTICAL_PROB_THRESHOLD:
            y1_range.append(y1)
    

    for y2 in range(MAX_CARS_ON_LOCATION):
        if p_y2(y2) > PRACTICAL_PROB_THRESHOLD:
            y2_range.append(y2)

    for x1 in range(MAX_CARS_ON_LOCATION):
        if p_x1(x1) > PRACTICAL_PROB_THRESHOLD:
            x1_range.append(x1)
    

    for x2 in range(MAX_CARS_ON_LOCATION):
        if p_x2(x2) > PRACTICAL_PROB_THRESHOLD:
            x2_range.append(x2)           
    
    

def build_mdp():
    state_space = []
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            state_space.append([n1,n2])
    define_reasonable_xy_ranges()        
    mdp = []
    cnt=0
    possibilities = (2*MAX_TRANSFER+1)*pow(MAX_CARS_ON_LOCATION,2)     
    for s in state_space:
        for a in range(-MAX_TRANSFER,MAX_TRANSFER+1,1):
            cnt +=1   
            if ((a < 0) and (abs(a) <= s[1])) or ((a >= 0) and (abs(a) <= s[0])):
            
                expected_s_prime = s_prime(s,[LAMBDA_X1,LAMBDA_X2],
                                           [LAMBDA_Y1,LAMBDA_Y2],a)
                print('considering action ', a, 'to take ', s,'->', expected_s_prime,' mdp scan ',100.0*cnt/possibilities,' percent complete')
                s_prime_candidates = []
                for i in range(-MAX_SCAN_S_PRIME,MAX_SCAN_S_PRIME+1,1):
                    for j in range(-MAX_SCAN_S_PRIME,MAX_SCAN_S_PRIME+1,1):
                        candidate = [0,0]
                        candidate[0] = expected_s_prime[0] + i
                        candidate[1] = expected_s_prime[1] + j
                        if np_array_in_list(s_prime_candidates,candidate) == False:
                            s_prime_candidates.append(candidate)       
                print(s_prime_candidates)
                
                
                for s_prime_c in s_prime_candidates:
                                
                    elements = mdp_prob(s_prime_c, s, a)
                    if len(elements) > 0:
                        for element in elements:
                            mdp.append(element)   
                            print("mdp grown with " + str(elements))
                            print("\n")
                            # on every update store the mdp as currently known
                            with open('mdp.data', 'wb') as filehandle: 
                                pickle.dump(mdp, filehandle)
    return mdp
                      
def build_state_space():    
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            S.append([n1,n2])
            
def init_pi():
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            pi.append(0) # a = 0 as initial default

def init_valuefunction():
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            V.append(0) # v = 0 as initial default         
def index_for_s(s):
    ind = 0
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            if s == [n1,n2]:
                return ind
            ind += 1
    return -1
            

                    
def policy_evaluation(mdp):
    # pi is a table with a deterministic action for every state in the state space
    # (ordered in the same way as the state space)
    eval_iter = 0
    while True:        
        delta = 0
        
        for (index,s) in enumerate(S):
            v = V[index]
            action_under_pi = pi[index]
            new_v = 0
            for m in mdp:
                if (m[A_IND] == action_under_pi) and (m[S_IND] == s):
                    p = m[P_IND]
                    r = m[R_IND]
                    s_prime = m[S_PRIME_IND]
                    s_prime_ind = index_for_s(s_prime)
                    if s_prime_ind >= 0:
                        v_prime = V[s_prime_ind]                    
                        new_v += p*(r + GAMMA*v_prime)
            V[index] = new_v
            delta = max(delta,abs(v-new_v))
            
        print('eval_iter ',eval_iter, 'delta ', delta)
        
        if delta < POLICY_THETA:
            break
        eval_iter += 1
        
    
    
    

def main(argv):
    
    parser = argparse.ArgumentParser(description='MDP based policy iteration on Sutton and Barto Jacks car rental example problem')
    
    parser.add_argument('-p','--mdp_path', help='path to precalculated mdp', required=False)
    args = vars(parser.parse_args())
    
    path = args['mdp_path']   
    
    
    if path is None:
        mdp = build_mdp()
    else:    
        #if you already have the mdp precalculated, load it from file
        mdp = pickle.load(open(path, 'rb'))
        
    print(mdp)
    
    build_state_space()
    init_pi()
    init_valuefunction()
    
    policy_evaluation(mdp)
    visualise_value_function()
    
    
    
    
    
    
if __name__ == "__main__":
    main(sys.argv)