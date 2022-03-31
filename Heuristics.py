import os
import pandas as pd
import numpy as np
from Hfunctions import heuristics

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Heuristics/Data'
os.chdir(path)

dtf = pd.read_csv('JSTdatasetR5.csv', header=0,
                  usecols=['year', 'iso', 'eq_capgain'])

# Create dataframes for each country into countries
countries = dtf.iso.unique()
dummy_years = [(2018), (2019)]
dummy_dtf = pd.DataFrame(dummy_years, columns=['year'])
DataFrameDict = {elem: pd.DataFrame for elem in countries}
ResultsDtfDict = {elem: pd.DataFrame for elem in countries}

for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf[dtf['iso'] == key]
    DataFrameDict[key] = DataFrameDict[key].append(
        dummy_dtf, ignore_index=True)
    DataFrameDict[key]['Recency'] = 1
    DataFrameDict[key]['60/40'] = 1
    DataFrameDict[key]['AllStocks'] = 1
    DataFrameDict[key]['2down'] = 1
    DataFrameDict[key]['Naive'] = 1
    DataFrameDict[key]['RecencyV2'] = 1
    # ResultsDtfDict[key] = resencyfunction()

Canda = heuristics(DataFrameDict['CAN'], 0, 0.025, 15)

for x in countries:
    print(x)
    heuristics(DataFrameDict[x], 0, 0.025, 15)

