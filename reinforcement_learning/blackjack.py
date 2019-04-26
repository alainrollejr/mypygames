# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:33:23 2019

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
import random
from numpy.random import choice

POSSIBLE_CARDS = (1,2,3,4,5,6,7,8,9,10) # all face cards have value 10
CARD_WEIGHTS =   (4.0/52.0,4.0/52.0,4.0/52.0,4.0/52.0,4.0/52.0,4.0/52.0,4.0/52.0,4.0/52.0,4.0/52.0,16.0/52.0)
GAMMA = 0.9 # discount factor
REWARD_WIN=+1.0
REWARD_DRAW=0.0
REWARD_BUST=-1.0
HIT = 1
STICK = 0
ALPHA = 0.01 # for moving average approach to Q value for (s,a) iso true average

MAX_EPSON = 0.5
MIN_EPSON = 0.01
EPSON_DECAY = 0.99999
EVAL_EPISODES = 10000

S = [] # state space
pi = [] # policy
optimal_pi = [] # optimal policy as per [Thorp], for benchmarking
Q = [] # action value function
Q_initiated = []
state_space = []
Q_dict = {} # dictionary that maps state to Q table index
pi_dict = {}

def init_optimal_pi():
    
    
    player_has_usable_ace = True
    
    for player_sum in range(12,22):
        for dealer_shows in range(1,11): # dealer shows ace has value 0
            if dealer_shows==1:
                dealer_shows_card =1
                if player_sum >= 19:
                    optimal_pi.append(STICK)
                else:
                    optimal_pi.append(HIT)
            else:
                dealer_shows_card = str(dealer_shows)
                
                if (dealer_shows >= 2) and (dealer_shows <= 8):
                    if player_sum >= 18:
                        optimal_pi.append(STICK)
                    else:
                        optimal_pi.append(HIT)
                else:
                    if player_sum >= 19:
                        optimal_pi.append(STICK)
                    else:
                        optimal_pi.append(HIT)
            
            
    player_has_usable_ace = False
    for player_sum in range(12,22):
        for dealer_shows in range(1,11): # dealer shows ace has value 0
            if dealer_shows==1:
                dealer_shows_card =1
                
                if player_sum >= 17:
                    optimal_pi.append(STICK)
                else:
                    optimal_pi.append(HIT)
                
            else:
                dealer_shows_card = str(dealer_shows)

                if (dealer_shows >= 2) and (dealer_shows <= 3):
                    if player_sum >= 13:
                        optimal_pi.append(STICK)
                    else:
                        optimal_pi.append(HIT)
                elif (dealer_shows >= 4) and (dealer_shows <= 6):
                    if player_sum >= 12:
                        optimal_pi.append(STICK)
                    else:
                        optimal_pi.append(HIT)
                else:
                    if player_sum >= 17:
                        optimal_pi.append(STICK)
                    else:
                        optimal_pi.append(HIT)

def init_Q():
    pi_ind = 0
    Q_ind = 0
    player_has_usable_ace = True
    
    for player_sum in range(12,22):
        for dealer_shows in range(1,11): # dealer shows ace has value 0
            
            dealer_shows_card = str(dealer_shows)
               
            pi.append(random_action())
            state_space.append((player_has_usable_ace,str(dealer_shows_card),player_sum))
            pi_dict[(player_has_usable_ace,dealer_shows_card,player_sum)] = pi_ind
            pi_ind += 1
            
            Q.append(0.0);
            Q_initiated.append(0)
            Q_dict[(player_has_usable_ace,dealer_shows_card,player_sum,STICK)] = Q_ind
            Q_ind += 1
            
            Q.append(0.0);
            Q_initiated.append(0)
            Q_dict[(player_has_usable_ace,dealer_shows_card,player_sum,HIT)] = Q_ind
            Q_ind += 1
            
    player_has_usable_ace = False
    for player_sum in range(12,22):
        for dealer_shows in range(1,11): # dealer shows ace has value 0
            
            dealer_shows_card = str(dealer_shows)
                
              
            pi.append(random_action())
            state_space.append((player_has_usable_ace,str(dealer_shows_card),player_sum))
            pi_dict[(player_has_usable_ace,dealer_shows_card,player_sum)] = pi_ind
            pi_ind += 1
            
            Q.append(0.0);
            Q_initiated.append(0)
            Q_dict[(player_has_usable_ace,dealer_shows_card,player_sum,STICK)] = Q_ind
            Q_ind += 1
            
            Q.append(0.0);
            Q_initiated.append(0)
            Q_dict[(player_has_usable_ace,dealer_shows_card,player_sum,HIT)] = Q_ind
            Q_ind += 1
            
