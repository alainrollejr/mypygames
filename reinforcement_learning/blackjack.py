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
S = [] # state space
pi = [] # policy
Q = [] # action value function

# episode variables


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
        for c in player_cards:
            if c != 'A':
                sum += c
        if sum <= 10:
            return True
    return False
    
    

def main(argv):
    
    parser = argparse.ArgumentParser(description='MC e-greedy policy iteration on Sutton and Barto Blackjack problem example')
    
    
    parser.add_argument('-m','--method', help='e:  epson greedy, s: start', required=False)
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
    
    for k in range(nr_episodes):
        dealer_cards = []
        player_cards = []       
        init_episode(dealer_cards, player_cards)
    

        print('dealer cards',dealer_cards)
        print('player cards',player_cards)
        print('player has usable ace', has_usable_ace(player_cards))         
    
    
if __name__ == "__main__":
    main(sys.argv)