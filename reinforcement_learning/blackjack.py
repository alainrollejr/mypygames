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

POSSIBLE_CARDS = ('A',1,2,3,4,5,6,7,8,9,10) # all face cards have value 10
GAMMA = 1.0 # discount factor
REWARD_WIN=+1.0
REWARD_DRAW=0.0
REWARD_BUST=-1.0
HIT = 1
STICK = 0
ALPHA = 0.01 # for moving average approach to Q value for (s,a) iso true average
MAX_EPSON = 0.8
MIN_EPSON = 0.01
EPSON_DECAY = 0.999999

S = [] # state space
pi = [] # policy
Q = [] # action value function
Q_initiated = []
state_space = []
Q_dict = {} # dictionary that maps state to Q table index
pi_dict = {}

# episode variables

def init_Q():
    pi_ind = 0
    Q_ind = 0
    player_has_usable_ace = True
    
    for player_sum in range(12,22):
        for dealer_shows in range(11): # dealer shows ace has value 0
            if dealer_shows==0:
                dealer_shows_card ='A'
            else:
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
        for dealer_shows in range(11): # dealer shows ace has value 0
            if dealer_shows==0:
                dealer_shows_card ='A'
            else:
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
            
def visualise_pi():
    pi_ind = 0
    
    X = np.empty([11,1]) # dealer shows
    Y = np.empty([10,1]) # player sum
    Z = np.empty([10,11])
    
    player_has_usable_ace = True
    
   
    n2 = 0    
    for player_sum in range(12,22):
        Y[n2] = player_sum
        n1 = 0
        for dealer_shows in range(11): # dealer shows ace has value 0

            X[n1] = dealer_shows            
            Z[n2][n1] = pi[pi_ind]
            pi_ind += 1
            n1 += 1
        n2 += 1
        
    X, Y = np.meshgrid(X, Y)
    
    fig = plt.figure()
    plt.contourf( X,Y, Z, cmap=cm.coolwarm)
    plt.colorbar()
    plt.title('player has usable ace')
    plt.show()
    
    
    X = np.empty([11,1]) # dealer shows
    Y = np.empty([10,1]) # player sum
    Z = np.empty([10,11])
    player_has_usable_ace = False
    

    n2 = 0    
    for player_sum in range(12,22):
        Y[n2] = player_sum
        n1 = 0
        for dealer_shows in range(11): # dealer shows ace has value 0  
            #print(player_sum,dealer_shows)            
            X[n1] = dealer_shows
            Z[n2][n1] = pi[pi_ind]
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
        print(s,'->',pi[ind])
        
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
    
    X = np.empty([11,1]) # dealer shows
    Y = np.empty([10,1]) # player sum
    Z = np.empty([10,11])
    
    player_has_usable_ace = True
    
   
    n2 = 0    
    for player_sum in range(12,22):
        Y[n2] = player_sum
        n1 = 0
        for dealer_shows in range(11): # dealer shows ace has value 0
            
            if dealer_shows==0:
                dealer_shows_card ='A'
            else:
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
    
    X = np.empty([11,1]) # dealer shows
    Y = np.empty([10,1]) # player sum
    Z = np.empty([10,11])
    
    player_has_usable_ace = False
    
   
    n2 = 0    
    for player_sum in range(12,22):
        Y[n2] = player_sum
        n1 = 0
        for dealer_shows in range(11): # dealer shows ace has value 0
            
            if dealer_shows==0:
                dealer_shows_card ='A'
            else:
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
    
    if Q_hit > Q_stick:
        pi[pi_ind] = HIT
    elif Q_hit < Q_stick:
        pi[pi_ind] = STICK
    else: # equal Q, break tie randomly
        pi[pi_ind] = random_action()
        
        

def init_episode(dealer_cards, player_cards):  
    
    dealer_cards.append(random.choice(POSSIBLE_CARDS)) #this is what the dealer shows
    dealer_cards.append(random.choice(POSSIBLE_CARDS))
    
    player_cards.append(random.choice(POSSIBLE_CARDS))
    player_cards.append(random.choice(POSSIBLE_CARDS))
    
def has_ace(cards):
    for c in cards:
        if c == 'A':
            return True
    return False

