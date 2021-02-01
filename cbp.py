#Eckert, Fort, Schott, Yang (2019)

import pandas as pd
from ast import literal_eval
import sys

'''
This method takes in a preorder traversal of the tree of codes (which could be
NAICS or geographic) and returns a list of dictionaries whose entries
identify the type of code in the node (naics or geo), its code, and its children.

The method takes in three inputs:
1. The tree of codes (which could be NAICS or geographic). The tree should
    be given as a preorder traversal
2. A name for the codes: Either 'naics' or 'geo'
3. A level function that, given a code, determines the level of the code
    in the directed tree (The level of a node in a directed tree is defined
    as 1 + number of edge between the root and the node.).

Outputs dicts -- a list whose entries have the following structure:
tree[index in the preorder traversal] =
{
  'name': 'naics' OR 'geo'
  'code': code,
  'children': a list of indices of its children in the tree
}
'''
def preorderTraversalToTree(preorder_traversal, name, level_function):
    dicts=[]
    # lineage = [0, index-first-parent, index-second-parent, ....]
    lineage = []

    for index in range(len(preorder_traversal)):
        code = preorder_traversal[index]

        # create this code's dictionary
        code_dict = {}
        code_dict['name'] = name
        code_dict[name] = code
        code_dict['children'] = []

        # find its parent and update the lineage
        level = level_function(code)
        while(len(lineage) >= level and len(lineage) > 0):
            lineage.pop()

        if len(lineage) > 0:
            parents_dictionary = dicts[lineage[-1]]
            parents_dictionary['children'].append(index)

        lineage.append(index)
        dicts.append(code_dict)

    return dicts

# Assumes SIC
def findCorrectionsToTypos(big_df, typos, year, ref_file_name):
    industry_codes = newNaicsCodes(ref_file_name, year)
    industry_tree = preorderTraversalToTree(industry_codes, 'sic', sic_level)

    for typo in typos:
        possible_codes = generatePossibleCodes(typo, year, ref_file_name)

        # numbers = numberTimesCodeOccurs(typo, year, 0, 0)
        # print('\nTypo %s appears %s times in the dataset [national, state, county].' % (typo, numbers))

        # for all occurrences of the typo, find codes that will fit the industrial
        # tree of that occurence
        for index, row in big_df[big_df.sic == typo].iterrows():
            st_id = row.fipstate
            co_id = row.fipscty

            neighborhood = big_df[(big_df.fipstate == st_id) & (big_df.fipscty == co_id)]

            for code in possible_codes:
                index_possible_code = industry_codes.index(code)

                for index_parent, row_parent in neighborhood.iterrows():
                    if row_parent.sic in industry_codes:
                        index_in_codes = industry_codes.index(row_parent.sic)
                        if index_possible_code in industry_tree[index_in_codes]['children']:
                            print('Found correct code for fipstate %d, fipscty %d, code %s. (possible) right code %s and parent %s' % (st_id, co_id, typo, code, row_parent.sic))
                            # print(row_parent.naics)

                            year_before = str(int(year) - 1); year_after = str(int(year) + 1)
                            print('At the same location, the code %s appears %s times in previous year datasets and %s times in next year datasets\n' % (code, numberTimesCodeOccurs(code, year_before, st_id, co_id), numberTimesCodeOccurs(code, year_after, st_id, co_id)) )
    print('')

def generatePossibleCodes(code, year, ref_file_name):
    industry_codes = newNaicsCodes(ref_file_name, year)
    possible_codes = []

    chars = list(range(10))

    for index in range(4):
        for c in chars:
            new_code = code[:index] + str(c) + code[index+1:]
            if (new_code in industry_codes) and (new_code not in possible_codes):
                possible_codes.append(new_code)

    new_code = code[:3] + '\\'
    if new_code in industry_codes:
        possible_codes.append(new_code)

    return possible_codes

def checkNoTimesCodeOccurs(code, year, us, st, co):
    numbers = [us[us.sic == code].sic.size, st[st.sic == code].sic.size, co[co.sic == code].sic.size]
    if numbers[0] > 0 and numbers[1] > 0 and numbers[2] > 0:
        return False

    return ((st[st.sic==code].sic.size <= 5) and (co[co.sic==code].sic.size <= 5))

