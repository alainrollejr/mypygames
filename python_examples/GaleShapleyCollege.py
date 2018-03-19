# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 18:32:45 2018

@author: aro
"""

import sys
import argparse
import pandas as pd
import random    
import numpy as np


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
            
    def weerhoud_vrijeplaatsen(self):
        for index,kind_obj in enumerate(self.lijst):
            if index < self.quotum:
                kind_obj.rejected = False 
                kind_obj.toegewezen_school = self.naam
                for k in range(1,4):
                    if self.naam == kind_obj.get_school_van_keuze(k):
                        kind_obj.voorkeur_van_toegewezen_school = k
                
            else:
                print(str(self.naam) + " rejecting " + str(kind_obj.naam))
                kind_obj.rejected = True;
                kind_obj.toegewezen_school = ''
                kind_obj.voorkeur_van_toegewezen_school = 0
                self.lijst.remove(kind_obj)
    
class kind(object):
    def __init__(self,naam):
        self.naam = naam
        self.lijst  = [] # van scholen
        self.voorkeur  = [] # van scholen
        self.rejected = True
        self.voorkeur_van_toegewezen_school = 0
        self.toegewezen_school = ''
        
    
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
            
def print_lijst_status_naar_matrix(alle_kinderen, alle_scholen, csv_naam):
  
    columns_matrix = ['kind']
    for school_obj in alle_scholen:
        columns_matrix.append(str(school_obj.naam))
    
       
    # eerste rij is speciale rij met vrije plaatsen 
    matrix = pd.DataFrame(columns=columns_matrix)
      
    matrix_row_list = ['vrije plaatsen']
    for school_obj in alle_scholen:
        matrix_row_list.append(str(int(school_obj.quotum)))        
        
    matrix_row = pd.Series(matrix_row_list,columns_matrix)
    matrix = matrix.append([matrix_row],ignore_index=True)
    
    
    for kind_obj in alle_kinderen:
        matrix_row_list = [kind_obj.naam]
        
        for school_obj in alle_scholen:
            if school_obj.naam == kind_obj.toegewezen_school:
                matrix_row_list.append(str(kind_obj.voorkeur_van_toegewezen_school))
            else:
                matrix_row_list.append(np.NaN)
        
        matrix_row = pd.Series(matrix_row_list,columns_matrix)
        matrix = matrix.append([matrix_row],ignore_index=True)
        
    matrix.to_csv(csv_naam, index=False)

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
    
    
    alle_scholen = []
    for school_naam in scholen_tmp:
        alle_scholen.append(school(naam = school_naam,
                                   quotum = matrix[school_naam].iloc[0]))
 
    #print(alle_scholen)
    
    
        
    """
    haal info over kinderen uit input matrix
    """    
    alle_kinderen = []
    for index, row in matrix.iterrows():
        if index > 0: # skip the first row with quota            
            kind_obj = kind(naam = row["kind"])
            
            df = matrix[matrix['kind']==row['kind']]
            nonnull_columns=df.columns[df.notnull().any()]
            
            i = 0
            for c in nonnull_columns:
                if i > 0:
                    kind_obj.add_school(school_naam=str(c), voorkeur = df[c].iloc[0])  
                i +=1
            
            
            alle_kinderen.append(kind_obj)
        
        
    #print(alle_kinderen)
        
    
    """
        Gale Shapley algorithme
    """
    
    K = 1
    stop = False
    
    while stop == False:
    
        """
            voeg kinderen toe aan lijst van school van hune K-de keuze
        """
        for kind_obj in alle_kinderen:
            if kind_obj.rejected == True:
                voorkeurschool_naam = kind_obj.get_school_van_keuze(K)
                for school_obj in alle_scholen:
                    if school_obj.naam == voorkeurschool_naam:
                        school_obj.add_kind(kind_obj)
                        
        #print(alle_scholen)    
          
        """
            rangschik en weerhoud enkel toegelaten aantal (vrije plaatsen)
        """
        for school_obj in alle_scholen:
            school_obj.sorteer_lijst(methode = variant)
            school_obj.weerhoud_vrijeplaatsen()
            
        if K == 3:
            stop = True
        else:
            K +=1 
        
    print_lijst_status_naar_matrix(alle_kinderen, alle_scholen, 'output_matrix.csv')
        
    #print("\n")
    #print(alle_scholen)
    
    """
        statistieken
    """
    percent_kreeg_eerste_keus = 0
    percent_kreeg_tweede_keus = 0
    percent_kreeg_derde_keus = 0
    percent_kreeg_niks = 0
    
    for kind_obj in alle_kinderen:
        if kind_obj.voorkeur_van_toegewezen_school == 1:
            percent_kreeg_eerste_keus += 1
        elif kind_obj.voorkeur_van_toegewezen_school == 2:
            percent_kreeg_tweede_keus += 1
        elif kind_obj.voorkeur_van_toegewezen_school == 3:
            percent_kreeg_derde_keus += 1
        else:
            percent_kreeg_niks += 1
            
    percent_kreeg_eerste_keus = 100.0 * float(percent_kreeg_eerste_keus)/len(alle_kinderen)
    percent_kreeg_tweede_keus = 100.0 * float(percent_kreeg_tweede_keus)/len(alle_kinderen)
    percent_kreeg_derde_keus = 100.0 * float(percent_kreeg_derde_keus)/len(alle_kinderen)
    percent_kreeg_niks = 100.0 * float(percent_kreeg_niks)/len(alle_kinderen)
    
    print("resultaat:")
    print("-----------")
    print("1ste keus: " + str(percent_kreeg_eerste_keus))
    print("2de keus: " + str(percent_kreeg_tweede_keus))
    print("3de keus: " + str(percent_kreeg_derde_keus))
    print("niks: " + str(percent_kreeg_niks))
    
if __name__ == "__main__":
    main(sys.argv)


