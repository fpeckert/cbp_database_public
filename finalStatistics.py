# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 19:55:56 2020

@author: Anubhav Agarwal
"""

import pandas as pd
import numpy as np
import os
import sys

yearlist = list(range(1975, 2018))
yearlist = list(map(str, yearlist))
orig_stdout = sys.stdout
dirname = os.path.dirname(__file__)
f = open('stats.txt', 'w')
sys.stdout = f

for year in yearlist:
    print("year: " + year)
    suffix = year[2:]
    filename = dirname + '\\' + year + '\\'
    os.chdir(filename)
    folder = dirname + '\\' + year + '\\Final Imputed'
    os.chdir(folder)
    if (os.path.exists('cbp' + year + '_adjustments.csv')):
        adj = pd.read_csv('cbp' + year + '_adjustments.csv')
        length = len(adj)
        lbsum = adj['lb'].sum()
        lbavg = lbsum / length
        ubsum = adj['ub'].sum()
        ubavg = ubsum / length
        print("Adjustments: " + str(length))
        print("Total LB Adjustment: " + str(lbsum))
        print("Total UB Adjustment: " + str(ubsum))
        print("Average lb Adjustment: " + str(lbavg))
        print("Average ub Adjustment: " + str(ubavg))
        print()
    else:
        print("No Adjustments")
        print()

sys.stdout = orig_stdout
f.close()