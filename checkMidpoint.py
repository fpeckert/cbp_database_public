# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 19:04:20 2020

@author: Anubhav Agarwal
"""

import cbp
import pandas as pd

def midpointable(year, suffix):
    is_sic = False
    if int(year) <= 1997:
        is_sic = True
    
    national_df = pd.read_csv('cbp' + year + 'us' + suffix + '.csv')
    state_df = pd.read_csv('cbp' + year + 'st' + suffix + '.csv')
    county_df = pd.read_csv('cbp' + year + 'co' + suffix + '.csv')
    
    if is_sic:
        national_df = national_df.rename(index=str, columns={'ind': 'naics'})
        state_df = state_df.rename(index=str, columns={'ind': 'naics'})
        county_df = county_df.rename(index=str, columns={'ind': 'naics'})
        
    industry_ref_file = cbp.refFileName(year)
    
    naics_codes = cbp.newNaicsCodes(industry_ref_file, year)
    
    geo_codes = cbp.geoCodes(state_df, county_df)
    
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
    
    
    results_df = cbp.merge_dataframes(national_df, state_df, county_df)
    
    results_df = results_df.rename(index = str, columns = {'ind' : 'naics'})    
    results_df = results_df.drop_duplicates(subset = ['naics', 'geo'])
    
    ub_matrix = results_df.pivot(index='naics', columns='geo', values='ub').fillna(0).astype(int)
    lb_matrix = results_df.pivot(index='naics', columns='geo', values='lb').fillna(0).astype(int)
    
    for geo_index, geo in enumerate(geo_codes): 
        for naics_index, naics in enumerate(naics_codes):
            # does the geo code have children in theory
            if len(geo_tree[geo_index]['children']) != 0:
                children = list(map(lambda x: geo_codes[x], geo_tree[geo_index]['children']))
                # sum of geographical children's lower/upper bounds
                geo_sum_lower = sum(lb_matrix[geo_codes[child]][naics] for child in geo_tree[geo_index]['children'])
                geo_sum_upper = sum(ub_matrix[geo_codes[child]][naics] for child in geo_tree[geo_index]['children'])
    
                # check if the code has children in data
                if geo_sum_upper == 0:
                    continue
    
                if geo_sum_lower > ub_matrix[geo][naics] or geo_sum_upper < lb_matrix[geo][naics]:
                    print('Found error in geo tree at industry code = %s' % naics)
                    print('children sum (lower, upper): ' + str((geo_sum_lower, geo_sum_upper)))
                    print('parent (lower, upper): ' + str((lb_matrix[geo][naics], ub_matrix[geo][naics])))
                    print()
                    print('Parent: %s. Children: %s \n' % (str(geo), children))
                    return False
    
            # check if the geo code has children in theory (in the industry tree)
            if len(naics_tree[naics_index]['children']) != 0:
                children = list(map(lambda x: naics_codes[x], naics_tree[naics_index]['children']))
                # sum of industrial children's lower/upper bounds
                naics_sum_lower = sum(lb_matrix[geo][naics_codes[child]] for child in naics_tree[naics_index]['children'])
                naics_sum_upper = sum(ub_matrix[geo][naics_codes[child]] for child in naics_tree[naics_index]['children'])
                
                # check if the code has children in data
                if naics_sum_upper == 0:
                    continue
                
                if naics_sum_lower > ub_matrix[geo][naics] or naics_sum_upper < lb_matrix[geo][naics]:
                    # sic does not have exact hierarchy after level 2 (inclusive)
                    if is_sic and cbp.sic_level(naics) >= 2 and naics_sum_upper < lb_matrix[geo][naics]:
                        continue
                    
                    # discrepancy
                    print('Found error in industry tree at geoography (fipstate, fipscty) = %s' % str(geo))
                    print('children sum (lower, upper): ' + str((naics_sum_lower, naics_sum_upper)))
                    print('parent (lower, upper): ' + str((lb_matrix[geo][naics], ub_matrix[geo][naics])))
                    print()
                    print('Parent: %s. Children: %s \n' % (naics, children))
                    return False
    return True