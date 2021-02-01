# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 01:47:13 2021

@author: Anubhav Agarwal
"""

import pandas as pd
import cbp_utils as cbpu
import numpy as np
import sys

year = '1982'
if len(sys.argv) > 1:
    year = sys.argv[1]
suffix = year[2:]

def oldCleaner(data):
    data.columns = map(str.lower, data.columns)
    data.columns = data.columns.str.replace('.*siccode.*', 'naics')
    data.columns = data.columns.str.replace('.*tflag.*', 'empflag')
    data.columns = data.columns.str.replace('.*tempm.*', 'emp')
    data.naics = data.naics.str.replace('/','\\')
    if 'fipscty2' in data.columns:
        data.columns = data.columns.str.replace('fipscty2', "fipscty")
    if data.name == 'co':
        data.loc[((data.emp) % 1000 == 0), ['emp']] = data.loc[((data.emp) % 1000 == 0), ['emp']] / 1000
    data['emp'] = data['emp'].astype(int)
    df_obj = data.select_dtypes(['object'])
    data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    data.loc[data['naics'] == '19--', ['naics']] = '20--'
    if year == '1986':
        data.loc[data['naics'] == '5800', ['naics']] = '5810'
        data.loc[data['naics'] == '1211', ['naics']] = '1210'
    data = data.loc[~(data['naics'] == '000000')]

def naicsOverlap(dList):
    co = dList[0]
    st = dList[1]
    coSic = co.naics.tolist()
    stSic = st.naics.tolist()
    common = list(set.intersection(set(coSic), set(stSic)))
    common.sort()
    return common

def addCodes(usData, costOverlap):
    usSic = usData.naics.tolist()
    toAdd = np.setdiff1d(costOverlap, usSic).tolist()
    for year in toAdd:
        usData = usData.append({'naics': year, 'lb': 0, 'ub': 10000000}, ignore_index = True)
    usData.sort_values(by=['naics'])
    return usData

def finalClean(data, geo, overlap):
    data = cbpu.cbp_clean(data, geo)
    data = data[data['naics'].isin(overlap)]
    if geo == 'st':
        data.drop_duplicates(subset = ['naics', 'fipstate'])
    if geo == 'co':
        data.drop_duplicates(subset = ["fipstate", "fipscty", "naics"])
    if geo == 'us':
        data = addCodes(data, overlap)
        data.drop_duplicates(subset = ['naics'])
    if 'fipstate' in data.columns:
        data.astype({"fipstate" : 'int32'})
        if 'fipscty' in data.columns:
            data.astype({"fipscty" : 'int32'})
            data.sort_values(["fipstate", "fipscty", "naics"], inplace=True)
        else:
            data.sort_values(["fipstate", "naics"], inplace=True)
    else:
        data.sort_values("naics", inplace=True) 
    data.to_csv('cbp' + year + geo + "_edit.csv", index=False)

co = pd.read_csv('CBP' + year + 'cty')
co.name = 'co'
st = pd.read_csv('CBP' + year + 'st')
st.name = 'st'
us = pd.read_csv('CBP' + year + 'us')
us.name = 'us'
files = [co, st, us]
geolist = ["co", "st", "us"]

data = pd.read_csv("CBP" + year + "cty", dtype={'FIPSTATE':str, 'FIPSCTY2':str})
df = data[['FIPSTATE', 'FIPSCTY2']]
df.drop_duplicates(subset=['FIPSTATE', 'FIPSCTY2'], inplace=True)
df = df.replace('"','', regex=True)
df = df.replace(' ','', regex=True)
df = df.replace(',','', regex=True)
df.rename(columns={"FIPSTATE": "fipstate", "FIPSCTY2": "fipscty"}, inplace=True)
df.sort_values(["fipstate", "fipscty"], inplace=True)
df.to_csv('cbp' + year + '_geo_ref.csv', sep='\t', index=False)

for file in files:
    oldCleaner(file)
    
overlap = naicsOverlap(files)
for i in range(3):
    finalClean(files[i], geolist[i], overlap)
    
with open('cbp' + year + '_ind_ref.csv', 'w') as f:
    f.write("naics\n")
    for item in overlap:
        f.write("%s\n" % item)



