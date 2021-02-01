# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 17:31:19 2019

@author: Anubhav Agarwal
"""

import pandas as pd
import cbp_utils as cbpu
import numpy as np

def dataCleaner(yearFull):
    year = yearFull[2:]
    geolist = ["co", "st", "us"]
    for geo in geolist:
        fileName = "cbp" + year + geo + ".txt"
        data = pd.read_csv(fileName)
        data.columns = map(str.lower, data.columns)
        data = cbpu.cbp_clean(data, geo)
        data = cbpu.cbp_drop(data, year, geo, cbpu.cbp_change_code)
        data.to_csv('cbp' + yearFull + geo + "_edit.csv")
    
    
    indDrawFile = "cbp" + yearFull + "co_edit.csv"
    indData = pd.read_csv(indDrawFile)
    indData.columns = map(str.lower, indData.columns)
    if 'sic' in indData.columns:
        indData = indData.rename(columns={"sic": "naics"})
        
    
    naicsList = indData['naics'].tolist()
    x = np.array(naicsList)
    y = np.unique(x).tolist()
    
    with open('cbp' + yearFull + '_ind_ref.csv', 'w') as f:
        f.write("naics\n")
        for item in y:
            f.write("%s\n" % item)
            
    data1 = []
    data2 = []
    with open('cbp' + year + 'co.txt', 'rt') as myFile:
        for myLine in myFile:
            data1.append(str(myLine[1:3]))
            data2.append(str(myLine[6:9]))
        
        df1 = pd.DataFrame(data1, columns=['fipstate'])
        df2 = pd.DataFrame(data2, columns=['fipscty'])
        df = pd.concat([df1, df2], axis=1)
        df.drop_duplicates(subset=['fipstate', 'fipscty'], inplace=True)
        df = df.replace('"','', regex=True)
        df = df.replace(' ','', regex=True)
        df = df.replace(',','', regex=True)
        df = df.drop(df.index[0])
        df.to_csv('cbp' + yearFull + '_geo_ref.csv', sep='\t', index=False)
            
