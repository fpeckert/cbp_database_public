#Eckert, Fort, Schott, Yang (2019)
#Corresponding Author: mail@fpeckert.me

import numpy as np, pandas as pd
import re, sys

#Clean data and prepare bounds
def cbp_clean(data_input, geo):

    data_input.columns = map(str.lower, data_input.columns)
    data_input['empflag'] = data_input['empflag'].astype(str)
    data_input.loc[data_input.empflag == ".", 'empflag'] = ""

    if 'lfo' in data_input.columns:
        data_input = data_input[data_input.lfo == '-']
    if 'naics' in data_input.columns:
        data_input = data_input.rename(columns={"naics": "ind"})
    elif 'sic' in data_input.columns:
        data_input = data_input.rename(columns={"sic": "ind"})

    data_input['lb'] = data_input['empflag']
    data_input['ub'] = data_input['empflag']

    data_input['lb'] = data_input['lb'].replace({'A':0,'B':20,'C':100,'E':250,'F':500,'G':1000,'H':2500,'I':5000,'J':10000,'K':25000,'L':50000,'M':100000})
    data_input['ub'] = data_input['ub'].replace({'A':19,'B':99,'C':249,'E':499,'F':999,'G':2499,'H':4999,'I':9999,'J':24999,'K':49999,'L':99999,'M':100000000})

    data_input[['lb','ub']] = data_input[['lb','ub']].apply(pd.to_numeric, errors='coerce')

    data_input.loc[np.isnan(data_input.lb), {'ub','lb'}] = data_input.loc[np.isnan(data_input.lb), 'emp']

    if geo == "us":
        data_input = data_input[['ind','lb','ub']]
    elif geo == "st":
        data_input = data_input[['fipstate','ind','lb','ub']]
    elif geo == "co":
        data_input = data_input[['fipstate','fipscty','ind','lb','ub']]

    return data_input


def cbp_change_code(data_input, code_old, code_new):

    data_helper = data_input.copy()
    data_helper = data_helper[data_helper.ind == code_old]
    data_helper.loc[data_helper.ind == code_old, 'ind'] = code_new
    data_helper.loc[:, 'lb'] = 0
    data_input = data_input.append(data_helper, ignore_index=True)

    return data_input

