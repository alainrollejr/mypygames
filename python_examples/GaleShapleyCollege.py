# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 18:32:45 2018

@author: aro
"""

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
import random    
import re

class school(object):
    def __init__(self,naam,quotum):
        self.naam = naam
        self.quotum = quotum
        self.lijst  = []
    
    def __repr__(self):
        return str(self.naam) + " q=" + str(self.quotum) + " lijst =" + str(self.lijst)
    
    def __str__(self):
        return str(self.naam) + " q=" + str(self.quotum) + " lijst =" + str(self.lijst)

def main(argv):
    
    parser = argparse.ArgumentParser(description='script dat optimale scholenkeuze simuleert')
    parser.add_argument('-v','--variant', help='1=super random, 2 = school prefereert studenten die voor die school gekozen hebben', required=True)
    parser.add_argument('-p','--path', help='path to aanmeldings_input_matrix.csv', required=True)    
    args = vars(parser.parse_args())
    
    path = args['path']
    
    matrix = pd.read_csv(path)
    
    print(matrix.head())
    
    scholen_tmp = list(matrix)
    scholen_tmp.remove('kind')
    print(scholen_tmp)
    
    lijst_van_scholen = []
    for school_naam in scholen_tmp:
        t = re.split('[,=]',school_naam)
        lijst_van_scholen.append(school(naam = t[0], quotum = int(t[2])))
 
    print(lijst_van_scholen)
        
    
    
if __name__ == "__main__":
    main(sys.argv)


