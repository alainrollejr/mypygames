# -*- coding: utf-8 -*-
"""
genereert een inschrijvingslijst op basis van 
een csv die de scholen opsomt alsook hun populariteit en capaciteit
"""

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
import random    


def main(argv):
    
    parser = argparse.ArgumentParser(description='script dat scholenkeuze simuleert')
    parser.add_argument('-t','--total', help='totaal aantal leerlingen dat moet geplaatst worden', required=True)
    parser.add_argument('-c','--capacity', help='totale capaciteit', required=True)
    parser.add_argument('-p','--path', help='path naar scholen lijst (.csv file)', required=True)    
    args = vars(parser.parse_args())
    
    path = args['path']
    
    df = pd.read_csv(path)
    aantal_scholen = len(df.index)
    df['kans dat kind hier naar toe wil']=0.01*df['kans dat kind hier naar toe wil (percent)'].astype(float)
    prob = df['kans dat kind hier naar toe wil'].tolist()
        
    total = int(args['total'])
    capacity = float(args['capacity'])
    
    
    print('total '+ str(total) + ' capacity ' + str(capacity)  + ' aantal scholen ' + str(aantal_scholen))
    
    # zet de absolute capaciteit in het dataframe
    tmp = round(0.01*capacity*df['relatieve capaciteit (percent relatief tot totale capaciteit)'].astype(float))
    vrije_plaatsen = tmp.tolist()
    print('vrije plaatsen ' + str(vrije_plaatsen))
    
    school_namen = df['naam (optioneel)'].tolist()
    
    ind = 0
    columns_matrix = ['kind']
    for school in school_namen:
        columns_matrix.append(str(school) + ' (q=' + str(int(vrije_plaatsen[ind]))+')')
        ind += 1
    
    print(columns_matrix)
    
    # simuleer de aanmeldingen volgens populariteit aangegeven in school_lijst.csv
    columns = ['kind','1ste keus', '2de keus','3de keus','computer keuze']
    aanmeldingslijst = pd.DataFrame(columns=columns)
    aanmeldingsmatrix = pd.DataFrame(columns=columns_matrix)
    for kind in range(total):
        scholen = np.arange(0, aantal_scholen)
        prob_tmp = copy.deepcopy(prob)        
        k1 = np.random.choice(scholen, p=prob_tmp)
        
        
        # eerste keus gemaakt, verwijder uit lijst en hernormaliseer populariteit
        index = scholen.tolist().index(k1)              
        scholen=np.delete(scholen,index)        
        prob_tot = 1.0 - prob_tmp[index]       
        del prob_tmp[index]       
        i=0
        for p in prob_tmp:
            prob_tmp[i] = p/prob_tot
            i += 1
        
        
        k2 = np.random.choice(scholen, p=prob_tmp)     
        
        # tweede keus gemaakt, verwijder uit lijst en hernormaliseer populariteit
        index = scholen.tolist().index(k2)              
        scholen=np.delete(scholen,index)        
        prob_tot = 1.0 - prob_tmp[index]       
        del prob_tmp[index]       
        i=0
        for p in prob_tmp:
            prob_tmp[i] = p/prob_tot
            i += 1
        
        k3 = np.random.choice(scholen, p=prob_tmp)
        
        matrix_row_list = [str(kind)]
        ind = 0
        for school in school_namen:
            if ind == k1:
                matrix_row_list.append(1)
            elif ind == k2:
                matrix_row_list.append(2)
            elif ind == k3:
                matrix_row_list.append(3)
            else:
                matrix_row_list.append(' ')
            ind +=1 
        
        row=pd.Series([kind,int(k1),int(k2),int(k3),-1],columns) # - 1 betekent nog geen computer keus
        matrix_row = pd.Series(matrix_row_list,columns_matrix)
        aanmeldingsmatrix = aanmeldingsmatrix.append([matrix_row],ignore_index=True)
        aanmeldingslijst = aanmeldingslijst.append([row],ignore_index=True)
        
    aanmeldingslijst.to_csv('aanmeldingen_input.csv')
    aanmeldingsmatrix.to_csv('aanmeldings_input_matrix.csv')
    
    # visualiseer keuzes
    aanmeldingslijst['1ste keus'] = aanmeldingslijst['1ste keus'].astype(int)    
    aanmeldingslijst.hist(column='1ste keus', bins=2*aantal_scholen+1)
    plt.title('histogram 1ste keus')
    plt.xlabel('school')
    plt.ylabel('aantal in 1ste keus')
    plt.show()
    
    aanmeldingslijst['2de keus'] = aanmeldingslijst['2de keus'].astype(int)    
    aanmeldingslijst.hist(column='2de keus', bins=2*aantal_scholen+1)
    plt.title('histogram 2de keus')
    plt.xlabel('school')
    plt.ylabel('aantal in 2de keus')
    plt.show()
    
    aanmeldingslijst['3de keus'] = aanmeldingslijst['3de keus'].astype(int)    
    aanmeldingslijst.hist(column='3de keus', bins=2*aantal_scholen+1)
    plt.title('histogram 3de keus')
    plt.xlabel('school')
    plt.ylabel('aantal in 3de keus')
    plt.show()
    
       
    
    
    
if __name__ == "__main__":
    main(sys.argv)



    

