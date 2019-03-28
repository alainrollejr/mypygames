# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 18:31:43 2019

@author: aro
"""

import os
import sys
import pickle
from graphviz import Digraph
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter


import matplotlib.pyplot as plt
from matplotlib import cm


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import numpy as np
from scipy.special import factorial

GAMMA = 0.9 # discount factor
POLICY_THETA = 0.5 # threshold on deviation of V from true V for policy
MAX_CARS_ON_LOCATION = 10
MAX_TRANSFER = 2
REWARD_FOR_RENTAL = 10
REWARD_FOR_TRANSFER = -2

PRACTICAL_PROB_THRESHOLD = 0.05 # we won't care about events that have less probability than this
LAMBDA_X1 = 2
LAMBDA_X2 = 1
LAMBDA_Y1 = 2
LAMBDA_Y2 = 2
TERMINAL_STATE = [-1,-1]

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
    A = np.empty([(MAX_CARS_ON_LOCATION+1),(MAX_CARS_ON_LOCATION+1)])
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            X[n1] = n1
            Y[n2] = n2
            Z[n2][n1] = V[ind]
            A[n2][n1] = pi[ind]
            print('n1',n1,'n2',n2,'a',pi[ind])
            ind += 1
            
    X, Y = np.meshgrid(X, Y)
    #print(X)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)         
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title('value function')
    plt.show() 
    
    fig = plt.figure()
    plt.contourf(X, Y, Z, cmap=cm.coolwarm)
    plt.colorbar()
    plt.title('value function')
    plt.show() 
    
    fig = plt.figure()
    
    plt.contourf(X, Y, A, cmap=cm.coolwarm)
    plt.colorbar()
    plt.title('actions (policy)')
    plt.show() 
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, A, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)         
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title('actions (policy)')
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
 

def reward(y,a):
    return (y[0]+y[1])*REWARD_FOR_RENTAL + abs(a)*REWARD_FOR_TRANSFER    



def p_sarsa(s,x,y,a):
    # if your are in terminal state you stay in terminal state
    if s == TERMINAL_STATE:
        s_prime = TERMINAL_STATE
        p = 1.0
        r = 0
        return [s_prime,s,r,a,p,x,y]
    p = p_x1(x[0])*p_x2(x[1])*p_y1(y[0])*p_y2(y[1])
    
    # if more cars are requested for rent than available at start of day
    # you are bust and go to terminal state
    if (s[0]-y[0] < 0): 
        r = 0        
        s_prime = TERMINAL_STATE
        return [s_prime,s,r,a,p,x,y]
    
    if (s[1]-y[1] < 0): 
        r = 0        
        s_prime = TERMINAL_STATE
        return [s_prime,s,r,a,p,x,y]
    
    # approaching the end of the day, the amount of available cars at a location
    # equals  s + x -y 
    # therefore you can never transfer more than this amount of cars to the other locations
    if a >  (s[0] +x[0] - y[0]):
        return []
    
    if -a > (s[1] +x[1] - y[1]):
        return []
        
    # no special corner cases -> default return values
    s_prime = [0,0]    
    s_prime[0] = min(s[0] + x[0] - y[0] - a,20)    
    s_prime[1] = min(s[1] + x[1] - y[1] + a,20)    
    r = reward(y,a)    
    return [s_prime,s,r,a,p,x,y]



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
   

    
def build_mdp(max_graph_index = 0):
    
    state_space = []
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            state_space.append([n1,n2])
    define_reasonable_xy_ranges()    

        
    mdp = []
    mdp_len = 0
    cnt=0
    possibilities = (2*MAX_TRANSFER+1)*pow(MAX_CARS_ON_LOCATION,2)     
    for s in state_space:
        for a in range(-MAX_TRANSFER,MAX_TRANSFER+1,1):    
            sa_list=[]   
            cnt +=1  
            print('mdp scan ',100.0*cnt/possibilities,' percent complete, len(mdp): ',mdp_len)
            
            for y1 in y1_range:        
                for y2 in y2_range:
                    for x1 in x1_range:
                        for x2 in x2_range: 
                            x = [x1,x2]
                            y = [y1,y2] 
                            
                            el = p_sarsa(s,x,y,a)
                            
                            #print(el)
                            
                            if len(el) > 0:
                                # aggregate equal (s',a,r,s) combinations to
                                # keep MDP representation small
                                if len(sa_list) == 0:
                                    sa_list.append(el)
                                else:
                                    exists = False
                                    for (ind,sa_el) in enumerate(sa_list):
                                        if sa_el[0:P_IND]==el[0:P_IND]:
                                            sa_list[ind][P_IND] += el[P_IND]
                                            exists = True
                                    if exists == False:
                                        sa_list.append(el)
                                            
                                        
            for sa_el in sa_list:                    
                mdp.append(sa_el)
                mdp_len +=1
                        
    filehandle = open('mdp.data', 'wb') 
    pickle.dump(mdp, filehandle)  
    filehandle.close()             
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
    # value of terminal state        
    V.append(0)
    
def index_for_s(s):
    ind = 0
    for n1 in range(0,MAX_CARS_ON_LOCATION+1,1):
        for n2 in range(0,MAX_CARS_ON_LOCATION+1,1):
            if s == [n1,n2]:
                return ind
            ind += 1
    if s == TERMINAL_STATE:
        return ind
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
        
def policy_improvement(mdp):
    policy_stable = True    
    
    for (index,s) in enumerate(S):
        old_action = pi[index]
        best_a = old_action
        max_v = -1000000
        
        # re-evaluate all possible actions a
        for a in range(-MAX_TRANSFER,MAX_TRANSFER+1,1):
            v = 0;
            for m in mdp:
                if (m[A_IND] == a) and (m[S_IND] == s):
                    p = m[P_IND]
                    r = m[R_IND]
                    s_prime = m[S_PRIME_IND]
                    s_prime_ind = index_for_s(s_prime)
                    if s_prime_ind >= 0:
                        v_prime = V[s_prime_ind]                    
                        v += p*(r + GAMMA*v_prime)
            if v > max_v:
                max_v = v
                best_a = a # argmax
        pi[index] = best_a # update policy
        if old_action != best_a:
            policy_stable = False
            
    return policy_stable
            
def policy_iteration(mdp):

    init_pi()
    init_valuefunction()
    
    max_iter = 10
    iter = 0
    policy_stable = False
    while (policy_stable == False) and (iter < max_iter):
        policy_evaluation(mdp)
        visualise_value_function()    
        policy_stable = policy_improvement(mdp)
        iter += 1
        
    
    
    filehandle = open('value_jack1.data', 'wb') 
    pickle.dump(V, filehandle)   
    filehandle.close()
     
    filehandle = open('pi_jack1.data', 'wb') 
    pickle.dump(pi, filehandle)
    filehandle.close()
    
def value_iteration(mdp):
    init_pi()
    init_valuefunction()
    delta = 10
    
    max_iter = 10
    iter = 0
    while (delta > POLICY_THETA) and (iter < max_iter):  
        delta = 0
        for (index,s) in enumerate(S):
            max_v = V[index]
            
            # re-evaluate all possible actions a
            for a in range(-MAX_TRANSFER,MAX_TRANSFER+1,1):
                v = 0;
                for m in mdp:
                    if (m[A_IND] == a) and (m[S_IND] == s):
                        p = m[P_IND]
                        r = m[R_IND]
                        s_prime = m[S_PRIME_IND]
                        s_prime_ind = index_for_s(s_prime)
                        if s_prime_ind >= 0:
                            v_prime = V[s_prime_ind]                    
                            v += p*(r + GAMMA*v_prime)
                if v > max_v:
                    max_v = v
 
            
            delta = max(delta, abs(max_v-V[index]))
            V[index] = max_v
        iter += 1
    policy_improvement(mdp)    

def main(argv):
    
    parser = argparse.ArgumentParser(description='MDP based policy iteration on Sutton and Barto Jacks car rental example problem')
    
    parser.add_argument('-p','--mdp_path', help='path to precalculated mdp', required=False)
    parser.add_argument('-m','--method', help='v:  value iteration, p: policy iteration', required=False)
    args = vars(parser.parse_args())
    
    path = args['mdp_path']   
    method = args['method']
    
    if method is None:
        value_iter = True
    else:
        if method=='v':
            value_iter = True
        elif method == 'p':
            value_iter = False
        else:
            print('unsupported method ',method)
            value_iter = True
    
    if path is None:
        mdp = build_mdp()
    else:    
        #if you already have the mdp precalculated, load it from file
        mdp = pickle.load(open(path, 'rb'))
        
    build_state_space()
    if value_iter == True:
        value_iteration(mdp)
    else:
        policy_iteration(mdp)
    
    visualise_value_function()
    
    
    
    
    
    
if __name__ == "__main__":
    main(sys.argv)