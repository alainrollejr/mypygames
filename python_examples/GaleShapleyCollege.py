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

def main(argv):
    
    parser = argparse.ArgumentParser(description='script dat optimale scholenkeuze simuleert')
    parser.add_argument('-v','--variant', help='1=super random, 2 = school prefereert studenten die voor die school gekozen hebben', required=True)
    parser.add_argument('-p','--path', help='path to aanmeldings_input_matrix.csv', required=True)    
    args = vars(parser.parse_args())
    
    path = args['path']
    
    matrix = pd.read_csv(path)
    
    print(matrix.head())
    
    school_lijst_tmp = list(matrix)
    school_lijst_tmp.remove('kind')
    print(school_lijst_tmp)
    
    school_lijst = []
    quota_lijst = []
    for school in school_lijst_tmp:
        t = re.split('[,=]',school)
        #print(t)
        school_lijst.append(t[0])
        quota_lijst.append(int(t[2]))
        
    print(school_lijst)
    print(quota_lijst)
    
    
    
    
if __name__ == "__main__":
    main(sys.argv)