#Clean data and prepare bounds
def cbp_drop(data_input, year, geo,codechanger):

    ind_drop_set = []
    geo_drop_set = [98,99]

    if geo == "co" and year in range(1970, 1990):
        if year == 1977:
            ind_drop_set = ["0785", "2031", "2433", "2442", "3611", "3716", "3791", "3803","3821", "5122", "5129", "6798", "7012", "7013", "8310", "8361"]

        if year == 1978:
            ind_drop_set = ["0785", "2015", "2433", "2442", "2661", "3611", "3716", "3791", "3803", "3821", "4582", "5129", "6070", "6798", "7012", "7013", "8062", "8084", "8310", "8361", "8411", "8800", "8810"]

        if year == 1979:
            ind_drop_set = ["0785", "0759", "0785", "079/", "1625", "2036", "2940", "2942", "3073", "3239", "3481", "5212", "5513", "5780", "5781", "5820", "5821", "5991", "6122", "6406", "7012", "7060", "7065", "7328", "7380", "7388", "7626", "7638", "7835", "7912",  "7994", "8120", "8126", "8500", "8560", "8562", "8680", "8800", "8810","8811", "3716", "5129", "5192", "6590", "6599", "6798", "7013", "8310", "8361"]

            data_helper = data_input.copy()
            data_helper = data_helper[data_helper.fipstate == 11]
            data_helper = data_helper[data_helper.fipscty == 99]
            data_helper.loc[:, 'lb'] = 0
            data_helper.loc[:, 'fipscty'] = 1
            data_input.append(data_helper, ignore_index=True)

        if year == 1980:
            ind_drop_set = [ "1629", "64--", "6798", "8310", "8361", "8631"]

        if year == 1981:
            ind_drop_set = ["1540", "1542", "6798", "8051", "8310", "8361"]

        if year == 1982:
            ind_drop_set = ["1321", "2771", "8800", "8810", "8811", "3716", "6590", "6599", "6798", "8310", "8361"]

        if year == 1983:
            ind_drop_set = ["1711", "3716", "4229", "6590", "6599", "6793", "6798", "8310", "8361"]

        if year == 1984:
            ind_drop_set = ["3716", "4229", "5380", "5580", "6590", "6599", "6798", "8310", "8361"]

        if year == 1985:
            ind_drop_set = ["3716", "5380", "5580", "6798", "8310", "8361"]

        if year == 1986:
            ind_drop_set = ["1111", "1481", "1531", "1611", "4131", "4151", "4231", "4411", "4431", "4441", "4712", "4811", "4821", "4899", "4911", "4941", "4961", "4971", "5380", "5580", "5970", "6410", "6610", "7840", "8110", "8361"]

        if year == 1987:
            ind_drop_set = ["1540", "4214", "5399", "6410", "8320", "8321", "8330", "8331", "8350", "8351", "8390", "8399"]

        if year == 1988:
            ind_drop_set = ["5399"]

    elif geo == "st" and year in range(70, 91):

        if year == 1977:
            ind_drop_set = ["0785", "2031", "2433", "2442", "3611", "3716", "3791", "3803", "3821", "5129", "6798", "7012", "7013", "8310", "8361"]

        if year == 1978:
            ind_drop_set = ["3716", "5129", "6070", "6798", "7012", "7013", "8310", "8361", "0785", "2015", "2433", "2442", "3611", "3791", "3803", "3821"]

        if year == 1979:
            ind_drop_set = ["0759", "0785", "079/", "1625", "2036", "2940", "2942", "3073", "3239", "3481", "3716", "5129", "5192", "5212", "5513", "5780", "5781", "5820", "5821", "5991", "6406", "6590", "6599", "6798", "7012", "7013", "7060", "7065", "7328", "7380", "7388", "7626", "7638", "7835", "7912", "7994", "8120", "8126", "8310", "8361", "8500", "8560", "8562", "8680", "8800", "8810", "8811"]

        if year == 1980:
            ind_drop_set = ["3716", "6798", "8310", "8361"]

        if year == 1981:
            ind_drop_set = ["1540", "1542", "6798", "8310", "8361"]

        if year == 1982:
            ind_drop_set = ["2771", "3716", "6590", "6599", "6798", "8310", "8361", "8800", "8810", "8811"]

        if year == 1983:
            ind_drop_set = ["3716", "4229", "6590", "6599", "6793", "6798", "8310", "8361"]

        if year == 1984:
            ind_drop_set = ["3716", "4229", "5380", "5580", "6590", "6599", "6798", "8310", "8361"]

        if year == 1985:
            ind_drop_set = ["3716", "5380", "5580", "6798", "8310", "8361"]

        if year == 1986:
            ind_drop_set = ["1111", "1481", "1531", "1611", "4131", "4151", "4231", "4411", "4431", "4441", "4712", "4811", "4821", "4899", "4911", "4941", "4961", "4971", "5380", "5580", "5970", "6410", "6610", "7840", "8110", "8361"]

        if year == 1987:
            ind_drop_set = ["1540", "4214", "6410", "8320", "8330", "8350", "8390"]

        if year == 1988:
            ind_drop_set = ["5399"]

        if year == 1990:
            ind_drop_set = ["8990"]

    elif geo == "us" and year in range(1970, 1990):

        if year == 1977:
            ind_drop_set = ["3716", "5129", "6798", "7012", "7013", "8310", "8361"]
            data_input = codechanger(data_input, "40--", "4300")
            data_input = codechanger(data_input, "40--", "4310")
            data_input = codechanger(data_input, "40--", "4311")

        if year == 1978:
            ind_drop_set = ["3716", "5129", "6070", "6798", "7012", "7013", "8310", "8361"]

        if year == 1979:
            ind_drop_set = ["5129", "6590", "6599", "6798", "7013", "8310", "8361"]
            data_input = codechanger(data_input, "1090", "1092")
            data_input = codechanger(data_input, "6110", "6113")

        if year == 1980:
            ind_drop_set = ["3761", "6798", "8310", "8361"]
            data_input = codechanger(data_input, "1090", "1092")
            data_input = codechanger(data_input, "6110", "6113")

        if year == 1981:
            ind_drop_set = ["6798", "8310", "8361"]
            data_input = codechanger(data_input, "6110", "6113")

        if year == 1982:
            ind_drop_set = ["3716", "6590", "6599", "6798", "8310", "8361"]
            data_input = codechanger(data_input, "1090", "1092")
            data_input = codechanger(data_input, "6110", "6113")

        if year == 1983:
            ind_drop_set = ["3716", "4229", "6590", "6599", "6798", "8310", "8361"]
            data_input = codechanger(data_input, "3570", "3572")
            data_input = codechanger(data_input, "6110", "6113")

        if year == 1984:
            ind_drop_set = ["3716", "4229", "6590", "6599", "6798", "8310", "8361"]
            data_input = codechanger(data_input, "3570", "3572")
            data_input = codechanger(data_input, "3670", "3673")

        if year == 1985:
            ind_drop_set = ["3716", "6798", "8310", "8361"]
            data_input = codechanger(data_input, "3570", "3572")

        if year == 1986:
            ind_drop_set = ["1111", "1481", "1531", "1611", "4131", "4151", "4231", "4411", "4431", "4441", "4712", "4811", "4821", "4899", "4911", "4941", "4961", "4971", "5380", "5580", "5970", "6410", "6610", "7840", "8110", "8361"]
            data_input = codechanger(data_input, "3570", "3572")

        if year == 1987:
            ind_drop_set = ["1110", "1210", "1540", "5399", "6410", "8320", "8321", "8330", "8331", "8350", "8351", "8390", "8399"]
            data_input = codechanger(data_input, "1112", "1110")
            data_input = codechanger(data_input, "1211", "1210")
            data_input = codechanger(data_input, "5800", "5810")


    data_input = data_input[~data_input.ind.isin(ind_drop_set)]

    if geo == 'co' or geo == 'st':
        data_input = data_input[~data_input.fipstate.isin(geo_drop_set)]

    data_input.loc[data_input.ind == "19--", 'ind'] = "20--"
    data_input.loc[data_input.ind == "--", "ind"] = "07--"


    if year == 1997:
        data_input = codechanger(data_input, "5800", "5810")
        data_input = codechanger(data_input, "2070", "2067")

    if year in range(1991, 1997):
        data_input = codechanger(data_input, "5800", "5810")

    if year in range(1970, 1998):
        data_input.ind = data_input.ind.str.replace('/','\\')

    return data_input


##Industry Code Files
def indreforder_ind(data_input):

    data_input = data_input[['NAICS']]
    data_input = data_input.sort_values(by = 'NAICS')

    return data_input


##Geography Code Files
def indreforder_geo(data_input):

    data_input = data_input[['fipstate','fipscty']]
    data_input = data_input.sort_values(by = ['fipstate','fipscty'])

    return data_input