def numberTimesCodeOccurs(code, year, st_id, co_id):
    us = pd.read_csv('cbp' + year + 'us_edit.csv')
    st = pd.read_csv('cbp' + year + 'st_edit.csv')
    co = pd.read_csv('cbp' + year + 'co_edit.csv')

    big_df = merge_dataframes(us, st, co)

    return big_df[(big_df.fipstate == st_id) & (big_df.fipscty == co_id) & (big_df.sic == code)].index.size

    # if int(year) <= 1997:
    #     return ((st[st.sic==code].sic.size <= 5) and (co[co.sic==code].sic.size <= 5))
    # else:
    #     return ((st[st.naics==code].naics.size <= 5) and (co[co.naics==code].naics.size <= 5))

def typos(year, national_file, state_file, county_file, ref_file_name):
    industry_codes = newNaicsCodes(ref_file_name, year)

    industry_codes_in_dataset = []

    if int(year) <= 1997:
        industry_codes_in_dataset = list(national_file.sic.drop_duplicates()) + list(state_file.sic.drop_duplicates()) + list(county_file.sic.drop_duplicates())
    else:
        industry_codes_in_dataset = list(national_file.sic.drop_duplicates()) + list(state_file.naics.drop_duplicates()) + list(county_file.naics.drop_duplicates())

    # find the codes that are in the datasets but not in the ref files
    typos = list(filter(lambda x: x not in industry_codes, industry_codes_in_dataset))

    # remove codes that appear in every dataset (national, state and county)
    typos = list(filter(lambda x: checkNoTimesCodeOccurs(x, year, national_file, state_file, county_file), typos))

    # drop duplicates
    typos = list(set(typos))

    return typos


def sic_level(code):
    if code == '----':
        return 1
    if '-' in code:
        return 2
    if code[3] == '\\':
        return 3
    if code[3] == '/':
        return 3
    if code[2:4] == '00':
        return 3
    if code[3] == '0':
        return 4
    return 5

# The level function for naics
def naics_level(code):
    # all industries
    if code ==  '------':
        return 1

    return sum(a.isdigit() for a in code)

# level function for geo
def geo_level(code):
    # national
    if code[0] == 0:
        return 1

    # state
    if code[1] == 0:
        return 2

    # county
    return 3

def refFileName(year):
    return "cbp" + year + "_ind_ref.csv"

    # names = {
    #     1980: 'sic80.txt',
    #     1981: 'sic81.txt',
    #     1982: 'sic82.txt',
    #     1983: 'sic83.txt',
    #     1984: 'sic84.txt',
    #     1985: 'sic85.txt',
    #     1986: 'sic86_87.txt',
    #     1987: 'sic86_87.txt',
    #     1988: 'sic88_97.txt',
    #     1989: 'sic88_97.txt',
    #     1990: 'sic88_97.txt',
    #     1991: 'sic88_97.txt',
    #     1992: 'sic88_97.txt',
    #     1993: 'sic88_97.txt',
    #     1994: 'sic88_97.txt',
    #     1995: 'sic88_97.txt',
    #     1996: 'sic88_97.txt',
    #     1997: 'sic88_97.txt',
    #     1998: 'naics03.txt',
    #     1999: 'naics03.txt',
    #     2000: 'naics03.txt',
    #     2001: 'naics03.txt',
    #     2002: 'naics03.txt',
    #     2003: 'naics2002.txt',
    #     2004: 'naics2002.txt',
    #     2005: 'naics2002.txt',
    #     2006: 'naics2002.txt',
    #     2007: 'naics2002.txt',
    #     2008: 'naics2008.txt',
    #     2009: 'naics2009.txt',
    #     2010: 'naics2010.txt',
    #     2011: 'naics2011.txt',
    #     2012: 'naics2012.txt',
    #     2013: 'naics2012.txt',
    #     2014: 'naics2012.txt',
    #     2015: 'naics2012.txt',
    #     2016: 'naics2012.txt'
    # }
    # return names[int(year)]

