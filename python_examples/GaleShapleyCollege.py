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
        
    def __repr__(self):
        return str(self.naam) + " q=" + str(self.quotum) + " lijst =" + str(self.lijst)
    
    def __str__(self):
        return str(self.naam) + " q=" + str(self.quotum) + " lijst =" + str(self.lijst)
    
        
    def add_kind(self, kind):
        self.lijst.append(kind)
        
    def sorteer_lijst(self, methode):
        if methode == 1:
            # totaal random
            random.shuffle(self.lijst)
        elif methode == 2:
            # school heeft lichte voorkeur voor kinderen die deze school een hoge voorkeur gaven
            print("variant nog niet geimplementeerd")
        else:
            print("variant niet gesupporteerd")
    
class kind(object):
    def __init__(self,naam):
        self.naam = naam
        self.lijst  = [] # van scholen
        self.voorkeur  = [] # van scholen
        
    
    def __repr__(self):
        return str(self.naam) + " lijst=" + str(self.lijst) + "voorkeuren=" + str(self.voorkeur)
    
    def __str__(self):
        return str(self.naam) + " lijst=" + str(self.lijst) + "voorkeuren=" + str(self.voorkeur)
    
    def add_school(self,school_naam, voorkeur):
        self.lijst.append(school_naam)
        self.voorkeur.append(voorkeur)
 
 
    def get_school_van_keuze(self, keuze):        
        for index,s in enumerate(self.lijst):
            if self.voorkeur[index] == keuze:
                return s
       

def main(argv):
    
    parser = argparse.ArgumentParser(description='script dat optimale scholenkeuze simuleert')
    parser.add_argument('-v','--variant', help='1=super random, 2 = school prefereert studenten die voor die school gekozen hebben', required=True)
    parser.add_argument('-p','--path', help='path to aanmeldings_input_matrix.csv', required=True)    
    args = vars(parser.parse_args())
    
    path = args['path']
    variant = int(args['variant'])
    
    matrix = pd.read_csv(path)
    
    print(matrix.head())


    """
    haal school info uit input matrix
    """    
    scholen_tmp = list(matrix)
    scholen_tmp.remove('kind')
    print(scholen_tmp)
    
    alle_scholen = []
    for school_naam in scholen_tmp:
        alle_scholen.append(school(naam = school_naam,
                                   quotum = matrix[school_naam].iloc[0]))
 
    print(alle_scholen)
    
    
        
    """
    haal info over kinderen uit input matrix
    """    
    alle_kinderen = []
    for index, row in matrix.iterrows():
        if index > 0: # skip the first row with quota
            print(row["kind"])
            kind_obj = kind(naam = row["kind"])
            
            df = matrix[matrix['kind']==row['kind']]
            nonnull_columns=df.columns[df.notnull().any()]
            
            i = 0
            for c in nonnull_columns:
                if i > 0:
                    kind_obj.add_school(school_naam=str(c), voorkeur = df[c].iloc[0])  
                i +=1
            
            
            alle_kinderen.append(kind_obj)
        
        
    print(alle_kinderen)
        
    
    """
        Gale Shapley algorithme
        
        Step1 : zet alle kinderen op lijst van de school van hun eerste keuze 
    """
    K = 1
    for kind_obj in alle_kinderen:
        voorkeurschool_naam = kind_obj.get_school_van_keuze(K)
        for school_obj in alle_scholen:
            if school_obj.naam == voorkeurschool_naam:
                school_obj.add_kind(kind_obj)
                
    print(alle_scholen)    
      
    for school_obj in alle_scholen:
        school_obj.sorteer_lijst(methode = variant)
        
    print("\n")
    print(alle_scholen)
    
if __name__ == "__main__":
    main(sys.argv)


