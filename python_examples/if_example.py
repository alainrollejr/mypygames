# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 08:20:00 2018

@author: aro


Gooit een dobbelsteen en print een boodschap als de worp groter is dan 3

"""

import random # een gereedschapskist vol met dobbelsteen achtige dingen

alle_dobbelsteen_getallen = (1,2,3,4,5,6) # een zelfgemaakt lijstje  

print(str(alle_dobbelsteen_getallen)) # lijstje even afdrukken op het scherm

gooi = random.choice(alle_dobbelsteen_getallen) # een getal willekeurig kiezen (choice = keus). Perfecte dobbelsteen !

print(gooi) # even afdrukken om te zien wat de computer koos

'''
    en nu komt het: "if" = als, "else" = anders
'''
if gooi > 3:
    print("groter dan 3 !")
else:
    print("kleiner dan 3 !")


    

