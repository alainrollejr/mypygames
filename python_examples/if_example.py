# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 08:20:00 2018

@author: aro


Gooit een dobbelsteen en print een boodschap als de worp groter is dan 3

if= als
else = anders

"""

import random # allerlei dobbelsteen achtige dingen


alle_dobbelsteen_getallen = (1,2,3,4,5,6) # een zelfgemaakt lijstje  (list)

print('effe checken:' + str(alle_dobbelsteen_getallen)) # lijstje even afdrukken op het scherm


worp = random.choice(alle_dobbelsteen_getallen) # een getal willekeurig kiezen (choice = keus). Perfecte dobbelsteen !

print('worp =' + str(worp)) # even afdrukken om te zien wat de computer koos


if worp > 3:
    print("groter dan 3 !")
elif  worp == 3:
    print("gelijk aan 3 !")
else: # alle ander gevallen 
    print("kleiner dan 3 !")
    


    

