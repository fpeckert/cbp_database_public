# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 09:22:35 2020

@author: Anubhav Agarwal
"""

import pandas as pd
import numpy as np
import os
import sys

def unique(l):
    x = np.array(l)
    y = np.unique(x).tolist()
    return y

def stringClean(data):
    data.columns = map(str.lower, data.columns)
    data.columns = data.columns.str.replace('.*siccode.*', 'naics')
    data.naics = data.naics.str.replace('/','\\')
    df_obj = data.select_dtypes(['object'])
    data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    data.loc[data['naics'] == '19--', ['naics']] = '20--'
    data = data.loc[~(data['naics'] == '000000')]

def diff(list1, list2):
    return (list(list(set(list1)-set(list2)) + list(set(list2)-set(list1))))


#yearlist = [str(i) for i in range(1975, 2017)]
yearlist = ['2017']

for year in yearlist:
    orig_stdout = sys.stdout
    suffix = year[2:]
    dirname = os.path.dirname(__file__)
    filename = dirname + '\\' + year + '\\'
    os.chdir(filename)
    f = open('out' + year + 'diff.txt', 'w')
    sys.stdout = f
    if (year <= '1985'):
        co = pd.read_csv('CBP' + year + 'cty')
        st = pd.read_csv('CBP' + year + 'st')
        us = pd.read_csv('CBP' + year + 'us')
    else:
        co = pd.read_csv('cbp' + suffix + 'co.txt')
        st = pd.read_csv('cbp' + suffix + 'st.txt')
        us = pd.read_csv('cbp' + suffix + 'us.txt')
    stringClean(co)
    stringClean(st)
    stringClean(us)
    os.chdir(filename + '\\Cleaned\\')
    naicsFinal = pd.read_csv('cbp' + year + '_ind_ref.csv')
    if 'siccode' in co.columns:
        coSic = co.siccode.tolist()
    else:
        coSic = co.naics.tolist()
    if 'siccode1' in st.columns:
        stSic = st.siccode1.tolist()
    else:
        stSic = st.naics.tolist()
    if 'siccode1' in us.columns:
        usSic = us.siccode1.tolist()
    else:
        usSic = us.naics.tolist()
    naicsFinal = naicsFinal.naics.tolist()
    coSic = unique(coSic)
    stSic = unique(stSic)
    usSic = unique(usSic)
    coDiff = diff(coSic, naicsFinal)
    stDiff = diff(stSic, naicsFinal)
    usDiff = diff(usSic, naicsFinal)
    print("County Dropped Codes:")
    print(coDiff)
    print("State dropped codes:")
    print(stDiff)
    print("US dropped codes:")
    print(usDiff)
    sys.stdout = orig_stdout
    f.close()
    