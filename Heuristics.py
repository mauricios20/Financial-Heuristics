import os
import pandas as pd
import numpy as np
import xlsxwriter

#  # #################### Load data ######################

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Heuristics/Data'
os.chdir(path)

dtf = pd.read_csv('JSTdatasetR5.csv', header=0,
                    usecols=['year', 'iso', 'eq_capgain'])

# Create dataframes for each country into countries
countries = dtf.iso.unique()
dummy_years = [(2018), (2019)]
dummy_dtf = pd.DataFrame(dummy_years, columns=['year'])
DataFrameDict = {elem: pd.DataFrame for elem in countries}


for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf[dtf['iso'] == key]
    DataFrameDict[key] = DataFrameDict[key].append(dummy_dtf, ignore_index=True)
    DataFrameDict[key]['Recency'] = 1
    DataFrameDict[key]['60/40'] = 1

# ### Recency FUNCTION INSIDE SOME FUNCTION
# def recency(key, cutoff, sfassetr, blocks)
list_df = np.array_split(DataFrameDict['USA'], 15)
for i in range(0, 15):
    list_df[i].dropna(inplace=True)
    list_df[i].reset_index(drop=True, inplace=True)
    for j in list_df[i]['eq_capgain']:
        if j > 0:
            cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
            # print(cr[0])
            fwd = cr+1
            # print(fwd[0])
            ivalue = list_df[i].at[cr[0], 'Recency']
            # print(ivalue)
            rr = list_df[i].at[fwd[0], 'eq_capgain']
            # print(rr)
            g = (ivalue)*(1+rr)
            # print(g)
            list_df[i].iloc[fwd[0], 3] = g
            if fwd[0] == len(list_df[i])-1:
                break
        if j < 0:
            cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
            # print(cr[0])
            fwd = cr+1
            # print(fwd[0])
            ivalue = list_df[i].at[cr[0], 'Recency']
            # print(ivalue)
            z = (ivalue)*(1+0.025)
            # print(z)
            list_df[i].iloc[fwd[0], 3] = z
            if fwd[0] == len(list_df[i])-1:
                break
# # check
# list_df[0]
# list_df[12]
# list_df[3]

# ### 60/40 FUNCTION INSIDE SOME FUNCTION
# def sixtyforty(key, cutoff, sfassetr, blocks)
list_df = np.array_split(DataFrameDict['USA'], 15)
for i in range(0, 15):
    list_df[i].dropna(inplace=True)
    list_df[i].reset_index(drop=True, inplace=True)
    for j in list_df[i]['eq_capgain']:
        if j > 0:
            cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
            # print(cr[0])
            fwd = cr+1
            # print(fwd[0])
            ivalue = list_df[i].at[cr[0], 'Recency']
            # print(ivalue)
            rr = list_df[i].at[fwd[0], 'eq_capgain']
            # print(rr)
            g = (ivalue)*(1+rr)
            # print(g)
            list_df[i].iloc[fwd[0], 3] = g
            if fwd[0] == len(list_df[i])-1:
                break
        if j < 0:
            cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
            # print(cr[0])
            fwd = cr+1
            # print(fwd[0])
            ivalue = list_df[i].at[cr[0], 'Recency']
            # print(ivalue)
            z = (ivalue)*(1+0.025)
            # print(z)
            list_df[i].iloc[fwd[0], 3] = z
            if fwd[0] == len(list_df[i])-1:
                break
