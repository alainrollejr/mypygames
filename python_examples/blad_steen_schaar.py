# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:31:36 2018

@author: AA
"""

import random # allerlei dobbelsteen achtige dingen

mogelijkheden = ('blad','steen','schaar') # een zelfgemaakt lijstje  (list)

gamer_keuze = 'blad'
 
while gamer_keuze != 'stop': #is niet gelijk aan 

    gamer_keuze = input("blad, steen, schaar of stop ? schrijf hier jouw keuze: ")
    
    computer_keuze = random.choice(mogelijkheden) # een getal willekeurig kiezen (choice = keus). Perfecte dobbelsteen !
    
    if gamer_keuze != 'stop':
        print('jouw_keuze =' + str(gamer_keuze)) 
        print('computer_keuze =' + str(computer_keuze)) # even afdrukken om te zien wat de computer koos
    
    
    if gamer_keuze =='steen':
        if computer_keuze =='steen':
            print('gelijkspel')    
        elif computer_keuze == 'blad':
            print('computer wint')
        else: 
            print('jij wint')
    elif gamer_keuze == 'blad':
        if computer_keuze =='steen':
            print('jij wint')    
        elif computer_keuze == 'blad':
            print('gelijk spel')
        else: 
            print('computer wint')    
    elif gamer_keuze == 'schaar':
        if computer_keuze =='steen':
            print('computer wint')    
        elif computer_keuze == 'blad':
            print('jij wint')
        else: 
            print('gelijkspel')   
    elif gamer_keuze == 'stop':
        break # spring uit de lus (of loop)
    else: # middel tegen hacker thierry
        print('ongeldige keuze, kijk je spelling na !')
        
print('tot de volgende keer')