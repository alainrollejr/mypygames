# -*- coding: utf-8 -*-
"""
Simulatie gebaseerd op uitleg ontvangen van stadsbestuur.

Variant 1, weerhouden voor gebruik:        

Naast schoolkeuze en sociale mix (IND/NIND) wordt ook het toevalscriterium gebruikt om leerlingen te ordenen.
Concreet betekent het dat alle leerlingen die voor een bepaalde school hebben aangemeld, 
los van de hoeveelste keuze ook, ad random geordend worden op elke schoollijst waarop ze staan. 
Dat betekent dat elke leerling op basis van toeval een plaats krijgt op de lijst van een school en dat men dus, 
afhankelijk van het aantal beschikbare plaatsen en de na te streven sociale mix, gunstig 
of ongunstig gerangschikt kan staan. Het is dus perfect mogelijk dat een leerling in zijn
tweede keuze gunstig gerangschikt wordt en dat een leerling met zijn eerste keuze 
ongunstig gerangschikt staat op die lijst.
De leerling die gunstig gerangschikt staat met zijn tweede keuze komt natuurlijk
ook in aanmerking om gunstig gerangschikt te worden in zijn eerste keuze. 
Als dat gebeurt dan krijgt hij hiervoor een ticket en wordt hij geschrapt in de gunstige 
rangschikking in zijn tweede keuze. Wordt hij niet gunstig gerangschikt 
in zijn eerste keuze dan krijgt hij een ticket voor zijn tweede keuze 
op basis van zijn gunstige rangschikking daar. DE REGEL IS DAT MEN EEN
 TICKET BEKOMT VOOR DE HOOGSTE SCHOOLKEUZE WAAR MEN GUNSTIG GERANGSCHIKT IS.
Hetzelfde gebeurt met leerlingen die gunstig gerangschikt zouden zijn in hun derde, 
vierde enz schoolkeuzes. 
Zij maken verschillende keren kans om gunstig gerangschikt te worden in 
een hogere schoolkeuze, waarna ze geschrapt worden in hun lagere schoolkeuzes.
 Op die manier blijven dus vooral leerlingen gunstig gerangschikt staan
 op de schoollijst van hun eerste keuze
 
Variant 2, niet weerhouden:
    
Een ander systeem dat in het kader van aanmeldingen in scholen soms gebruikt wordt, 
is dat van de optimalisatie van de eerste schoolkeuze. D.w.z. dat bij de toekenning 
van de tickets de leerlingen die als eerste keuze voor die school gekozen hebben 
voorrang krijgen. Slechts indien er nog plaatsen over zijn komen dan de leerlingen die 
als tweede keuze die school aangeduid hebben in aanmerking. Dit systeem is performant
in een omgeving met weinig capaciteitsproblematiek. Indien er slechts in een enkele 
school gebrek aan capaciteit is, bekomt men dan quasi zeker een ticket voor zijn
tweede of uitzonderlijk derde keuze. D.w.z. dat indien er te weinig plaatsen zouden zijn,
zelfs voor leerlingen met de eerste keuze, men wellicht plaats vindt in een andere hoge schoolkeuze.
Anders is het gesteld met het gebruik van dit systeem in een omgeving met
veel capaciteitsproblematiek (zoals in Gent).
Als een leerling daar in zijn eerste keuze ongunstig gerangschikt wordt
(op de wachtlijst komt), zou hij in aanmerking komen voor de tweede keuze.
Maar aangezien in die tweede keuze iedereen die die school als eerste keuze
 aangeduid heeft voorrang krijgt, is de kans groot dat u ook daar geen plaats meer hebt.
 Erger wordt het nog in de derde keuze, waar iedereen die voor die school koos als
 eerste én tweede keuze voorrang heeft op u, enz … D.w.z. dat
 wanneer u in dit systeem uw eerste schoolkeuze mist door meer vraag dan aanbod,
 u onvermijdelijk in de onderste regionen van de schoolkeuzes uitkomt.
Dit resulteert in een aantal scholen die alleen maar leerlingen van 
eerste keuze hebben en een aantal andere scholen die overwegend leerlingen
 van 4e, 5e, 6e enz schoolkeuzes hebben. Dit is geen prettig vooruitzicht
 voor die scholen en zeker ook niet voor de betrokken leerlingen.
"""
import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
import random