# # ########### Heuristics FUNCTION Check #################### #
# # def heuristics(key, cutoff, sfassetr, blocks):
#
# # ## 60/40 Part of the FUNCTION INSIDE SOME FUNCTION
# list_df = np.array_split(DataFrameDict['USA'], 15)
# for i in range(0, 15):
#     list_df[i].dropna(inplace=True)
#     list_df[i].reset_index(drop=True, inplace=True)
#     for j in list_df[i]['eq_capgain']:
#         if j > 0:
#             cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
#             # print(cr[0])
#             fwd = cr+1
#             # print(fwd[0])
#             ivalue = list_df[i].at[cr[0], 'Recency']
#             # print(ivalue)
#             rr = list_df[i].at[fwd[0], 'eq_capgain']
#             # print(rr)
#             g = (ivalue)*(1+rr)
#             # print(g)
#             list_df[i].iloc[fwd[0], 3] = g
#             if fwd[0] == len(list_df[i])-1:
#                 break
#         if j < 0:
#             cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
#             # print(cr[0])
#             fwd = cr+1
#             # print(fwd[0])
#             ivalue = list_df[i].at[cr[0], 'Recency']
#             # print(ivalue)
#             z = (ivalue)*(1+0.025)
#             # print(z)
#             list_df[i].iloc[fwd[0], 3] = z
#             if fwd[0] == len(list_df[i])-1:
#                 break
# # # check
# # list_df[0]
# # list_df[12]
# # list_df[3]
#
# # ### 60/40 Part of the FUNCTION INSIDE SOME FUNCTION
# for i in range(0, 15):
#     for j in list_df[i]['eq_capgain']:
#         cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
#         # print(cr[0])
#         fwd = cr+1
#         # print(fwd[0])
#         ivalue = list_df[i].at[cr[0], '60/40']
#         # print(ivalue)
#         rr = list_df[i].at[fwd[0], 'eq_capgain']
#         # print(rr)
#         sixty = (0.60*ivalue)*(1+rr)
#         # print(sixty)
#         forty = (0.40*ivalue)*(1+0.025)
#         # print(forty)
#         res = sixty+forty
#         list_df[i].iloc[fwd[0], 4] = res
#         if fwd[0] == len(list_df[i])-1:
#             break
# # # check
# # list_df[0]
# # list_df[3]
# # list_df[12]
#
# # ### 100% Stocks Part of the FUNCTION INSIDE SOME FUNCTION
# for i in range(0, 15):
#     for j in list_df[i]['eq_capgain']:
#         cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
#         # print(cr[0])
#         fwd = cr+1
#         # print(fwd[0])
#         ivalue = list_df[i].at[cr[0], 'AllStocks']
#         # print(ivalue)
#         res = ivalue*(1+j)
#         list_df[i].iloc[fwd[0], 5] = res
#         if fwd[0] == len(list_df[i])-1:
#             break
# # # check
# # list_df[0]
# # list_df[3]
# # list_df[12]
#
# # ### 2 down out Part of the FUNCTION INSIDE SOME FUNCTION
# list_of_js = {elem: [] for elem in range(0, 15)}
# for i in range(0, 15):
#     for j in list_df[i]['eq_capgain']:
#         list_of_js[i].append(j)
#
#
# for i in range(0, 15):
#     res = list(zip(list_of_js[i], list_of_js[i][1:]))
#     for x, y in res:
#         if x < 0 and y < 0:
#             cx = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == x].index.values
#             # print(cj[0])
#             fwd = cx+1
#             # print(fwd[0])
#             ivalue = list_df[i].iloc[cx[0], 6]
#             res = ivalue*(1+0.025)
#             list_df[i].iloc[fwd[0], 6] = res
#
#             if fwd[0] == len(list_df[i])-1:
#                 break
#         else:
#             cx = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == x].index.values
#             # print(cj[0])
#             fwd = cx+1
#             # print(fwd[0])
#             ivalue = list_df[i].iloc[cx[0], 6]
#             ave = (x+y)/2
#             res = ivalue*(1+ave)
#             list_df[i].iloc[fwd[0], 6] = res
#             if fwd[0] == len(list_df[i])-1:
#                 break
#
# # # check
# # list_df[0]
# # list_df[3]
# # list_df[12]
#
# # ### Naive Part of the FUNCTION INSIDE SOME FUNCTION
# for i in range(0, 15):
#     for j in list_df[i]['eq_capgain']:
#         if j < 0:
#             cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
#             # print(cr[0])
#             fwd = cr+1
#             # print(fwd[0])
#             ivalue = list_df[i].at[cr[0], 'Naive']
#             # print(ivalue)
#             rr = list_df[i].at[fwd[0], 'eq_capgain']
#             # print(rr)
#             g = (ivalue)*(1+rr)
#             # print(g)
#             list_df[i].iloc[fwd[0], 7] = g
#             if fwd[0] == len(list_df[i])-1:
#                 break
#         if j > 0:
#             cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
#             # print(cr[0])
#             fwd = cr+1
#             # print(fwd[0])
#             ivalue = list_df[i].at[cr[0], 'Naive']
#             # print(ivalue)
#             z = (ivalue)*(1+0.025)
#             # print(z)
#             list_df[i].iloc[fwd[0], 7] = z
#             if fwd[0] == len(list_df[i])-1:
#                 break
# # check
# # list_df[0]
# # list_df[3]
# # list_df[12]
#
# # ### Recency 2 of the FUNCTION INSIDE SOME FUNCTION
# for i in range(0, 15):
#     for j in list_df[i]['eq_capgain']:
#         if j < 0.025:
#             # print('below')
#             pos = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
#             # print(pos[0])
#             fwd = pos+1
#             # print(fwd[0])
#             ivalue = list_df[i].iloc[pos[0], 8]
#             # print(ivalue)
#             z = (ivalue)*(1+0.025)
#             # print(z)
#             list_df[i].iloc[fwd[0], 8] = z
#             if fwd[0] == len(list_df[i])-1:
#                 break
#         if j >= 0.025:
#             # print('above')
#             cr = list_df[i]['eq_capgain'][list_df[i]['eq_capgain'] == j].index.values
#             # print(cr[0])
#             fwd = cr+1
#             # print(fwd[0])
#             ivalue = list_df[i].iloc[cr[0], 8]
#             # print(ivalue)
#             rr = list_df[i].iloc[fwd[0], 2]
#             # print(rr)
#             g = (ivalue)*(1+rr)
#             # print(g)
#             list_df[i].iloc[fwd[0], 8] = g
#             if fwd[0] == len(list_df[i])-1:
#                 break
#
# finaldf = pd.concat(list_df)
# check
# list_df[0]
# list_df[3]
# list_df[12]
