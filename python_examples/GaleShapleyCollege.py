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
        self.lijst  = [] # van studenten
        self.voorkeur  = []  # van studenten
    
    def __repr__(self):
        return str(self.naam) + " q=" + str(self.quotum) + " lijst =" + str(self.lijst)
    
    def __str__(self):
        return str(self.naam) + " q=" + str(self.quotum) + " lijst =" + str(self.lijst)
    
class kind(object):
    def __init__(self,naam):
        self.naam = naam
        self.lijst  = [] # van scholen
        self.voorkeur  = [] # van scholen
        
    
    def __repr__(self):
        return str(self.naam) + " lijst=" + str(self.lijst) 
    
    def __str__(self):
        return str(self.naam) + " lijst=" + str(self.lijst)
    
    def add_school(school_naam, voorkeur):
        self.lijst.append(school_naam)
        self.voorkeur.append(voorkeur)
        

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
    
    alle_scholen = []
    for school_naam in scholen_tmp:
        alle_scholen.append(school(naam = school_naam,
                                   quotum = matrix[school_naam].iloc[0]))
 
    print(alle_scholen)
    
    alle_kinderen = []
    for index, row in matrix.iterrows():
        if index > 0: # skip the first row with quota
            print(row["kind"])
            kind_obj = kind(naam = row["kind"])
            
            df = matrix[matrix['kind']==row['kind']]
            nonnull_columns=df.columns[df.notnull().any()]
            
                       
            
            print(df[nonnull_columns])
            
            i = 0
            for c in nonnull_columns:
                if i > 0:
                    print(c)
                    print(df[c])
#                    kind_obj.add_school(str(c), df[c]) # deze lookup van voorkeur werkt nog niet 
                i +=1
            
            
            alle_kinderen.append(kind_obj)
        
        
    print(alle_kinderen)
        
    
    
        
    
    
if __name__ == "__main__":
    main(sys.argv)


