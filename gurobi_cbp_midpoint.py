#Eckert, Fort, Schott, Yang (2019)
#Corresponding Author: mail@fpeckert.me

##Load Packages
#from gurobipy import *
from gurobipy import *
import cbp
import numpy as np, pandas as pd
import re, sys


model = Model('cbp')

# extract year from the arguments
year = 2016

is_estab = False

if len(sys.argv) > 1:
    year = sys.argv[1]
    if len(sys.argv) > 2:
        is_estab = sys.argv[2] == 'estab'

is_sic = False
if year <= 1997:
    is_sic = True

#Reading in a year's data
national_df = pd.read_csv(root+'/Data Process/'+str(year)+'/us/'+'cbp'+str(year)+'us_edit.csv')
state_df    = pd.read_csv(root+'/Data Process/'+str(year)+'/st/'+'cbp'+str(year)+'st_edit.csv')
county_df   = pd.read_csv(root+'/Data Process/'+str(year)+'/co/'+'cbp'+str(year)+'co_edit.csv')

#rename industry column from sic to naics in sic years.
if is_sic:
    national_df = national_df.rename(index=str, columns={'sic': 'naics'})
    state_df    = state_df.rename(index=str, columns={'sic': 'naics'})
    county_df   = county_df.rename(index=str, columns={'sic': 'naics'})

# find the ref files
industry_ref_file = cbp.refFileName(year)

refpath = root+'/Data Process/'+str(year)+'/ref/'
os.chdir(refpath)

naics_codes       = cbp.newNaicsCodes(industry_ref_file, year)

geo_codes         = cbp.geoCodes(state_df, county_df)


# ##
# Construct tree for NAICS codes
# ##
# determine level function based on which industry code is used
industry_level_function = cbp.naics_level
if is_sic:
    industry_level_function = cbp.sic_level

naics_tree = cbp.preorderTraversalToTree(naics_codes, 'naics', industry_level_function)

# ##
# Construct tree for Geography
# ##
geo_tree = cbp.preorderTraversalToTree(geo_codes, 'geo', cbp.geo_level)

df = cbp.merge_dataframes(national_df, state_df, county_df)



# matrices
ub_matrix = df.pivot(index='ind', columns='geo', values='ub').fillna(0).astype(int)
lb_matrix = df.pivot(index='ind', columns='geo', values='lb').fillna(0).astype(int)

ub_matrix_estab = ub_matrix.copy()
lb_matrix_estab = lb_matrix.copy()

# geo_codes's entries are tuples, which mess up the indexing
# solution: convert the entries to string and remove the space
# because gurobi doesn't like spaces in variable names
geo_codes_str = list(map(lambda x: x.replace(' ', ''), map(str, geo_codes)))


entries = model.addVars(naics_codes, geo_codes_str, name = "Entries")

# add gurobi variables for differences and absolute differences
diffs = model.addVars(naics_codes, geo_codes_str, lb = (-1) * GRB.INFINITY, name = "Diffs")
abs_diffs = model.addVars(naics_codes, geo_codes_str, name = "Abs_Diffs")

if is_estab:
    ub_matrix_estab = df.pivot(index='naics', columns='geo', values='ub_estab').fillna(0).astype(int)
    lb_matrix_estab = df.pivot(index='naics', columns='geo', values='lb_estab').fillna(0).astype(int)

    # Upper bound
    model.addConstrs((entries[naics, geo] <= ub_matrix_estab[geo_codes[geo_index]][naics] for naics in naics_codes for geo_index, geo in enumerate(geo_codes_str)), "ub")
    # Lower bound
    model.addConstrs((entries[naics, geo] >= lb_matrix_estab[geo_codes[geo_index]][naics] for naics in naics_codes for geo_index, geo in enumerate(geo_codes_str)), "lb")
else:
    # Upper bound
    model.addConstrs((entries[naics, geo] <= ub_matrix[geo_codes[geo_index]][naics] for naics in naics_codes for geo_index, geo in enumerate(geo_codes_str)), "ub")
    # Lower bound
    model.addConstrs((entries[naics, geo] >= lb_matrix[geo_codes[geo_index]][naics] for naics in naics_codes for geo_index, geo in enumerate(geo_codes_str)), "lb")