def newNaicsCodes(ref_file, year):
    refs = pd.read_csv(ref_file)
    return list(refs.naics)

# produces a list of naics/sic codes that are ordered like a
# preorder tree traversal. takes in the reference file
# industry reference file's NAICS or SIC column are preordered
def naicsCodes(ref_file_name, year, use=''):
    naics_codes = []
    if int(year) <= 1997:
        if int(year) >= 1988:
            with open(ref_file_name, 'r') as f:
                naics_codes = [line.split(None, 1)[0] for line in f]
        elif int(year) >= 1986:
            with open(ref_file_name, 'r') as f:
                naics_codes = [line.split(None, 1)[0] for line in f]
            naics_codes = naics_codes[1:] # the first one is 'SIC', so remove that one
        elif int(year) >= 1980:
            with open(ref_file_name, 'r') as f:
                naics_codes = [line[0:4] for line in f] # first 4 chars are the code
    else:
        if int(year) <= 2011:
            with open(ref_file_name, 'r') as f:
                naics_codes = [line.split(None, 1)[0] for line in f]
            # remove the first element, which is 'NAICS'
            naics_codes = naics_codes[1:]
        else:
            naics_codes = list(pd.read_csv(ref_file_name).NAICS)

    if use != 'typos':
        # some codes are unused. if you add them to the naics codes, then you
        # have KeyError problems later. so compare them with the national_df
        national_df = pd.read_csv('cbp' + year + 'us_edit.csv')
        real_naics_codes = []
        if int(year) <= 1997:
            real_naics_codes = list(national_df['sic'])
        else:
            real_naics_codes = list(national_df['naics'])

        # have to check these codes are actually used in the dataset
        naics_codes = list(filter(lambda x: x in real_naics_codes, naics_codes))

    # drop duplicated codes but keep order
    return sorted(set(naics_codes))

def geoCodes(state_df, county_df):
    # Create a preorder traversal of the geo tree
    # in list geo_codes
    states = state_df.drop_duplicates(['fipstate'])[['fipstate']].values.tolist()
    counties = county_df.drop_duplicates(['fipstate', 'fipscty'])[['fipstate','fipscty']]
    geo_codes = [(0,0)]
    for state in states:
        state = state[0]
        geo_codes.append((state, 0))
        for county in list(counties[counties.fipstate == state].fipscty):
            geo_codes.append((state, county))

    return geo_codes

def merge_dataframes(national_df, state_df, county_df):
    state_df['fipscty'] = 0
    national_df['fipscty'] = 0
    national_df['fipstate'] = 0
    df = pd.concat([national_df,state_df,county_df], sort=True)
    df['geo'] = list(zip(df.fipstate, df.fipscty))
    return df

# This function submits a query to the data frame and returns a pandas series
# entry is a dictionary with 'geo' representing the geo code (fipstate or 0, fipscty or 0)
# and 'naics' representing the naics code
# It chooses the data frame to search (national, state or county)
# based on the length of the geography argument
def read_df(entry, ub, lb):
    geo = entry['geo']
    naics = entry['naics']
    return (ub[geo][naics], lb[geo][naics])

# write updates the database. it takes in
# 1. the element to be updated (which is a python
#   dictionary that includes geo and naics codes for the element)
# 2. bound to be updated
# 3. the new value for the bound
def write_df(entry, bound, new_value, ub, lb):
    geo = entry['geo']
    naics = entry['naics']

    if bound == 'ub':
        ub[geo][naics] = new_value
    elif bound == 'lb':
        lb[geo][naics] = new_value

    return (ub, lb)

# merges two python dictionaries
def merge_dict(x,y): return {**x, **y}

# checks if two lists of pandas dataframes contain equivalent data frames
def equalListDataFrames(list1, list2):
    for index in range(len(list1)):
        if list1[index].equals(list2[index]) == False:
            return False
    return True

# take str of tuple and return the tuple
def strToTuple(tuple_str):
    tuple_list = tuple_str.replace('(',')').replace(')',',').split(',')
    tuple_list = list(filter(lambda x: x!='', tuple_list))
    return (int(tuple_list[0]), int(tuple_list[1]))