def visualise_pi(policy):
    pi_ind = 0
    
    X = np.empty([10,1]) # dealer shows
    Y = np.empty([10,1]) # player sum
    Z = np.empty([10,10])
    
    player_has_usable_ace = True
    
   
    n2 = 0    
    for player_sum in range(12,22):
        Y[n2] = player_sum
        n1 = 0
        for dealer_shows in range(1,11): # dealer shows ace has value 1

            X[n1] = dealer_shows            
            Z[n2][n1] = policy[pi_ind]
            pi_ind += 1
            n1 += 1
        n2 += 1
        
    X, Y = np.meshgrid(X, Y)
    
    fig = plt.figure()
    plt.contourf( X,Y, Z, cmap=cm.coolwarm)
    plt.colorbar()
    plt.title('player has usable ace')
    plt.show()
    
    
    X = np.empty([10,1]) # dealer shows
    Y = np.empty([10,1]) # player sum
    Z = np.empty([10,10])
    player_has_usable_ace = False
    

    n2 = 0    
    for player_sum in range(12,22):
        Y[n2] = player_sum
        n1 = 0
        for dealer_shows in range(1,11): # dealer shows ace has value 1 
            #print(player_sum,dealer_shows)            
            X[n1] = dealer_shows
            Z[n2][n1] = policy[pi_ind]
            pi_ind += 1
            n1 += 1
        n2 += 1
        
    X, Y = np.meshgrid(X, Y)
    fig = plt.figure()
    plt.contourf(X,Y, Z, cmap=cm.coolwarm)
    plt.colorbar()
    plt.title('player has no usable ace')
    plt.show()
    
    for s in state_space:
        ind = pi_dict[s]
        print(s,'->',policy[ind])
        
    for s in state_space:
        sa_hit = (s[0],s[1],s[2],HIT)
        sa_stick = (s[0],s[1],s[2],STICK)
        ind_hit = Q_dict[sa_hit]
        ind_stick = Q_dict[sa_stick]
        print(sa_hit,'->',Q[ind_hit],Q_initiated[ind_hit],
              ';',sa_stick,'->',Q[ind_stick],Q_initiated[ind_stick])
        
        
def visualise_Q():
    
    # we expect the Q value that map to the final policy
    # to be distinctly positive towards +1.0
    # values lower than 0.0 point at a policy of best choice under not so good 
    # conditions (meaning the expected result is still to loose)    
    
    pi_ind = 0
    
    X = np.empty([10,1]) # dealer shows
    Y = np.empty([10,1]) # player sum
    Z = np.empty([10,10])
    
    player_has_usable_ace = True
    
   
    n2 = 0    
    for player_sum in range(12,22):
        Y[n2] = player_sum
        n1 = 0
        for dealer_shows in range(1,11): # dealer shows ace has value 1
            
            
            dealer_shows_card = str(dealer_shows)

            X[n1] = dealer_shows  
            Q_ind = Q_dict[(player_has_usable_ace,dealer_shows_card,player_sum,pi[pi_ind])]
            Z[n2][n1] = Q[Q_ind]
            pi_ind += 1
            n1 += 1
        n2 += 1
        
    X, Y = np.meshgrid(X, Y)
    
    fig = plt.figure()
    plt.contourf( X,Y, Z, cmap=cm.coolwarm)
    plt.colorbar()
    plt.title('Q for player has usable ace')
    plt.show()
    
    X = np.empty([10,1]) # dealer shows
    Y = np.empty([10,1]) # player sum
    Z = np.empty([10,10])
    
    player_has_usable_ace = False
    
   
    n2 = 0    
    for player_sum in range(12,22):
        Y[n2] = player_sum
        n1 = 0
        for dealer_shows in range(1,11): # dealer shows ace has value 0
            
            
            dealer_shows_card = str(dealer_shows)

            X[n1] = dealer_shows  
            Q_ind = Q_dict[(player_has_usable_ace,dealer_shows_card,player_sum,pi[pi_ind])]
            Z[n2][n1] = Q[Q_ind]
            pi_ind += 1
            n1 += 1
        n2 += 1
        
    X, Y = np.meshgrid(X, Y)
    
    fig = plt.figure()
    plt.contourf( X,Y, Z, cmap=cm.coolwarm)
    plt.colorbar()
    plt.title('Q for player has no usable ace')
    plt.show()
    
    
    
  
