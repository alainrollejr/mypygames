# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:31:36 2018

@author: AA
"""

import random # allerlei dobbelsteen achtige dingen

mogelijkheden = ('blad','steen','schaar') # een zelfgemaakt lijstje  (list)
 
gamer_keuze = input("blad, steen of schaar ? schrijf hier jouw keuze: ")
computer_keuze = random.choice(mogelijkheden) # een getal willekeurig kiezen (choice = keus). Perfecte dobbelsteen !

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
else:
    print('ongeldige keuze, kijk je spelling na !')