def splitBigDataFrame(big_df, year):
    # from 'geo' create 'fipstate' and 'fipscty'
    big_df[['fipstate', 'fipscty']] = pd.DataFrame(big_df['geo'].tolist(), index = big_df.index)
    big_df = big_df.drop(['geo'], axis = 1)
    big_df = big_df[['naics', 'fipstate', 'fipscty', 'ub', 'lb']]

    # pull national df from big df
    us = big_df.loc[(big_df['fipstate'] == 0)]
    # drop unnecessary columns
    us = us[['naics', 'lb', 'ub']]

    # pull state df from big df and merge missing values
    st = big_df.loc[(big_df['fipstate'] != 0) & (big_df['fipscty'] == 0)]

    original_st = pd.read_csv('cbp' + year + 'st_edit.csv')
    original_st = original_st.rename(index=str, columns={'ind': 'naics'})
    original_st['fipscty'] = 0

    st = pd.merge(st, original_st, on=['naics', 'fipstate', 'fipscty'], how='outer').fillna(0)
    # rename columns
    st = st.rename(index=str, columns={"ub_x": "ub", "lb_x": "lb"})
    # change dtype from float to int
    st.ub = st.ub.astype(int)
    st.lb = st.lb.astype(int)
    # drop unnecessary columns like fipscty
    st = st[['fipstate', 'naics', 'lb', 'ub']]
    st = st.sort_values(by=['fipstate'])

    # oull county df from big df and merge missing values
    co = big_df.loc[(big_df['fipstate'] != 0) & (big_df['fipscty'] != 0)]

    original_co = pd.read_csv('cbp' + year + 'co_edit.csv')
    original_co = original_co.rename(index=str, columns={'ind': 'naics'})

    co = pd.merge(co, original_co, on=['naics', 'fipstate', 'fipscty'], how='outer').fillna(0)
    # rename columns
    co = co.rename(index=str, columns={"ub_x": "ub", "lb_x": "lb"})
    # change datatype from float to int
    co.ub = co.ub.astype(int)
    co.lb = co.lb.astype(int)
    # drop unnecessary columns
    co = co[['fipstate', 'fipscty', 'naics', 'lb', 'ub']]
    co = co.sort_values(by=['fipstate', 'fipscty'])

    return (us, st, co)

def matrixToBigDataFrame(ub, lb):
    ub['naics'] = ub.index
    lb['naics'] = lb.index

    ub_df = pd.melt(ub, id_vars=['naics'], var_name='geo', value_name='ub')
    lb_df = pd.melt(lb, id_vars=['naics'], var_name='geo', value_name='lb')

    df = pd.merge(ub_df, lb_df, on=['naics', 'geo'])

    # some rows were added to make a matrix
    # but they did not exist in the original database
    df = df[df['ub'] != 0]

    return df

def findNonzeroSlack(ub_slack, lb_slack):
    ub_df = pd.melt(ub_slack, id_vars=['naics'], var_name='geo', value_name='ub')
    lb_df = pd.melt(lb_slack, id_vars=['naics'], var_name='geo', value_name='lb')
    df = pd.merge(ub_df, lb_df, on=['naics', 'geo'])
    # delete nonzero entries
    df = df[(df['ub'] != 0) | (df['lb'] != 0)]

    return df

def save(ub, lb, year="2016", optional_name=""):
    big_df = matrixToBigDataFrame(ub, lb)
    (us, st, co) = splitBigDataFrame(big_df, year)

    us.to_csv("cbp" + year + "us" + optional_name + ".csv", index=False)
    st.to_csv("cbp" + year + "st" + optional_name + ".csv", index=False)
    co.to_csv("cbp" + year + "co" + optional_name + ".csv", index=False)

