#Eckert, Fort, Schott, Yang (2019)
#Corresponding Author: mail@fpeckert.me

##Load Packages
import numpy as np, pandas as pd
import re, sys
import fnmatch
import os

##Define Paths
root = "/Users/fpeckert/Desktop/CBP Project Final"
git = "/Users/fpeckert/github/cbp_final/codes"
sys.path.append(git)
sys.path.append(root)

##Import Own Packages
import cbp_utils

##Code to prepare CBP data
geolist = ['co','st','us']

# Using for loop
for year in range(1977, 2017):
    for geo in geolist:

        yl = 'cbp'+str(year)+geo

        data = pd.read_csv(root+"/Data Input"+'/'+str(year)+'/'+geo+'/'+yl+'.txt')

        data = cbp_utils.cbp_clean(data,geo)

        data = cbp_utils.cbp_drop(data, year, geo, cbp_utils.cbp_change_code)

        data.to_csv(root+"/Data Process"+'/'+str(year)+'/'+geo+'/'+yl+'_edit.csv',index=False)

        print(str(year)+':'+geo+'--done!')


##Code to prepare industry and geo reference files
for year in range(1977, 2017):
    os.chdir(root+'/Data Input/'+str(year)+'/ref')
    data = []
    data1 = []
    data2 = []

    for file in os.listdir('.'):
        if fnmatch.fnmatchcase(file, '*sic*'):
            with open (file, 'rt') as myfile:  # Open file lorem.txt for reading text
                for myline in myfile:                 # For each line, read it to a string
                    data.append(str(myline[0:4]))

                df = pd.DataFrame(data, columns=['ind'])
                #df = df.drop(df.index[0])
                df = df.replace('"','')
                df = df.replace("  ","")
                df.to_csv(root+"/Data Process"+'/'+str(year)+'/ref/ind_ref_'+str(year)+'.csv', sep='\t',index=False)

        elif fnmatch.fnmatchcase(file, '*naics*'):
            with open (file, 'rt') as myfile:  # Open file lorem.txt for reading text
                for myline in myfile:                 # For each line, read it to a string
                    data.append(str(myline[0:6]))

                df = pd.DataFrame(data, columns=['ind'])
                df = df.replace('"','', regex=True)
                df = df.replace(' ','', regex=True)
                df = df[df.ind != 'NAICS']
                df.to_csv(root+"/Data Process"+'/'+str(year)+'/ref/ind_ref_'+str(year)+'.csv', sep='\t',index=False)

        elif fnmatch.fnmatchcase(file, '*geo*'):
            with open (file, 'rt') as myfile:  # Open file lorem.txt for reading text
                for myline in myfile:                 # For each line, read it to a string
                    data1.append(str(myline[1:3]))
                    data2.append(str(myline[6:9]))

                df1 = pd.DataFrame(data1, columns=['fipstate'])
                df2 = pd.DataFrame(data2, columns=['fipstate'])
                df = pd.concat([df1, df2], axis=1)
                df = df.replace('"','', regex=True)
                df = df.replace(' ','', regex=True)
                df = df.replace(',','', regex=True)
                df = df.drop(df.index[0])
                df.to_csv(root+"/Data Process"+'/'+str(year)+'/ref/geo_ref_'+str(year)+'.csv', sep='\t',index=False)


# #Aux Code to Rename Files/Folders quickly
# geolist = ['co','st','us']
#
# for year in range(1977, 2017):
#         for geo in geolist:
#             os.chdir(root+'/Data Process/'+str(year)+'/'+ref+'/')
#
#             for file in os.listdir('.'):
#                 if fnmatch.fnmatchcase(file, '*cbp*'):
#                     os.remove(file)

import numpy as np, pandas as pd
import re, sys
import fnmatch
import os
import shutil

##Define Paths
root = "/Users/fpeckert/Desktop/CBP Project Final"
git = "/Users/fpeckert/github/cbp_final/codes"
sys.path.append(git)
sys.path.append(root)

geolist = ['co','st','us']

os.chdir(root+'/Data Input Website/')

for year in range(1977, 2017):
    shutil.make_archive('efsy_cbp_raw_'+str(year), 'zip', str(year))






# geolist = ['co','st','us']
#
# for year in range(1977, 2017):
#         for geo in geolist:
#             os.chdir(root+'/Data Input/'+str(year)+'/'+geo+'/')
#
#             for file in os.listdir('.'):
#                 if fnmatch.fnmatchcase(file, '*cbp*'):
#                     os.rename(file,"cbp"+str(year)+geo+".txt")