def update_pi(s):
    # adapt policy to new insights in Q (fully greedy)

    pi_ind = pi_dict[s]
    s_hit = (s[0],s[1],s[2],HIT)
    s_stick = (s[0],s[1],s[2],STICK)
    Q_ind_hit = Q_dict[s_hit]
    Q_ind_stick = Q_dict[s_stick]
    Q_hit = Q[Q_ind_hit]
    Q_stick = Q[Q_ind_stick]
    
    #if ((Q_initiated[Q_ind_hit]) > 0) and ((Q_initiated[Q_ind_stick]) > 0):
    if Q_hit > Q_stick:
        pi[pi_ind] = HIT
    elif Q_hit < Q_stick:
        pi[pi_ind] = STICK
    else: # equal Q, break tie randomly
        pi[pi_ind] = random_action()
        
        

def init_episode(dealer_cards, player_cards):  
    
    dealer_cards.append(choice(POSSIBLE_CARDS,p=CARD_WEIGHTS).astype(np.int)) #this is what the dealer shows
    dealer_cards.append(choice(POSSIBLE_CARDS,p=CARD_WEIGHTS).astype(np.int))
    
    player_cards.append(choice(POSSIBLE_CARDS,p=CARD_WEIGHTS).astype(np.int))
    player_cards.append(choice(POSSIBLE_CARDS,p=CARD_WEIGHTS).astype(np.int))
    
def has_ace(cards):
    for c in cards:
        if c == 1:
            return True
    return False

def has_usable_ace(cards):
    ace_used = False
    ace_found = False
    sum = 0
    for c in cards:
        if c == 1:
            ace_found = True
            if ace_used == False:
                ace_used = True
                sum += 11
            else:
                sum +=1
        else:
            sum += c
            
    if ace_found == True:
        if sum > 21:
            return False
        else:
            return True
    else:
        return False

def card_sum(cards):
    c_sum = 0
    ace_used = False
    if has_usable_ace(cards) == True:
        for c in cards:
            if c != 1:
                c_sum += int(c)
            else:
                if ace_used == False:
                    c_sum += 11
                    ace_used = True
                else:
                    c_sum +=1 # watch out for more than 1 ace
    else:
        for c in cards:
            if c != 1:
                c_sum += int(c)
            else:
                c_sum += 1
    return c_sum

def state(player_cards, dealer_cards):
    return (has_usable_ace(player_cards),str(dealer_cards[0]),card_sum(player_cards))

def player_action(player_cards, dealer_cards, policy,epson):
    c = card_sum(player_cards)
    if c < 12:
        return HIT
    if c == 21:
        return STICK
       
    index = pi_dict[state(player_cards, dealer_cards)]
    greedy_action = policy[index]
    
    v = random.uniform(0, 1)
    if v > epson:
        return greedy_action
    else:
        return random_action()
    
def random_action():
    v = random.uniform(0, 1)
    if v > 0.5:
        return HIT
    else:        
        return STICK
    
        
def play_episode(player_cards, dealer_cards,policy,epson,methodString,debugplay):
    visited_sa_list = []
    pa = HIT

    episode_end = False   
    
    
    if debugplay == True:        
        print('--------  NEW EPISODE   ------------\n')
    
    s = state(player_cards, dealer_cards)
    
    if debugplay == True:
        print('player_cards',player_cards)
        print('dealer_cards',dealer_cards)

        
    
    # state evaluation
    c_p = card_sum(player_cards)
    c_d = card_sum(dealer_cards)
    
    # first: player turns
    while pa == HIT:
        
        
                
        s = state(player_cards, dealer_cards)
        pa = player_action(player_cards, dealer_cards,policy,epson)
        
        
        
        # only remember the  interesting, non obvious actions
        if c_p >= 12:  
            cur_sa= (s[0],s[1],s[2],pa)
            cur_reward = 0
            
            if methodString == 'td':
                if len(visited_sa_list) > 0:
                    prev_sa = visited_sa_list.pop()
                    prev_sa_Q_ind = Q_dict[prev_sa]
                    cur_sa_Q_ind = Q_dict[cur_sa]
                    target = cur_reward + GAMMA*Q[cur_sa_Q_ind]
                    Q[prev_sa_Q_ind] = Q[prev_sa_Q_ind] + ALPHA*(target - Q[prev_sa_Q_ind])
                    update_pi((prev_sa[0],prev_sa[1],prev_sa[2]))
            
            visited_sa_list.append(cur_sa)
            
            
        if pa == HIT:
            player_cards.append(choice(POSSIBLE_CARDS,p=CARD_WEIGHTS).astype(np.int))
            
        if debugplay == True:
            if pa == HIT:
                print('player HITs')
                print('player_cards',player_cards)
            else:
                print('player STICKs')
            print('state',s)
                
        c_p = card_sum(player_cards)
        if c_p > 21:
            episode_end = True
            break
        
    
    while episode_end == False:         
        # dealer action (fixed policy)
        if c_d < 17: #HIT
            dealer_cards.append(choice(POSSIBLE_CARDS,p=CARD_WEIGHTS).astype(np.int))
            if debugplay == True:
                print('dealer HITs')
                print('dealer_cards',dealer_cards)
            c_d = card_sum(dealer_cards)
                
        else:     
            if debugplay == True:
                print('dealer STICKs')
            episode_end = True
        
       
    if c_d > 21:
        if c_p > 21:
            r = REWARD_BUST
        else:
            r=REWARD_WIN
    elif c_d == 21:
        if c_p == 21:
            r= REWARD_DRAW                    
        else:
            r=REWARD_BUST
    else:
        if c_p > 21:
            r = REWARD_BUST
        else:            
            if c_d > c_p:
                r = REWARD_BUST
            elif c_p > c_d:
                r = REWARD_WIN
            else: # equals
                r = REWARD_DRAW
            
    if methodString == 'td': # deal with the terminal state
        if len(visited_sa_list) > 0:
            prev_sa = visited_sa_list.pop()
            prev_sa_Q_ind = Q_dict[prev_sa]
            
            target = r
            Q[prev_sa_Q_ind] = Q[prev_sa_Q_ind] + ALPHA*(target - Q[prev_sa_Q_ind])    
            update_pi((prev_sa[0],prev_sa[1],prev_sa[2]))
      
            
    if debugplay == True:
        print('play ends:')              
        print('reward',r)
        print('----------')
        
    return (visited_sa_list, r)