'''
optimize is a method that takes in a 'fixed location' (which could be a geographical
location like a county or a NAICS code) and a 'variable' tree.
It goes over the tree and optimizes the corresponding entries based on the child-parent
relations in the tree.
'''
def optimize(ub_matrix, lb_matrix, geo_tree, naics_tree,
    location, tree, direction='up', method='children', suppress_output=True):
    if suppress_output == False:
        print('Optimizing. Method: ' + method)

    # direction of the optimization
    r = range(len(tree))
    if direction == 'down': r = reversed(r)

    for index in r:
        node = tree[index]

        # if there is theoretically no children,
        # there is no optimization to be done
        if len(node['children']) == 0:
            continue

        code_upper, code_lower = read_df(merge_dict(node, location), ub_matrix, lb_matrix)

        sum_children_upper, sum_children_lower = (0, 0)
        for c in node['children']:
            (ub,lb) = read_df(merge_dict(tree[c], location), ub_matrix, lb_matrix)
            sum_children_upper += ub
            sum_children_lower += lb

        # if there is no children in the database (even though theoretically
        # there could be), then you can't optimize
        if (sum_children_upper, sum_children_lower) == (0,0):
            continue

        if method == 'children':
            # if none of the children is suppressed, don't update them
            if sum_children_lower == sum_children_upper:
                continue

            for c in node['children']:
                c_upper, c_lower = read_df(merge_dict(tree[c], location), ub_matrix, lb_matrix)

                new_value_upper = min(c_upper, code_upper-(sum_children_lower-c_lower))
                new_value_lower = max(c_lower, code_lower-(sum_children_upper-c_upper))

                # sum of children should be updated
                sum_children_lower += new_value_lower - c_lower
                sum_children_upper += new_value_upper - c_upper

                if (not suppress_output) and ((c_upper, c_lower) != (new_value_upper, new_value_lower)):
                    print(index, c, c_upper, c_lower, new_value_upper, new_value_lower)

                (ub_matrix, lb_matrix) = write_df(merge_dict(tree[c], location), 'ub', new_value_upper, ub_matrix, lb_matrix)
                (ub_matrix, lb_matrix) = write_df(merge_dict(tree[c], location), 'lb', new_value_lower, ub_matrix, lb_matrix)

        elif method == 'parent':
            # if the parent is not suppressed, don't update it
            if code_upper == code_lower:
                continue

            if (not suppress_output) and (sum_children_lower > code_lower or sum_children_upper < code_upper):
                print(index, code_upper, code_lower, sum_children_upper, sum_children_lower)

            new_value_upper = min(sum_children_upper, code_upper)
            new_value_lower = max(sum_children_lower, code_lower)

            # a discrepancy in the data means that there is no overlap between
            # the entry's interval and the interval obtained using its children's
            # sum. The if statement below checks if there is a discrepancy at this entry.
            # if there is a discrepancy in data, print out and exit.
            if max(sum_children_lower, code_lower)>min(sum_children_upper, code_upper):
                print('discrepancy')
                print('index: ' + str(index))
                print('location: ' + str(location))
                print('children sum (lower, upper): ' + str((sum_children_lower, sum_children_upper)))
                print('code (lower, upper): ' + str((code_lower, code_upper)))

                save(ub, lb, optional_name='_problem')

                exit()

            (ub_matrix, lb_matrix) = write_df(merge_dict(node, location),'lb', new_value_lower, ub_matrix, lb_matrix)
            (ub_matrix, lb_matrix) = write_df(merge_dict(node, location),'ub', new_value_upper, ub_matrix, lb_matrix)

    return (ub_matrix, lb_matrix)