def has_usable_ace(cards):
    ace_used = False
    ace_found = False
    sum = 0
    for c in cards:
        if c == 'A':
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
            if c != 'A':
                c_sum += int(c)
            else:
                if ace_used == False:
                    c_sum += 11
                    ace_used = True
                else:
                    c_sum +=1 # watch out for more than 1 ace
    else:
        for c in cards:
            if c != 'A':
                c_sum += int(c)
            else:
                c_sum += 1
    return c_sum

def state(player_cards, dealer_cards):
    return (has_usable_ace(player_cards),str(dealer_cards[0]),card_sum(player_cards))

def player_action(player_cards, dealer_cards, epson):
    c = card_sum(player_cards)
    if c < 12:
        return HIT
    if c == 21:
        return STICK
       
    index = pi_dict[state(player_cards, dealer_cards)]
    greedy_action = pi[index]
    
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
    
        
def play_episode(player_cards, dealer_cards,epson,debugplay):
    visited_sa_list = []
    pa = HIT

    episode_end = False
    
    if debugplay == True:
        print('------------------------------------\n')
        print('--------  NEW EPISODE   ------------\n')
        print('------------------------------------\n')
    
    s = state(player_cards, dealer_cards)
    
    if debugplay == True:
        print('player_cards',player_cards)
        print('dealer_cards',dealer_cards)

        
    
    # state evaluation
    c_p = card_sum(player_cards)
    c_d = card_sum(dealer_cards)
    
    # first: player turn
    while pa == HIT:
        s = state(player_cards, dealer_cards)
        pa = player_action(player_cards, dealer_cards,epson)
        
        # only remember the  interesting, non obvious actions
        if card_sum(player_cards) >= 12:       
            visited_sa_list.append((s[0],s[1],s[2],pa))
            
            
        if pa == HIT:
            player_cards.append(random.choice(POSSIBLE_CARDS))
            
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
    if debugplay == True:
        print('player_cards',player_cards)
        
    
    while episode_end == False:         
        # dealer action (fixed policy)
        if c_d < 17: #HIT
            dealer_cards.append(random.choice(POSSIBLE_CARDS))
            if debugplay == True:
                print('dealer HITs')
                print('dealer_cards',dealer_cards)
                
        else:     
            if debugplay == True:
                print('dealer STICKs')
            episode_end = True
        c_d = card_sum(dealer_cards)
            
           
    
    
    if c_d > 21:
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
            
        
      
            
    if debugplay == True:
        print('play ends:')              
        print('reward',r)
        print('----------')
            
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
            


def main(argv):
    
    parser = argparse.ArgumentParser(description='MC e-greedy policy iteration on Sutton and Barto Blackjack problem example')
    
    
    parser.add_argument('-m','--method', help='e:  epson greedy on policy, s: exploring starts', required=False)
    parser.add_argument('-e','--episodes', help='-e <nr of episodes>', required=False)
    args = vars(parser.parse_args())
    
    
    method = args['method']
    episodes = args['episodes']
    
    if episodes is None:
        nr_episodes = 1
    else:
        nr_episodes = int(episodes)
    
    if nr_episodes < 10:
        debugplay = True
    else:
        debugplay = False
        
   
    if method is None:
        epson_greedy = True
    else:
        if method=='e':
            epson_greedy = True
        elif method == 's':
            epson_greedy  = False
        else:
            print('unsupported method, reverting to default method ',method)
            epson_greedy = True
    epson = MAX_EPSON
    init_Q()
    #print(Q_dict)
    for k in range(nr_episodes):
        dealer_cards = []
        player_cards = []       
        init_episode(dealer_cards, player_cards)
        
        play_episode(dealer_cards, player_cards,epson,debugplay)
    
        epson = max(epson*EPSON_DECAY,MIN_EPSON)
        
        if k % 1000 == 0:
            print("\rEpisode {}/{} (epson {}).".format(k, nr_episodes,epson), end="")
            sys.stdout.flush()

    if nr_episodes >= 10:
        visualise_pi()
        visualise_Q()
        
    
    
if __name__ == "__main__":
    main(sys.argv)