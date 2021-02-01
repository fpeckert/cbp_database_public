# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 00:23:57 2020

@author: Anubhav Agarwal
"""

import pandas as pd

def addAdjFlag(year):
    adjDf = pd.read_csv('cbp' + year + '_adjustments.csv')
    codf = pd.read_csv('cbp' + year + 'co_gurobi.csv')
    stdf = pd.read_csv('cbp'+ year + 'st_gurobi.csv')
    usdf = pd.read_csv('cbp' + year + 'us_gurobi.csv')
    adjDf[['fipstate', 'fipscty']] = adjDf.geo.str.split(",", expand = True)
    df_obj = adjDf.select_dtypes(['object'])
    adjDf[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    adjDf['fipstate'] = adjDf['fipstate'].map(lambda x: x.lstrip('('))
    adjDf['fipscty'] = adjDf['fipscty'].map(lambda x: x.rstrip(')'))
    adjDf.drop('geo', inplace = True, axis = 1)
    adjDf.drop('Unnamed: 0', inplace = True, axis = 1)
    adjDf['fipstate'] = pd.to_numeric(adjDf['fipstate'])
    adjDf['fipscty'] = pd.to_numeric(adjDf['fipscty'])
    usadj = adjDf.loc[(adjDf.fipstate == 0)]
    stadj = adjDf.loc[(adjDf.fipscty == 0) & (adjDf.fipstate != 0)]
    coadj = adjDf.loc[(adjDf.fipscty) != 0]
    usadj.drop(['fipstate', 'fipscty'], inplace = True, axis = 1)
    stadj.drop('fipscty', inplace = True, axis = 1)
    usdf = usdf.astype(str)
    usadj = usadj.astype(str)
    stdf = stdf.astype(str)
    stadj = stadj.astype(str)
    codf = codf.astype(str)
    coadj = coadj.astype(str)
    
    uscomb = pd.merge(usdf, usadj, on = 'naics', how = 'left', indicator = 'adjusted')
    uscomb.drop(['ub_y', 'lb_y'], inplace = True, axis = 1)
    uscomb = uscomb.astype({"adjusted" : 'str'})
    uscomb.loc[uscomb['adjusted'] == 'both', ['adjusted']] = '1'
    uscomb.loc[uscomb['adjusted'] == 'left_only', ['adjusted']] = '0'
    uscomb.rename(columns = {'lb_x' : 'lb', 'ub_x' : 'ub'}, inplace = True)
    
    stcomb = pd.merge(stdf, stadj, on = ['naics', 'fipstate'], how = 'left', indicator = 'adjusted')
    stcomb.drop(['ub_y', 'lb_y'], inplace = True, axis = 1)
    stcomb= stcomb.astype({"adjusted" : 'str'})
    stcomb.loc[stcomb['adjusted'] == 'both', ['adjusted']] = '1'
    stcomb.loc[stcomb['adjusted'] == 'left_only', ['adjusted']] = '0'
    stcomb.rename(columns = {'lb_x' : 'lb', 'ub_x' : 'ub'}, inplace = True)
    
    cocomb = pd.merge(codf, coadj, on = ['naics', 'fipstate', 'fipscty'], how = 'left', indicator = 'adjusted')
    cocomb.drop(['ub_y', 'lb_y'], inplace = True, axis = 1)
    cocomb= cocomb.astype({"adjusted" : 'str'})
    cocomb.loc[cocomb['adjusted'] == 'both', ['adjusted']] = '1'
    cocomb.loc[cocomb['adjusted'] == 'left_only', ['adjusted']] = '0'
    cocomb.rename(columns = {'lb_x' : 'lb', 'ub_x' : 'ub'}, inplace = True)
                                
    uscomb.to_csv('cbp' + year + 'us_gurobi.csv', index = False)
    stcomb.to_csv('cbp' + year + 'st_gurobi.csv', index = False)
    cocomb.to_csv('cbp' + year + 'co_gurobi.csv', index = False)