# establishment bounds
def fix(ub_matrix, lb_matrix, ub_est, lb_est, geo_tree, naics_tree, suppress_output):
    for geo_index, geo in enumerate(geo_tree):
        for naics_index, naics in enumerate(naics_tree):
            current_entry = merge_dict(naics, geo)

            current_upper, current_lower = read_df(current_entry, ub_matrix, lb_matrix)
            current_upper_est, current_lower_est = read_df(current_entry, ub_est, lb_est)
            est_violates_adding_up_constraints = False

            # NAICS
            # check theoretical children
            if len(naics_tree[naics_index]['children']) != 0:
                sum_children_upper, sum_children_lower = (0,0)

                for child in naics_tree[naics_index]['children']:
                    child_upper, child_lower = read_df(merge_dict(naics_tree[child], geo_tree[geo_index]), ub_matrix, lb_matrix)

                    sum_children_upper += child_upper
                    sum_children_lower += child_lower

                # are there actual children in the dataset
                if (sum_children_upper, sum_children_lower) != (0,0):
                    # is the establishment dataset: (1) better (2) violating adding up constraints?

                    # the establishment dataset is better
                    if current_upper_est < current_upper or current_lower < current_lower_est:

                        # the establishment estimate does not violate adding up constraints
                        if max(current_lower_est, sum_children_lower) <= min(current_upper_est, sum_children_upper):
                            ub_matrix, lb_matrix = write_df(current_entry, 'ub', current_upper_est, ub_matrix, lb_matrix)
                            ub_matrix, lb_matrix = write_df(current_entry, 'lb', current_lower_est, ub_matrix, lb_matrix)
                        else:
                            est_violates_adding_up_constraints = True

            # GEO
            # check theoretical children
            if len(geo_tree[geo_index]['children']) != 0:
                sum_children_upper, sum_children_lower = (0,0)

                for child in geo_tree[geo_index]['children']:
                    child_upper, child_lower = read_df(merge_dict(naics_tree[naics_index], geo_tree[child]), ub_matrix, lb_matrix)

                    sum_children_upper += child_upper
                    sum_children_lower += child_lower

                # are there actual children in the dataset
                if (sum_children_upper, sum_children_lower) != (0,0):
                    # is the establishment dataset: (1) better (2) violating adding up constraints?

                    # the establishment dataset is better
                    if current_upper_est < current_upper or current_lower < current_lower_est:

                        # the establishment estimate does not violate adding up constraints
                        if max(current_lower_est, sum_children_lower) <= min(current_upper_est, sum_children_upper) and (not est_violates_adding_up_constraints):
                            ub_matrix, lb_matrix = write_df(current_entry, 'ub', current_upper_est, ub_matrix, lb_matrix)
                            ub_matrix, lb_matrix = write_df(current_entry, 'lb', current_lower_est, ub_matrix, lb_matrix)

    print('Fixed the dataset.')
    ub_matrix.to_csv('ub_fixed.csv')
    lb_matrix.to_csv('lb_fixed.csv')

    return (ub_matrix, lb_matrix)

# BOUND-TIGHTENING BEGINS HERE
def tighten_bounds(ub_matrix, lb_matrix, geo_tree, naics_tree, year = '16', suppress_output=True):
    print('tightening started')

    while True:
        old_dfs = list(map(lambda x: x.copy(), [ub_matrix, lb_matrix]))

        # STEP 1
        for geo in geo_tree:
            (ub_matrix, lb_matrix) = optimize(ub_matrix, lb_matrix, geo_tree, naics_tree, geo, naics_tree, 'down', 'children', suppress_output)

        # STEP 2
        for naics in naics_tree:
            (ub_matrix, lb_matrix) = optimize(ub_matrix, lb_matrix, geo_tree, naics_tree, naics, geo_tree, 'down', 'children', suppress_output)

        # STEP 3
        for geo in geo_tree:
            (ub_matrix, lb_matrix) = optimize(ub_matrix, lb_matrix, geo_tree, naics_tree, geo, naics_tree, 'up', 'parent', suppress_output)

        # STEP 4
        for naics in naics_tree:
            (ub_matrix, lb_matrix) = optimize(ub_matrix, lb_matrix, geo_tree, naics_tree, naics, geo_tree, 'up', 'parent', suppress_output)

        # check if we're converged
        new_dfs = [ub_matrix, lb_matrix]
        if equalListDataFrames(new_dfs, old_dfs):
            # write data
            ub_matrix.to_csv('ub_converged.csv')
            lb_matrix.to_csv('lb_converged.csv')

            save(ub_matrix, lb_matrix, year, '_tightened_bounds')

            print('converged')
            break
        else:
            ub_matrix.to_csv('ub.csv')
            lb_matrix.to_csv('lb.csv')

            print('no convergence')
