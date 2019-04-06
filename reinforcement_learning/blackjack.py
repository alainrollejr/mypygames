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

S = [] # state space
pi = [] # policy
Q = [] # action value function
Q_dict = {} # dictionary that maps state to Q table index

# episode variables

def init_Q():
    ind = 0
    player_has_usable_ace = True
    
    for player_sum in range(12,22):
        for dealer_shows in range(11): # dealer shows ace has value 0
            if dealer_shows==0:
                dealer_shows_card ='A'
            else:
                dealer_shows_card = str(dealer_shows)
                
            Q.append(STICK)
            Q_dict[(player_has_usable_ace,dealer_shows_card,player_sum)] = ind
            ind += 1
    player_has_usable_ace = False
    for player_sum in range(12,22):
        for dealer_shows in range(11): # dealer shows ace has value 0
            if dealer_shows==0:
                dealer_shows_card ='A'
            else:
                dealer_shows_card = str(dealer_shows)
                
            Q.append(STICK)
            Q_dict[(player_has_usable_ace,dealer_shows_card,player_sum)] = ind
            ind += 1
    

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
    if has_ace(cards) == True:
        sum = 0
        for c in cards:
            if c != 'A':
                sum += c
        if sum <= 10:
            return True
    return False

def card_sum(cards):
    c_sum = 0
    if has_usable_ace(cards) == True:
        for c in cards:
            if c != 'A':
                c_sum += int(c)
            else:
                c_sum += 11
    else:
        for c in cards:
            if c != 'A':
                c_sum += int(c)
            else:
                c_sum += 1
    return c_sum

def player_action(player_cards, dealer_cards):
    c = card_sum(player_cards)
    if c < 12:
        return HIT
    
    index = Q_dict[(has_usable_ace(player_cards),str(dealer_cards[0]),c)]
    return Q[index]
    
        
def play_episode(player_cards, dealer_cards):
    if card_sum(player_cards) > 21:
        return REWARD_BUST
    
    if card_sum(dealer_cards) > 21:
        return REWARD_WIN
    
    
    

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
    
    init_Q()
    print(Q_dict)
    for k in range(nr_episodes):
        dealer_cards = []
        player_cards = []       
        init_episode(dealer_cards, player_cards)
    

        print('dealer cards',dealer_cards)
        print('dealer sum', card_sum(dealer_cards))
        print('player cards',player_cards)
        print('player sum', card_sum(player_cards))
        print('player has usable ace', has_usable_ace(player_cards))         
    
    
if __name__ == "__main__":
    main(sys.argv)