# define diffs and absolute differences
model.addConstrs((diffs[naics, geo] == (entries[naics, geo] - (ub_matrix[geo_codes[geo_index]][naics] + lb_matrix[geo_codes[geo_index]][naics]) / 2.0) for naics in naics_codes for geo_index, geo in enumerate(geo_codes_str)), "difference")
model.addConstrs((abs_diffs[naics, geo] == abs_(diffs[naics, geo]) for naics in naics_codes for geo in geo_codes_str), "absolute_difference")

for geo_index, geo in enumerate(geo_codes_str):
    # print(geo_index)
    for naics_index, naics in enumerate(naics_codes):
        # bounds = (ub_matrix[geo_codes[geo_index]][naics], lb_matrix[geo_codes[geo_index]][naics])

        # # Upper bound
        # model.addConstr((entries[naics, geo] <= bounds[0]), "ub" + naics + geo)
        # model.addConstr((entries[naics, geo] >= bounds[1]), "lb" + naics + geo)

        # model.addConstr((diffs[naics, geo] == (entries[naics, geo] - sum(bounds) / 2.0)), "difference" + naics + geo)
        # model.addConstr((abs_diffs[naics, geo] == abs_(diffs[naics, geo])), "absolute_difference" + naics + geo)

        # Geographical constraints
        # if no children, there is no constraint
        if len(geo_tree[geo_index]['children']) > 0:
            # check whether in reality this cell has children
            children_geo_sum_upper = sum(ub_matrix[geo_codes[child]][naics] for child in geo_tree[geo_index]['children'])
            if children_geo_sum_upper > 0:
                model.addConstr(entries[naics, geo] == sum(entries[naics, geo_codes_str[child]] for child in geo_tree[geo_index]['children']), "Geographical_Constraint" + naics + geo)

        # Industry constraints
        # if no children, there is no constraint
        if len(naics_tree[naics_index]['children']) > 0:
            # check whether this cell has children in reality (in the dataset)
            # if children's upper bound sum is nonzero then there is children in the data
            children_naics_sum_upper = sum(ub_matrix[geo_codes[geo_index]][naics_codes[child]] for child in naics_tree[naics_index]['children'])
            if children_naics_sum_upper > 0:
                # SIC does not have exact hierarchy after level 2. NAICS always has exact hierarchy
                if is_sic and (cbp.sic_level(naics) >= 2):
                    model.addConstr(entries[naics, geo] >= sum(entries[naics_codes[child], geo] for child in naics_tree[naics_index]['children']),  "Industry_Constraint" + naics + geo)
                else:
                    model.addConstr(entries[naics, geo] == sum(entries[naics_codes[child], geo] for child in naics_tree[naics_index]['children']),  "Industry_Constraint" + naics + geo)

# Objective
# obj = entries.sum()
obj = abs_diffs.sum()

# model.setObjective(obj, GRB.MAXIMIZE) # maximize
model.setObjective(obj, GRB.MINIMIZE) # minimize
print('Model created.')


# make the model less sensitive
model.Params.NumericFocus = 1


# model.write("model.lp")

m = model.optimize()

# Write solution to the python variables
for v in model.getVars():
    if v.Varname.split('[')[0] == 'Entries':
        # get naics and geo codes from the variable name
        s = v.Varname.replace(']', '[').split('[')[1]
        naics = s.split(',', 1)[0]
        s = s.split(',', 1)[1]
        geo = tuple(map(int, re.findall('\d+', s)))

        if is_estab:
            # update the matrix
            ub_matrix_estab[geo][naics] = v.X
            lb_matrix_estab[geo][naics] = v.X
        else:
            # update the matrix
            ub_matrix[geo][naics] = v.X
            lb_matrix[geo][naics] = v.X

        # print("%s %f" % (v.Varname, v.X))

# print solution quality statistics
model.printQuality()

# cbp's save function to save the matrices
if is_estab:
    cbp.save(ub_matrix_estab, lb_matrix_estab, year, "_gurobi_midpoint_estab")
else:
    cbp.save(ub_matrix, lb_matrix, year, "_gurobi_midpoint")
