# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 17:16:27 2019

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

GAMMA = 1.0 # discount factor
POLICY_THETA = 0.05 # threshold on deviation of V from true V for policy
MAX_CAPITAL=100
P_HEADS = 0.4
TERMINAL_STATE = -1



# ([s_prime, s, r, a,p])
S_PRIME_IND = 0
S_IND = 1
R_IND = 2
A_IND = 3
P_IND = 4

S = [] # state space
pi = [] # policy
V = [] # state value function

def index_for_s(s):
    ind = 0
    for ind in S:
        if ind==s:
            return ind
    if s == TERMINAL_STATE:   
        return MAX_CAPITAL+1

def build_state_space():
    for ind in range(MAX_CAPITAL+1):
        S.append(ind)
    
def action_range(s):
    return range(0,min(s,MAX_CAPITAL-s)+1)

def init_pi():
    for ind in range(MAX_CAPITAL+1):       
        pi.append(0) # minimal bet

def init_valuefunction():
    for ind in range(MAX_CAPITAL+1):
        V.append(0)
        
    # now the terminal state 
    V.append(0)
 

def visualise_value_function():
        
    plt.figure()
    plt.scatter(S,V[0:MAX_CAPITAL+1])
    plt.show()
    
    plt.figure()
    plt.scatter(S,pi)
    plt.show()

def p_sarsa(s,x,a):
    if s == TERMINAL_STATE:
        r = 0
        s_prime = TERMINAL_STATE
        p = 1.0
        return [s_prime,s,r,a,p]
    
    if x == 1: # heads
        s_prime = s + a
        p = P_HEADS
        if s_prime == MAX_CAPITAL:
            s_prime = TERMINAL_STATE
            r = +1
        else:
            r = 0
        return [s_prime,s,r,a,p]
    else: # tails
        s_prime = s -a
        p = 1.0 - P_HEADS
        if s_prime <= 0:
            s_prime = TERMINAL_STATE
        r = 0
        return [s_prime,s,r,a,p]
    
def build_mdp():
    mdp = []
    for s in S:
        for a in action_range(s):
            for x in range(2):
                # ([s_prime, s, r, a,p])
                mdp.append(p_sarsa(s,x,a))
    return mdp

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
        max_v = V[index]
        
        # re-evaluate all possible actions a
        for a in action_range(s):
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

def show_policy_alternatives(mdp):        
    plt.figure()
    for (index,s) in enumerate(S):
        old_action = pi[index]
        best_a = old_action
        best_v = V[index]
        
        print('state:',s,' alternatives for a=',best_a)
        print('-----------------------------------------')
        
        # re-evaluate all possible actions a
        for a in action_range(s):
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
            if v == best_v:
                print('a ',a)
                plt.scatter(s,a)
        
        
            
def policy_iteration(mdp):
    
    init_pi()
    init_valuefunction()
    
    max_iter = 10
    iter = 0
    policy_stable = False
    while (policy_stable == False) and (iter < max_iter):
        policy_evaluation(mdp)
        #visualise_value_function()    
        policy_stable = policy_improvement(mdp)
        iter += 1
        
    #visualise_value_function()
    
    filehandle = open('value_gambler1.data', 'wb') 
    pickle.dump(V, filehandle)   
    filehandle.close()
     
    filehandle = open('pi_gambler1.data', 'wb') 
    pickle.dump(pi, filehandle)
    filehandle.close()
    
    

def main(argv):
    
    parser = argparse.ArgumentParser(description='MDP based policy iteration on Sutton and Barto Gambler problem example')
    
    parser.add_argument('-p','--mdp_path', help='path to precalculated mdp', required=False)
    args = vars(parser.parse_args())
    
    path = args['mdp_path']   
    
    build_state_space()
    
    if path is None:
        mdp = build_mdp()
    else:    
        #if you already have the mdp precalculated, load it from file
        mdp = pickle.load(open(path, 'rb'))
        
    #graph_mdp_elements([9,10], mdp)
    
    
    policy_iteration(mdp)
    visualise_value_function()
    show_policy_alternatives(mdp)
    
    
    
if __name__ == "__main__":
    main(sys.argv)