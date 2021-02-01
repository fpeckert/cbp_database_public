# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 00:17:24 2020

@author: Anubhav Agarwal
"""

import os
import dataCleaner as dc
import checkMidpoint as cm
import gurobi_closest_def as gcd
import gurobi_midpoint_def as gmd
import addFlag as af
import addAdjFlag as adjf

year = '1975'
year = os.getenv('SLURM_ARRAY_TASK_ID')
#dc.dataCleaner(year)
midpointSolveable = cm.midpointable(year, '_edit')
if(midpointSolveable):
    print("Midpoint")
    gmd.gurobiMid(year)
else:
    print("Altered")
    gcd.gurobiClosestModel(year)
    adjf.addAdjFlag(year)