def main(argv):
    
    parser = argparse.ArgumentParser(description='script dat scholenkeuze simuleert')
    parser.add_argument('-v','--variant', help='1=super random, 2 = optimisatie 1ste keuze', required=True)
    parser.add_argument('-t','--total', help='totaal aantal leerlingen dat moet geplaatst worden', required=True)
    parser.add_argument('-c','--capacity', help='totale capaciteit', required=True)
    parser.add_argument('-p','--path', help='path to input.csv', required=True)    
    args = vars(parser.parse_args())
    
    df = pd.read_csv('school_lijst.csv')
    aantal_scholen = len(df.index)
    df['kans dat kind hier naar toe wil']=0.01*df['kans dat kind hier naar toe wil (percent)'].astype(float)
    prob = df['kans dat kind hier naar toe wil'].tolist()
        
    total = int(args['total'])
    capacity = float(args['capacity'])
    variant = int(args['variant'])
    
    print('total '+ str(total) + ' capacity ' + str(capacity) + ' variant ' + str(variant) + ' aantal scholen ' + str(aantal_scholen))
    
    # zet de absolute capaciteit in het dataframe
    tmp = round(0.01*capacity*df['relatieve capaciteit (percent relatief tot totale capaciteit)'].astype(float))
    vrije_plaatsen = tmp.tolist()
    print('vrije plaatsen ' + str(vrije_plaatsen))
    
    school_namen = df['naam (optioneel)'].tolist()
       
    # simuleer de aanmeldingen volgens populariteit aangegeven in school_lijst.csv
    columns = ['kind','1ste keus', '2de keus','3de keus','computer keuze']
    aanmeldingslijst = pd.DataFrame(columns=columns)
    for kind in range(total):
        scholen = np.arange(1, aantal_scholen+1)
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
        
        row=pd.Series([kind,int(k1),int(k2),int(k3),0],columns)
        aanmeldingslijst = aanmeldingslijst.append([row],ignore_index=True)
        
    aanmeldingslijst.to_csv('aanmeldingen.csv')
    
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
    
    """
        nu het eigenlijke selectie algorithme
    """
    
    # lege lijst initialisatie
    lijst_van_wachtlijsten = []
    lijst_weerhouden = []
    for school in np.arange(1, aantal_scholen+1):
        lijst_van_wachtlijsten.append([])
        lijst_weerhouden.append([])
        
    
        
    
    if variant == 1:
        # zet elk kind in wachtrij van elke school vernoemd door dat kind
        for index, row in aanmeldingslijst.iterrows():
            for school in np.arange(1, aantal_scholen+1):
                if (row['1ste keus'] == school) or (row['2de keus'] == school) or (row['3de keus'] == school):
                    lijst_van_wachtlijsten[school-1].append(row['kind'])
        
           
        for school in np.arange(1, aantal_scholen+1):
            print('initiele wachtrij school ' + str(school)+ 
                  ' (aka ' + str(school_namen[school-1]) + ') '+
                  ' telt ' + str(len(lijst_van_wachtlijsten[school-1])) + 
                  ' kinderen' + ' , vrije plaatsen ' + str(vrije_plaatsen[school -1]))
                       
            
            # shuffle de initiele wachtrij            
            random.shuffle(lijst_van_wachtlijsten[school-1])
            print(lijst_van_wachtlijsten[school-1])
                    
            
            
        # loop over alle kinderen
        aantal_die_eerste_keus_kreeg = 0
        aantal_die_tweede_keus_kreeg = 0
        aantal_die_derde_keus_kreeg = 0
        aantal_die_bot_vangt = 0
        
        k1Vect = aanmeldingslijst['1ste keus']
        k2Vect = aanmeldingslijst['2de keus']
        k3Vect = aanmeldingslijst['3de keus']
        for kind in range(total):
            # print('kind '+ str(kind) + ' 1ste keus ' +str(k1Vect[kind]))
            k1 = k1Vect[kind]
            k2 = k2Vect[kind]
            k3 = k3Vect[kind]
            
            n1 = int(vrije_plaatsen[k1 -1])
            n2 = int(vrije_plaatsen[k2 -1])
            n3 = int(vrije_plaatsen[k3 -1])
            
            if kind in lijst_van_wachtlijsten[k1-1][0:n1]: 
                # kind gunstig geplaatst voor school van eerste keus
                # makkelijkst geval. Kind is weerhouden voor 1ste keuze
                aanmeldingslijst['computer keuze'][kind] = k1
                aantal_die_eerste_keus_kreeg += 1
                
                # schrap het kind van alle lagere lijsten
                if kind in lijst_van_wachtlijsten[k2-1]:
                    lijst_van_wachtlijsten[k2-1].remove(kind)
                if kind in lijst_van_wachtlijsten[k3-1]:
                    lijst_van_wachtlijsten[k3-1].remove(kind)
                    
            elif kind in lijst_van_wachtlijsten[k2-1][0:n2]:
                # kind gunstig geplaatst voor school van tweede keuze
                aanmeldingslijst['computer keuze'][kind] = k2
                aantal_die_tweede_keus_kreeg += 1
                
                # schrap het kind van de lager gelegen lijst
                # (het zal nog steeds voorkomen op wachtlijst van hogere lijst)
                if kind in lijst_van_wachtlijsten[k3-1]:
                    lijst_van_wachtlijsten[k3-1].remove(kind)
                    
            elif kind in lijst_van_wachtlijsten[k3-1][0:n3]:
                # kind gunstig geplaatst voor school van derde keuze
                aanmeldingslijst['computer keuze'][kind] = k3 
                aantal_die_derde_keus_kreeg += 1
            else:
                aantal_die_bot_vangt += 1
                    
            
        aanmeldingslijst.to_csv('aanmeldingen.csv')     
        
            
        
        
    elif variant == 2:
        print("variant not supported yet")
    else:
        print("unsupported variant")
        
    # statistieken
    print('aantal_die_eerste_keus_kreeg ' + str(aantal_die_eerste_keus_kreeg))
    print('aantal_die_tweede_keus_kreeg ' + str(aantal_die_tweede_keus_kreeg))
    print('aantal_die_derde_keus_kreeg ' + str(aantal_die_derde_keus_kreeg))
    print('aantal_die_bot_vangt ' + str(aantal_die_bot_vangt))    
    
if __name__ == "__main__":
    main(sys.argv)



    

