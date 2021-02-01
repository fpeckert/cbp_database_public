import shutil
import os
import csv

# 1970 and 1972 have state summary (STSUM) files, but cannot find electronic documentation
# Some of the CSV files have interesting 'D's and other values.. would love to discuss which are good and which aren't
# 1974 does not have US data
# 1974-1986 state data: flag 50 might have been a little off (mismatch between start index and width)

# TEST DIVISION YEARS 1971 - 1973
# Convert files to txt files

yearlist = ['70', '71', '72', '73']
divlist = ['1-2', '3-4', '5-6', '7-9']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    for div in divlist:
        file_name = "CBP" + year + ".DIV" + div
        os.rename(r"/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"+file_name,
                  r"/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"+file_name+'.txt')

# Concatenate division files
yearlist = ['70', '71', '72', '73']
divlist = ['1-2', '3-4', '5-6', '7-9']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    with open(root + year + "_div_data.txt", 'wb') as wfd:
        for div in divlist:
            file_name = "CBP" + year + ".DIV" + div
            with open(root+file_name+ ".txt", 'rb') as fd:
                    shutil.copyfileobj(fd, wfd)


# FOR YEARS 1970 - 1973 (split into divisions)

yearlist = ['70', '71', '72', '73']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = year + "_div_data.txt"
    text_file = open(file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    newcsv = csv.writer(open(root + 'CBP19'+ year + 'div.csv', 'w'))
    newcsv.writerow(["stcode", "cocode", "siccode", "totemp", "totwages", "rptun", "rptun_cl1", "rptun_cl2", "rptun_cl3",
         "rptun_cl4", "rptun_cl5", "rptun_cl6", "rptun_cl7", "rptun_cl8", "geoname"])

    for line in lines:
        # split information in each line and write to csv file
        stcode = line[0:2]
        cocode = line[2:5]
        # blank1 = line[5]
        siccode = line[6:10]
        # blank2 = line[10:12]
        totemp = line[12:24]
        totwages = line[24:36]
        rptun = line[36:42]
        rptun_cl1 = line[42:48]
        rptun_cl2 = line[48:54]
        rptun_cl3 = line[54:60]
        rptun_cl4 = line[60:66]
        rptun_cl5 = line[66:72]
        rptun_cl6 = line[72:78]
        rptun_cl7 = line[78:84]
        rptun_cl8 = line[84:90]
        # blank3 = line[90:96]
        geoname = line[96:]

        newcsv.writerow(
            [stcode, cocode, siccode, totemp, totwages, rptun, rptun_cl1, rptun_cl2, rptun_cl3, rptun_cl4, rptun_cl5,
             rptun_cl6, rptun_cl7, rptun_cl8, geoname])

# TEST YEARS 1974 - 1987
# Concatenate county files

yearlist = ['74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = "RG029.CBP" + year + ".T2I"
    with open(root + year + '_county_data.txt', 'wb') as wfd:
        for i in range(1, 10):
            with open(root + file_name + str(i), 'rb') as fd:
                shutil.copyfileobj(fd, wfd)

# NOTE: Add in code to delete other county files???


# FOR YEARS 1974 - 1986 (COUNTY DATA)

yearlist = ['74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = year + '_county_data.txt'
    text_file = open(root + file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    newcsv = csv.writer(open(root + 'CBP19'+ year + 'cty.csv', 'w'))
    newcsv.writerow(["STATE2", "COUNTY2", "SICCODE", "TFLAG", "FILL1", "FILL2", "TEMPMM", "TPAYQ1","TANPAY",
                    "TESTAB", "CTYEMPl", "CTYEMP2", "CTYEMP3", "CTYEMP4", "CTYEMP5", "CTYEMP6", "CTYEMP7", "CTYEMP8",
                    "CTYEMP9", "CTYEMP10", "CTYEMP11", "CTYEMP12", "CTYEMP13", "FILL3", "SSASTAT2", "SSACTY2", "FILL4",
                    "FIPSTATE", "FIPSCTY2", "FILL5"])


    for line in lines:
        STATE2 = line[0:2]
        COUNTY2 = line[2:5]
        SICCODE =  line[5:11]
        TFLAG = line[11:12] 
        FILL1 = line[12:14]
        FILL2 = line[14:15]
        TEMPMM = line[15:27]
        TPAYQ1 = line[27:39]
        TANPAY = line[39:51]
        TESTAB = line[51:57]
        CTYEMPl = line[57:63]
        CTYEMP2 = line[63:69]
        CTYEMP3 = line[69:75]
        CTYEMP4 = line[75:81]
        CTYEMP5 = line[81:87]
        CTYEMP6 = line[87:93]
        CTYEMP7 = line[93:99]
        CTYEMP8 = line[99:105]
        CTYEMP9 = line[105:111]
        CTYEMP10 = line[111:117]
        CTYEMP11 = line[117:123]
        CTYEMP12 = line[123:129]
        CTYEMP13 = line[129:130]
        FILL3 = line[129:132]
        SSASTAT2 = line[136:138]
        SSACTY2 = line[138:141]
        FILL4 = line[141:142]
        FIPSTATE = line[139:141]
        FIPSCTY2 = line[141:144]
        FILL5 = line[147:]

        newcsv.writerow([STATE2, COUNTY2, SICCODE, TFLAG, FILL1, FILL2, TEMPMM, TPAYQ1, TANPAY,
                        TESTAB, CTYEMPl, CTYEMP2, CTYEMP3, CTYEMP4, CTYEMP5, CTYEMP6, CTYEMP7, CTYEMP8,
                        CTYEMP9, CTYEMP10, CTYEMP11, CTYEMP12, CTYEMP13, FILL3, SSASTAT2, SSACTY2, FILL4,
                        FIPSTATE, FIPSCTY2, FILL5])

# Concatenate state files (years with B1 - B9 state divisions)
yearlist = ['74', '75', '76', '77']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    with open(root + "RG029.CBP" + year + ".T1ST", 'wb') as wfd:
        for i in range(1, 10):
            with open(root + "RG029.CBP" + year + ".T1B" + str(i), 'rb') as fd:
                shutil.copyfileobj(fd, wfd)

# Concatenate state files (years with census state divisions)
yearlist = ['78', '79']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    list = [root + "RG029.CBP" + year + ".T115", root +"RG029.CBP" + year + ".T169"]
    with open(root +"RG029.CBP" + year + ".T1ST", 'wb') as wfd:
        for f in list:
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd)

# Rename state files to have consistent naming
yearlist = ['80', '81', '82']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = "RG029.CBP" + year + ".T119"
    os.rename(root + file_name, root + "RG029.CBP" + year + ".T1ST")

# FOR YEARS 1974 - 1986 (STATE DATA)
yearlist = ['74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = "RG029.CBP" + year + ".T1ST"
    text_file = open(root + file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    newcsv = csv.writer(open(root + "CBP19" + year + 'st.csv', 'w'))
    newcsv.writerow(["state1B", "fill1", "siccode1", "fill2", "tflag", "tempmm",
                     "tpayq1", "tanpay", "testab", "flag1", "emp1m4", "qwa1q4", "awg1q4",
                     "estno4q1", "flag5", "emp5m9", "fqwg5q9", "awg5q9", "estno5q9", "flag10",
                     "emp10m19", "wg10q19", "awg10q19", "est10q19", "flag20", "emp20m49", "wg20q49",
                     "awg20q49", "est20q49", "flag50", "emp50m99", "wg50m99", "qwg50q99", "est50q99",
                     "flag100", "e100m249", "w100q249", "a100q249", "n100q249", "flag250", "e250m499",
                     "w250q499", "a250q499", "n250q499", "flag500", "e500m999", "w500q999", "a500q999",
                     "n500q999", "flag1000", "emp1000m", "ewg1000q", "awg1000q", "en01000q", "fill3",
                     "ssacode", "fill4", "fipstate", "fill5"])

    for line in lines:
        # split information in each line and write to csv file
        state1B = line[0:2]
        fill1 = line[2:6]
        siccode1 = line[6:10]
        fill2 = line[10:12]
        tflag = line[12:13]
        tempmm = line[13:20]
        tpayq1 = line[20:28]
        tanpay = line[28:37]
        testab = line[37:43]
        flag1 = line[43:44]
        emp1m4 = line[44:50]
        qwa1q4 = line[50:56]
        awg1q4 = line[56:63]
        estno4q1 = line[63:69]
        flag5 = line[69:70]
        emp5m9 = line[70:76]
        fqwg5q9 = line[76:83]
        awg5q9 = line[83:90]
        estno5q9 = line[90:96]
        flag10 = line[96:97]
        emp10m19 = line[97:103]
        wg10q19 = line[103:110]
        awg10q19 = line[110:117]
        est10q19 = line[117:123]
        flag20 = line[123:124]
        emp20m49 = line[124:131]
        wg20q49 = line[131:138]
        awg20q49 = line[138:145]
        est20q49 = line[145:150]
        flag50 = line[150:151]  #says size is 5? But next one starts one over
        emp50m99 = line[151:157]
        wg50m99 = line[157:164]
        awg50q99 = line[164:171]
        est50q99 = line[171:176]
        flag100 = line[176:177]
        e100m249 = line[177:184]
        w100q249 = line[184:191]
        a100q249 = line[191:199]
        n100q249 = line[199:204]
        flag250 = line[204:205]
        e250m499 = line[205:212]
        w250q499 = line[212:219]
        a250q499 = line[219:227]
        n250q499 = line[227:231]
        flag500 = line[231:232]
        e500m999 = line[232:239]
        w500q999 = line[239:246]
        a500q999 = line[246:254]
        n500q999 = line[254:258]
        flag1000 = line[258:259]
        emp1000m = line[259:266]
        ewg1000q = line[266:273]
        awg1000q = line[273:281]
        en01000q = line[281:285]
        fill3 = line[285:289]
        ssacode = line[289:291]
        fill4 = line[291:295]
        fipstate = line[295:297]
        fill5 = line[297:]


        newcsv.writerow([state1B, fill1, siccode1, fill2, tflag, tempmm,
                         tpayq1, tanpay, testab, flag1, emp1m4, qwa1q4, awg1q4,
                         estno4q1, flag5, emp5m9, fqwg5q9, awg5q9, estno5q9, flag10,
                         emp10m19, wg10q19, awg10q19, est10q19, flag20, emp20m49, wg20q49,
                         awg20q49, est20q49, flag50, emp50m99, wg50m99, awg50q99, est50q99,
                         flag100, e100m249, w100q249, a100q249, n100q249, flag250, e250m499,
                         w250q499, a250q499, n250q499, flag500, e500m999, w500q999, a500q999,
                         n500q999, flag1000, emp1000m, ewg1000q, awg1000q, en01000q, fill3,
                         ssacode, fill4, fipstate, fill5])


# 1975 - 1979 (U.S. DATA)
yearlist = ['75', '76', '77', '78', '79']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = "RG029.CBP" + year + ".USUM"
    text_file = open(root + file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    newcsv = csv.writer(open(root + 'CBP19' + year+ 'us.csv', 'w'))
    newcsv.writerow(["USIND", "SICCODE1", "TFLAG", "TEMPM", "TPAYQ1", "TPAY", "TESTB", "FILL1", "FLAG1", "EMP1M4",
                     "EMPWG1Q4", "EMPAN1Q4", "ESTNU1Q4", "FLAG5", "EMP5M9", "EMPWG5Q9", "EMPAN5Q9", "ESTNU5Q9",
                     "FLAG10", "EMP10M19", "EWG10Q19", "EAN10Q19", "ENU10Q19", "FLAG20", "EMP20M49", "EWG0Q49",
                     "EAN20Q49", "ENU20Q49", "FLAG50", "EMP50M99", "EWG50Q99", "EAN50Q99", "ENU50Q99", "FLAG100",
                     "E100M249", "W100Q249", "A100Q249", "N100Q249", "FLAG250", "E250M499", "W250Q499", "A250Q499",
                     "N250Q499", "FLAG500", "E500M999", "W500M999", "A500M999", "N500M999", "FLAG1000",
                     "EMP1000M", "EWG1000Q", "EAN10000Q", "ENU1000Q", "FILL2"])

    for line in lines:

        USIND = line[0:2]
        SICCODE1 = line[2:6]
        TFLAG = line[6:7]
        TEMPM = line[7:15]
        TPAYQ1 = line[15:24]
        TPAY = line[24:33]
        TESTB = line[33:41]
        FILL1 = line[41:43]
        FLAG1 = line[43:44]
        EMP1M4 = line[44:51]
        EMPWG1Q4 = line[51:59]
        EMPAN1Q4 = line[59:67]
        ESTNU1Q4 = line[67:74]
        FLAG5 = line[74:75]
        EMP5M9 = line[75:82]
        EMPWG5Q9 = line[82:90]
        EMPAN5Q9 = line[90:98]
        ESTNU5Q9 = line[98:104]
        FLAG10 = line[104:105]
        EMP10M19 = line[105:112]
        EWG10Q19 = line[112:120]
        EAN10Q19 = line[120:128]
        ENU10Q19 = line[128:134]
        FLAG20 = line[134:135]
        EMP20M49 = line[135:143]
        EWG0Q49 = line[143:151]
        EAN20Q49 = line[151:160]
        ENU20Q49 = line[160:166]
        FLAG50 = line[166:167]
        EMP50M99 = line[167:174]
        EWG50Q99 = line[174:182]
        EAN50Q99 = line[182:190]
        ENU50Q99 = line[190:196]
        FLAG100 = line[196:197]
        E100M249 = line[197:205]
        W100Q249 = line[205:213]
        A100Q249 = line[213:222]
        N100Q249 = line[222:227]
        FLAG250 = line[227:228]
        E250M499 = line[228:235]
        W250Q499 = line[235:243]
        A250Q499 = line[243:251]
        N250Q499 = line[251:256]
        FLAG500 = line[256:257]
        E500M999 = line[257:264]
        W500M999 = line[264:272]
        A500M999 = line[272:280]
        N500M999 = line[280:284]
        FLAG1000 = line[284:285]
        EMP1000M = line[285:293]
        EWG1000Q = line[293:301]
        EAN10000Q = line[301:310]
        ENU1000Q = line[310:314]
        FILL2 = line[314:]

        newcsv.writerow([USIND, SICCODE1, TFLAG, TEMPM, TPAYQ1, TPAY, TESTB, FILL1, FLAG1, EMP1M4,
                     EMPWG1Q4, EMPAN1Q4, ESTNU1Q4, FLAG5, EMP5M9, EMPWG5Q9, EMPAN5Q9, ESTNU5Q9,
                     FLAG10, EMP10M19, EWG10Q19, EAN10Q19, ENU10Q19, FLAG20, EMP20M49, EWG0Q49,
                     EAN20Q49, ENU20Q49, FLAG50, EMP50M99, EWG50Q99, EAN50Q99, ENU50Q99, FLAG100,
                     E100M249, W100Q249, A100Q249, N100Q249, FLAG250, E250M499, W250Q499, A250Q499,
                     N250Q499, FLAG500, E500M999, W500M999, A500M999, N500M999, FLAG1000,
                     EMP1000M, EWG1000Q, EAN10000Q, ENU1000Q, FILL2])


# 1983 - 1986 (U.S. DATA)
yearlist = ['83', '84', '85', '86']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = "RG029.CBP" + year + ".USUM"
    text_file = open(root + file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    newcsv = csv.writer(open(root + 'CBP19' + year + 'us.csv', 'w'))
    newcsv.writerow(["USIND", "SICCODE1", "TOTFLAG", "TOTTEMPM", "TOTPAYQ1", "TOTPAY", "TOTTEST", "FLAG1-4", "EMP1-4",
                     "EMPWG1-4", "EMPAN1-4", "ESTNU1-4", "FLAG5-9", "EMP5-9", "EMPWG5-9", "EMPAN5-9", "ESTNU5-9",
                     "FLAG10-19", "EMP10-19", "EWG10 - 19", "EAN10-19", "ENU10-19", "FLAG20-49", "EMP20-49", "EWG2O-49",
                     "EAN20-49", "ENU20-49", "FLAG50-99", "EMP50 - 99", "EWG5O-99", "EAN50-99", "ENU5O-99", "FL100-249",
                     "E100-249", "W100-249", "A100-249", "N100-249", "FL25O - 499", "E25O-499", "W25O-499", "A250-499",
                     "N250-499", "FL500-999", "E500-999", "W500-999", "A500-999", "N5OO-999", "FLAG1000", "EMP1000",
                     "EWG1000", "EAN1000", "ENU1000", "FILLER"])


    for line in lines:

        USIND = line[0:2]
        SICCODE1 = line[2:6]
        TOTFLAG = line[6:7]
        TOTTEMPM = line[7:15]
        TOTPAYQ1 = line[15:24]
        TOTPAY = line[24:34]
        TOTTEST = line[34:42]
        FLAG1_4 = line[42:43]
        EMP1_4 = line[43:50]
        EMPWG1_4 = line[50:58]
        EMPAN1_4 = line[58:66]
        ESTNU1_4 = line[66:73]
        FLAG5_9 = line[73:74]
        EMP5_9 = line[74:81]
        EMPWG5_9 = line[81:89]
        EMPAN5_9 = line[89:97]
        ESTNU5_9 = line[97:104]
        FLAG10_19 = line[104:105]
        EMP10_19 = line[105:112]
        EWG10_19 = line[112:120]
        EAN10_19 = line[120:128]
        ENU10_19 = line[128:134]
        FLAG20_49 = line[134:135]
        EMP20_49 = line[135:143]
        EWG2O_49 = line[143:151]
        EAN20_49 = line[151:160]
        ENU20_49 = line[160:166]
        FLAG50_99 = line[166:167]
        EMP50_99 = line[167:174]
        EWG5O_99 = line[174:182]
        EAN50_99 = line[182:191]
        ENU5O_99 = line[191:197]
        FL100_249 = line[197:198]
        E100_249 = line[198:206]
        W100_249 = line[206:214]
        A100_249 = line[214:223]
        N100_249 = line[223:228]
        FL25O_499 = line[228:229]
        E25O_499 = line[229:236]
        W25O_499 = line[236:244]
        A250_499 = line[244:53]
        N250_499 = line[253:258]
        FL500_999 = line[258:259]
        E500_999 = line[259:266]
        W500_999 = line[266:274]
        A500_999 = line[274:282]
        NSOO_999 = line[282:286]
        FLAG1000 = line[286:287]
        EMP1000 = line[287:295]
        EWG1000 = line[295:303]
        EAN1000 = line[303:312]
        ENU1000 = line[312:316]
        FILLER = line[316:]

        newcsv.writerow([USIND, SICCODE1, TOTFLAG, TOTTEMPM, TOTPAYQ1, TOTPAY, TOTTEST, FLAG1_4, EMP1_4, EMPWG1_4,
                         EMPAN1_4, ESTNU1_4, FLAG5_9, EMP5_9, EMPWG5_9, EMPAN5_9, ESTNU5_9, FLAG10_19, EMP10_19,
                         EWG10_19, EAN10_19, ENU10_19, FLAG20_49, EMP20_49, EWG2O_49, EAN20_49, ENU20_49, FLAG50_99,
                         EMP50_99, EWG5O_99, EAN50_99, ENU5O_99, FL100_249, E100_249, W100_249, A100_249, N100_249,
                         FL25O_499, E25O_499, W25O_499, A250_499, N250_499, FL500_999, E500_999, W500_999, A500_999,
                         NSOO_999, FLAG1000, EMP1000, EWG1000, EAN1000, ENU1000, FILLER])


# 1980 - 1982 (U.S. DATA)
yearlist = ['80', '81', '82']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = "RG029.CBP" + year + ".USUM"
    text_file = open(root + file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    newcsv = csv.writer(open(root + 'CBP19' + year + 'us.csv', 'w'))
    newcsv.writerow(["USIND", "SICCODE1", "TFLAG", "TEMPM", "TPAYQ1", "TPAY", "TESTB", "FILL1", "FLAG1", "EMP1M4",
                     "EMPWG1Q4", "EMPAN1Q4", "ESTNU1Q4", "FLAG5", "EMP5M9", "EMPWG5Q9", "EMPAN5Q9", "ESTNU509",
                     "FLAG10", "EMP10M19", "EWG10Q19", "EAN10Q19", "ENU10Q19", "FLAG20", "EMP20M49", "EWG20Q49",
                     "EAN20Q49", "ENU20Q49", "FLAG50", "EMP50M99", "EWG50Q99", "EAN50Q99", "ENU50Q99", "FLAG100",
                     "E100M249", "W100Q249", "A100Q249", "N100Q249", "FLAG250", "E250M499", "W250Q499", "A250Q499",
                     "N250Q499", "FLAG500", "E500M999", "W500Q999", "A500Q999", "N500Q999", "FLAG1000", "EMP1000M",
                     "EWG1000Q", "EAN1000Q", "ENU1000Q", "FILL2"])

    for line in lines:

        USIND = line[0:2]
        SICCODE1 = line[2:6]
        TFLAG = line[6:7]
        TEMPM = line[7:15]
        TPAYQ1 = line[15:24]
        TPAY = line[24:34]
        TESTB = line[34:42]
        FILL1 = line[42:43]
        FLAG1 = line[43:44]
        EMP1M4 = line[44:51]
        EMPWG1Q4 = line[51:59]
        EMPAN1Q4 = line[59:67]
        ESTNU1Q4 = line[67:74]
        FLAG5 = line[74:75]
        EMP5M9 = line[75:82]
        EMPWG5Q9 = line[82:90]
        EMPAN5Q9 = line[90:98]
        ESTNU509 = line[98:104]
        FLAG10 = line[104:105]
        EMP10M19 = line[105:112]
        EWG10Q19 = line[112:120]
        EAN10Q19 = line[120:128]
        ENU10Q19 = line[128:134]
        FLAG20 = line[134:135]
        EMP20M49 = line[135:143]
        EWG20Q49 = line[143:151]
        EAN20Q49 = line[151:160]
        ENU20Q49 = line[160:166]
        FLAG50 = line[166:167]
        EMP50M99 = line[167:174]
        EWG50Q99 = line[174:182]
        EAN50Q99 = line[182:191]
        ENU50Q99 = line[191:197]
        FLAG100 = line[197:198]
        E100M249 = line[198:206]
        W100Q249 = line[206:214]
        A100Q249 = line[214:223]
        N100Q249 = line[223:228]
        FLAG250 = line[228:229]
        E250M499 = line[229:236]
        W250Q499 = line[236:244]
        A250Q499 = line[244:253]
        N250Q499 = line[253:258]
        FLAG500 = line[258:259]
        E500M999 = line[259:266]
        W500Q999 = line[266:274]
        A500Q999 = line[274:282]
        N500Q999 = line[282:286]
        FLAG1000 = line[286:287]
        EMP1000M = line[287:295]
        EWG1000Q = line[295:303]
        EAN1000Q = line[303:312]
        ENU1000Q = line[312:316]
        FILL2 = line[316:]

        newcsv.writerow([USIND, SICCODE1, TFLAG, TEMPM, TPAYQ1, TPAY, TESTB, FILL1, FLAG1, EMP1M4,
                        EMPWG1Q4, EMPAN1Q4, ESTNU1Q4, FLAG5, EMP5M9, EMPWG5Q9, EMPAN5Q9, ESTNU509,
                        FLAG10, EMP10M19, EWG10Q19, EAN10Q19, ENU10Q19, FLAG20, EMP20M49, EWG20Q49,
                        EAN20Q49, ENU20Q49, FLAG50, EMP50M99, EWG50Q99, EAN50Q99, ENU50Q99, FLAG100,
                        E100M249, W100Q249, A100Q249, N100Q249, FLAG250, E250M499, W250Q499, A250Q499,
                        N250Q499, FLAG500, E500M999, W500Q999, A500Q999, N500Q999, FLAG1000, EMP1000M,
                        EWG1000Q, EAN1000Q, ENU1000Q, FILL2])

# FOR YEARS 1967 and 1969
import shutil
import os
import csv

yearlist = ['1967', '1969']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year[2:] + "/"
    os.chdir(root)
    file_name = "CBP" + year + ".txt"
    text_file = open(root + file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    # name the csv file CBP + year (4 numbers) + geographic (cty, st, us)
    newcsv = csv.writer(open(root + 'CBP' + year + 'us.csv', 'w'))
    newcsv.writerow(["state", "county", "sic","tot_employees", "tot_wages","tot_reporting_units","ru_byemp1:3",
                     "ru_byemp4:7", "ru_byemp8:19", "ru_byemp20:49", "ru_byemp50:99", "ru_byemp100:249",
                     "ru_byemp250:499", "ru_byemp500;more", "county_name"])

    for line in lines:
        # split information in each line and write to csv file
        state = line[0:2]
        county = line[2:6]
        sic = line[6:10]
        tot_employees = line[12:24]
        tot_wages = line[24:36]
        tot_reporting_units = line[36:42]
        ru_byemp1_3 = line[42:48]
        ru_byemp4_7 = line[48:54]
        ru_byemp8_19 = line[54:60]
        ru_byemp20_49 = line[60:66]
        ru_byemp50_99 = line[66:72]
        ru_byemp100_249 = line[72:78]
        ru_byemp250_499 = line[78:84]
        ru_byemp500_more = line[84:90]
        county_name = line[96:114]

        newcsv.writerow([state, county, sic, tot_employees, tot_wages, tot_reporting_units, ru_byemp1_3,
                         ru_byemp4_7, ru_byemp8_19, ru_byemp20_49, ru_byemp50_99, ru_byemp100_249, ru_byemp250_499,
                         ru_byemp500_more, county_name])


# FOR 1987 (COUNTY DATA)

yearlist = ['87']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = year + '_county_data.txt'
    text_file = open(root + file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    newcsv = csv.writer(open(root + 'CBP19' + year + 'cty.csv', 'w'))
    newcsv.writerow(["FIPSTATE2", "FIPCTY2", "FILL1", "SICCODE2", "FILL2", "TFLAG", "TEMPMM", "TPAYQ1","TANPAY",
                    "TESTAB", "CTYEMPl", "CTYEMP2", "CTYEMP3", "CTYEMP4", "CTYEMP5", "CTYEMP6", "CTYEMP7", "CTYEMP8",
                    "CTYEMP9", "CTYEMP10", "CTYEMP11", "CTYEMP12", "CTYEMP13", "FILL3", "COUNTY2", "FILL4",
                    "STATE2"])


    for line in lines:
        FIPSTATE2 = line[0:2]
        FIPCTY2 = line[2:5]
        FILL1 = line[5:6]
        SICCODE2 = line[6:10]
        FILL2 = line[10:11]
        TFLAG = line[11:12]
        TEMPMM = line[12:24]
        TPAYQ1 = line[24:36]
        TANPAY = line[36:48]
        TESTAB = line[48:54]
        CTYEMPl = line[54:60]
        CTYEMP2 = line[60:66]
        CTYEMP3 = line[66:72]
        CTYEMP4 = line[72:78]
        CTYEMP5 = line[78:84]
        CTYEMP6 = line[84:90]
        CTYEMP7 = line[90:96]
        CTYEMP8 = line[96:102]
        CTYEMP9 = line[102:108]
        CTYEMP10 = line[108:114]
        CTYEMP11 = line[114:120]
        CTYEMP12 = line[120:126]
        CTYEMP13 = line[126:132]
        FILL3 = line[132:134]
        COUNTY2 = line[136:139]
        FILL4 = line[139:140]
        STATE2 = line[134:]

        newcsv.writerow([FIPSTATE2, FIPCTY2, FILL1, SICCODE2, FILL2, TFLAG, TEMPMM, TPAYQ1, TANPAY,
                     TESTAB, CTYEMPl, CTYEMP2, CTYEMP3, CTYEMP4, CTYEMP5, CTYEMP6, CTYEMP7, CTYEMP8,
                     CTYEMP9, CTYEMP10, CTYEMP11, CTYEMP12, CTYEMP13, FILL3, COUNTY2, FILL4,
                     STATE2])

# FOR YEAR 1987 (STATE DATA)
yearlist = ['87']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = "RG029.CBP" + year + ".T1ST"
    text_file = open(root + file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    newcsv = csv.writer(open(root + 'CBP19' + year + 'st.csv', 'w'))
    newcsv.writerow(["fipstate", "fill1", "siccode1", "fill2", "tflag", "tempmm",
                     "tpayq1", "tanpay", "testab", "flag1", "emp1m4", "qwa1q4", "awg1q4",
                     "estno4q1", "flag5", "emp5m9", "fqwg5q9", "awg5q9", "estno5q9", "flag10",
                     "emp10m19", "wg10q19", "awg10q19", "est10q19", "flag20", "emp20m49", "wg20q49",
                     "awg20q49", "est20q49", "flag50", "emp50m99", "wg50m99", "awg50q99", "est50q99",
                     "flag100", "e100m249", "w100q249", "a100q249", "n100q249", "flag250", "e250m499",
                     "w250q499", "a250q499", "n250q499", "flag500", "e500m999", "w500q999", "a500q999",
                     "n500q999", "flag1000", "emp1000m", "ewg1000q", "awg1000q", "en01000q", "fill3",
                     "state1b"])

    for line in lines:
        # split information in each line and write to csv file
        fipstate = line[0:2]
        fill1 = line[2:6]
        siccode1 = line[6:10]
        fill2 = line[10:12]
        tflag = line[12:13]
        tempmm = line[13:21]
        tpayq1 = line[21:29]
        tanpay = line[29:38]
        testab = line[38:44]
        flag1 = line[44:45]
        emp1m4 = line[45:51]
        qwa1q4 = line[51:58]
        awg1q4 = line[58:66]
        estno4q1 = line[66:72]
        flag5 = line[72:73]
        emp5m9 = line[73:79]
        fqwg5q9 = line[79:86]
        awg5q9 = line[86:94]
        estno5q9 = line[94:100]
        flag10 = line[100:101]
        emp10m19 = line[101:108]
        wg10q19 = line[108:115]
        awg10q19 = line[115:123]
        est10q19 = line[123:129]
        flag20 = line[129:130]
        emp20m49 = line[130:137]
        wg20q49 = line[137:144]
        awg20q49 = line[144:152]
        est20q49 = line[152:157]
        flag50 = line[157:158]
        emp50m99 = line[158:165]
        wg50m99 = line[165:172]
        awg50q99 = line[172:180]
        est50q99 = line[180:185]
        flag100 = line[185:186]
        e100m249 = line[186:193]
        w100q249 = line[193:200]
        a100q249 = line[200:208]
        n100q249 = line[208:213]
        flag250 = line[213:214]
        e250m499 = line[214:221]
        w250q499 = line[221:228]
        a250q499 = line[228:237]
        n250q499 = line[237:240]
        flag500 = line[240:241]
        e500m999 = line[241:248]
        w500q999 = line[248:255]
        a500q999 = line[255:263]
        n500q999 = line[263:267]
        flag1000 = line[267:268]
        emp1000m = line[268:275]
        ewg1000q = line[275:282]
        awg1000q = line[282:290]
        en01000q = line[290:294]
        fill3 = line[294:298]
        state1b = line[298:]



        newcsv.writerow([fipstate, fill1, siccode1, fill2, tflag, tempmm,
                     tpayq1, tanpay, testab, flag1, emp1m4, qwa1q4, awg1q4,
                     estno4q1, flag5, emp5m9, fqwg5q9, awg5q9, estno5q9, flag10,
                     emp10m19, wg10q19, awg10q19, est10q19, flag20, emp20m49, wg20q49,
                     awg20q49, est20q49, flag50, emp50m99, wg50m99, awg50q99, est50q99,
                     flag100, e100m249, w100q249, a100q249, n100q249, flag250, e250m499,
                     w250q499, a250q499, n250q499, flag500, e500m999, w500q999, a500q999,
                     n500q999, flag1000, emp1000m, ewg1000q, awg1000q, en01000q, fill3,
                     state1b])

# 1987 (U.S. DATA)
yearlist = ['87']

for year in yearlist:
    root = "/Users/soumyg/Downloads/CBP_Data/CBP_" + year + "/"
    os.chdir(root)
    file_name = "RG029.CBP" + year + ".USUM"
    text_file = open(root + file_name, "r")
    lines = text_file.readlines()
    text_file.close()
    newcsv = csv.writer(open(root + 'CBP19' + year + 'us.csv', 'w'))
    newcsv.writerow(["USIND", "SICCODE1", "TOTFLAG", "TOTTEMPM", "TOTPAYQ1", "TOTPAY", "TOTTEST", "FLAG1-4", "EMP1-4", "EMPWG1-4",
                     "EMPAN1-4", "ESTNU1-4", "FLAG5-9", "EMP5-9", "EMPWG5-9", "EMPAN5-9", "ESTNU5-9", "FLAG10-19", "EMP10-19", "EWG10-19",
                     "EAN10-19", "ENU10-19", "FLAG20-49", "EMP20-49", "EWG20-49", "EAN20-49", "ENU20-49", "FLAG50-99", "EMP50-99", "EWG50-99",
                     "EAN50-99", "ENU50-99", "FL100-249", "E100-249", "W100-249", "A100-249", "N100-249", "FL250-499", "E250-499", "W250-499",
                     "A250-499", "N250-499", "FL500-999", "E500-999", "W500-999", "A500-999", "N500-999", "FLAG1000", "EMP1000", "EWG1000",
                     "EAN1000", "ENU1000", "FILLER"])

    for line in lines:

        USIND = line[0:2]
        SICCODE1 = line[2:6]
        TOTFLAG = line[6:7]
        TOTTEMPM = line[7:15]
        TOTPAYQ1 = line[15:24]
        TOTPAY = line[24:34]
        TOTTEST = line[34:42]
        FLAG1_4 = line[42:43]
        EMP1_4 = line[43:51]
        EMPWG1_4 = line[51:59]
        EMPAN1_4 = line[59:68]
        ESTNU1_4 = line[68:75]
        FLAG5_9 = line[75:76]
        EMP5_9 = line[76:84]
        EMPWG5_9 = line[84:92]
        EMPAN5_9 = line[92:101]
        ESTNU5_9 = line[101:108]
        FLAG10_19 = line[108:109]
        EMP10_19 = line[109:117]
        EWG10_19 = line[117:125]
        EAN10_19 = line[125:134]
        ENU10_19 = line[134:140]
        FLAG20_49 = line[140:141]
        EMP20_49 = line[141:149]
        EWG20_49 = line[149:157]
        EAN20_49 = line[157:166]
        ENU20_49 = line[166:172]
        FLAG50_99 = line[172:173]
        EMP50_99 = line[173:181]
        EWG50_99 = line[181:189]
        EAN50_99 = line[189:198]
        ENU50_99 = line[198:204]
        FL100_249 = line[204:205]
        E100_249 = line[205:213]
        W100_249 = line[213:221]
        A100_249 = line[221:230]
        N100_249 = line[230:235]
        FL250_499 = line[235:236]
        E250_499 = line[236:244]
        W250_499 = line[244:252]
        A250_499 = line[252:261]
        N250_499 = line[261:266]
        FL500_999 = line[266:267]
        E500_999 = line[267:275]
        W500_999 = line[275:283]
        A500_999 = line[283:292]
        N500_999 = line[292:296]
        FLAG1000 = line[296:297]
        EMP1000 = line[297:305]
        EWG1000 = line[305:313]
        EAN1000 = line[313:322]
        ENU1000 = line[322:326]
        FILLER = line[326:]

        newcsv.writerow([USIND, SICCODE1, TOTFLAG, TOTTEMPM, TOTPAYQ1, TOTPAY, TOTTEST, FLAG1_4, EMP1_4, EMPWG1_4,
                     EMPAN1_4, ESTNU1_4, FLAG5_9, EMP5_9, EMPWG5_9, EMPAN5_9, ESTNU5_9, FLAG10_19, EMP10_19, EWG10_19,
                     EAN10_19, ENU10_19, FLAG20_49, EMP20_49, EWG20_49, EAN20_49, ENU20_49, FLAG50_99, EMP50_99, EWG50_99,
                     EAN50_99, ENU50_99, FL100_249, E100_249, W100_249, A100_249, N100_249, FL250_499, E250_499, W250_499,
                     A250_499, N250_499, FL500_999, E500_999, W500_999, A500_999, N500_999, FLAG1000, EMP1000, EWG1000,
                     EAN1000, ENU1000, FILLER])