def backprop(visited_sa_list, r, debugplay):            
    # episode done, backprop of reward
    for sa in visited_sa_list:        
                
        index = Q_dict[sa]
        if debugplay == True:
            print ('sa',sa)
            print('Q',Q[index])
#        if Q_initiated[index] == 0:
#            # first update            
#            Q[index] = r
#        else:
#            Q[index] = Q[index] + ALPHA*(r - Q[index])
        Q[index] = Q[index] + ALPHA*(r - Q[index])
        Q_initiated[index] = Q_initiated[index] +1
        
        if debugplay == True:
            print('new Q',Q[index])
            
        update_pi((sa[0],sa[1],sa[2]))
            
def test_pi(policy):
    player_wins = 0
    dealer_wins = 0
    draws = 0
    epson = 0 #epson = 0: no exploration
    debugplay = False
    for k in range(EVAL_EPISODES):
        dealer_cards = []
        player_cards = []       
        init_episode(dealer_cards, player_cards)
        
        result = play_episode(dealer_cards, player_cards,policy,epson,'mc',debugplay)
        if result[1] > 0:
            player_wins += 1
        elif result[1] < 0:
            dealer_wins += 1
        else:
            draws += 1
    
    print('policy testing:')
    print('---------------')
    print('player wins',100*player_wins/EVAL_EPISODES,'%')
    print('dealer wins',100*dealer_wins/EVAL_EPISODES,'%')
    print('draws',100*draws/EVAL_EPISODES,'%')

def main(argv):
    
    parser = argparse.ArgumentParser(description='MC e-greedy policy iteration on Sutton and Barto Blackjack problem example')
    
    
    parser.add_argument('-m','--method', help='mc:  Monte Carlo, td: TD(0)', required=False)
    parser.add_argument('-e','--episodes', help='-e <nr of episodes>', required=False)
    args = vars(parser.parse_args())
    
    
    method = args['method']
    episodes = args['episodes']
    
    if episodes is None:
        nr_episodes = 1
    else:
        nr_episodes = int(episodes)
    
    if nr_episodes < 100:
        debugplay = True
    else:
        debugplay = False
        
   
    if method is None:
        methodString = 'mc'
    else:
        methodString = 'td'
        
    epson = MAX_EPSON
    init_Q()
    init_optimal_pi()
    visualise_pi(optimal_pi)
    
    #print(Q_dict)
    for k in range(nr_episodes):
        dealer_cards = []
        player_cards = []       
        init_episode(dealer_cards, player_cards)
        
        result = play_episode(dealer_cards, player_cards,pi,epson,methodString,debugplay)
        
        if methodString == 'mc':
            backprop(result[0], result[1], debugplay)
    
        epson = max(epson*EPSON_DECAY,MIN_EPSON)
        
        if k % 1000 == 0:
            print("\rEpisode {}/{} (epson {}).".format(k, nr_episodes,epson), end="")
            sys.stdout.flush()

    if nr_episodes >= 100:
        visualise_pi(pi)
        visualise_Q()
        
    test_pi(pi) 
    print('Thorp policy:')
    test_pi(optimal_pi) 
        
    
    
        
    
    
if __name__ == "__main__":
    main(sys.argv)