# from pystata import stata
# from sfi import Scalar
import os
import pandas as pd
from Hfunctions import heuristics
import numpy as np
# import stata_setup
# stata_setup.config('/Applications/Stata', 'be')


def stats_h(list, a):
    # 15 blocks takes 10 observations, decades
    command = 'summarize ' + a + ', ' + 'detail'
    list_of_stats = {elem: [] for elem in range(0, blocks)}
    for i in range(0, len(list)):
        stata.pdataframe_to_data(list[i], force=True)
        stata.run(command)
        # Get stats for each block
        N = Scalar.getValue('r(N)')
        mean = Scalar.getValue('r(mean)')
        min = Scalar.getValue('r(min)')
        max = Scalar.getValue('r(max)')
        sd = Scalar.getValue('r(sd)')
        sum = Scalar.getValue('r(sum)')
        var = Scalar.getValue('r(Var)')
        kurt = Scalar.getValue('r(kurtosis)')
        skw = Scalar.getValue('r(skewness)')

        # Append results to stats list_df
        list_of_stats[i].extend((N, mean, max, min, sd, var, sum, kurt, skw))

    df = pd.DataFrame.from_dict(list_of_stats, orient='index')
    df.rename(columns={0: "N", 1: "Mean", 2: "Max",
                       3: "Min", 4: "Sd", 5: "Var",
                       6: "Sum of Variable", 7: "Kurtosis",
                       8: "Skewness"}, inplace=True)
    # Rename columns DO NOT FORGERT
    return df


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
StatisticDict = {elem: [] for elem in countries}

for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf[dtf['iso'] == key]
    DataFrameDict[key] = DataFrameDict[key].append(
        dummy_dtf, ignore_index=True)
    DataFrameDict[key]['Recency'] = 1
    DataFrameDict[key]['sixty'] = 1
    DataFrameDict[key]['AllStocks'] = 1
    DataFrameDict[key]['twodown'] = 1
    DataFrameDict[key]['Naive'] = 1
    DataFrameDict[key]['RecencyV2'] = 1
    # ResultsDtfDict[key] = resencyfunction()

# lOOP CHECK
for key in countries:
    print(key)
    ResultsDtfDict[key], StatisticDict[key] = heuristics(
        DataFrameDict[key], 0, 0.025, 15)

# print(StatisticDict['JPN'])
# print(StatisticDict['JPN']['twodown'])
#
# print(StatisticDict['BEL'])
# print(StatisticDict['JPN']['twodown'])

# dfUSA, Statdic = heuristics(DataFrameDict['USA'], 0, 0.025, 15)
# # print(statsUSA['Recency'])
#
# writer = pd.ExcelWriter('Heuristics_test.xlsx', engine='xlsxwriter')
# dfUSA.to_excel(writer, sheet_name=key)
# Statdic['Recency'].to_excel(writer, sheet_name='USA', startrow=0, startcol=11)
# Statdic['sixty'].to_excel(writer, sheet_name='USA', startrow=19, startcol=11)
# Statdic['AllStocks'].to_excel(writer, sheet_name='USA', startrow=37, startcol=11)
# Statdic['twodown'].to_excel(writer, sheet_name='USA', startrow=0, startcol=24)
# Statdic['Naive'].to_excel(writer, sheet_name='USA', startrow=19, startcol=24)
# Statdic['RecencyV2'].to_excel(writer, sheet_name='USA', startrow=37, startcol=24)
# writer.save()

writer = pd.ExcelWriter('Heuristics_Analysis.xlsx', engine='xlsxwriter')
for key in ResultsDtfDict:
    ResultsDtfDict[key].to_excel(writer, sheet_name=key)
    StatisticDict[key]['Recency'].to_excel(
        writer, sheet_name=key, startrow=0, startcol=11)
    StatisticDict[key]['sixty'].to_excel(
        writer, sheet_name=key, startrow=19, startcol=11)
    StatisticDict[key]['AllStocks'].to_excel(
        writer, sheet_name=key, startrow=37, startcol=11)
    StatisticDict[key]['twodown'].to_excel(
        writer, sheet_name=key, startrow=0, startcol=24)
    StatisticDict[key]['Naive'].to_excel(
        writer, sheet_name=key, startrow=19, startcol=24)
    StatisticDict[key]['RecencyV2'].to_excel(
        writer, sheet_name=key, startrow=37, startcol=24)
writer.save()


#

# print(ResultsDtfDict['USA'][['Recency', '60/40',
#       'AllStocks', '2down', 'Naive', 'RecencyV2']])


#
# blocks = 15
# cutoff = 0
# sfassetr = 0.025
#
# list_df = np.array_split(DataFrameDict['BEL'], blocks)
# for i in range(0, blocks):
#     list_df[i].dropna(inplace=True)
#     list_df[i].reset_index(drop=True, inplace=True)
#
# list_df = list(filter(lambda list_df: not list_df.empty, list_df))
# list_df = [i for i in list_df if len(i) > 2]
#
# for i in range(0, len(list_df)):
#     for j in list_df[i]['eq_capgain']:
#         if j >= cutoff:
#             cr = list_df[i]['eq_capgain'][list_df[i]
#                                           ['eq_capgain'] == j].index.values
#             # print(cr[0])
#             fwd = cr + 1
#             # print(fwd[0])
#             ivalue = list_df[i].iloc[cr[0], 3]
#             # print(ivalue)
#             rr = list_df[i].iloc[fwd[0], 2]
#             g = (ivalue) * (1 + rr)
#             # print(g)
#             list_df[i].iloc[fwd[0], 3] = g
#             if fwd[0] == (len(list_df[i]) - 1):
#                 break
#         if j < cutoff:
#             cr = list_df[i]['eq_capgain'][list_df[i]
#                                           ['eq_capgain'] == j].index.values
#             # print(cr[0])
#             fwd = cr + 1
#             # print(fwd[0])
#             ivalue = list_df[i].iloc[cr[0], 3]
#             # print(ivalue)
#             z = (ivalue) * (1 + sfassetr)
#             # print(z)
#             list_df[i].iloc[fwd[0], 3] = z
#             if fwd[0] == (len(list_df[i]) - 1):
#                 break
#
# # 60/40 Part of the FUNCTION INSIDE SOME FUNCTION
# for i in range(0, len(list_df)):
#     for j in list_df[i]['eq_capgain']:
#         cr = list_df[i]['eq_capgain'][list_df[i]
#                                       ['eq_capgain'] == j].index.values
#         # print(cr[0])
#         fwd = cr + 1
#         # print(fwd[0])
#         ivalue = list_df[i].iloc[cr[0], 4]
#         # print(ivalue)
#         rr = list_df[i].iloc[fwd[0], 2]
#         # print(rr)
#         sixty = (0.60 * ivalue) * (1 + rr)
#         # print(sixty)
#         forty = (0.40 * ivalue) * (1 + sfassetr)
#         # print(forty)
#         res = sixty + forty
#         list_df[i].iloc[fwd[0], 4] = res
#         if fwd[0] == (len(list_df[i]) - 1):
#             break
#
# Recency_stats = stats_h(list_df, 'Recency')
# sixty_stats = stats_h(list_df, 'sixty')
# print(sixty_stats)
#
# stats_collection = {}
# stats_collection['Recency'] = Recency_stats
# stats_collection['sixty'] = sixty_stats
#
# stats_collection['Recency']

# STATS CHECK!
# command = 'summarize ' + 'Recency' + ', ' + 'detail'
# list_of_stats = {elem: [] for elem in range(0, blocks)}
# for i in range(0, len(list_df)):
#     stata.pdataframe_to_data(list_df[i], force=True)
#     stata.run(command)
#     # Get stats for each block
#     N = Scalar.getValue('r(N)')
#     mean = Scalar.getValue('r(mean)')
#     min = Scalar.getValue('r(min)')
#     max = Scalar.getValue('r(max)')
#     sd = Scalar.getValue('r(sd)')
#     sum = Scalar.getValue('r(sum)')
#     var = Scalar.getValue('r(Var)')
#     kurt = Scalar.getValue('r(kurtosis)')
#     skw = Scalar.getValue('r(skewness)')
#
#     # Append results to stats list_df
#     list_of_stats[i].extend((N, mean, max, min, sd, var, sum, kurt, skw))
#
# df = pd.DataFrame.from_dict(list_of_stats, orient='index')
# df.rename(columns={0: "N", 1: "Mean", 2: "Max",
#                    3: "Min", 4: "Sd", 5: "Var",
#                    6: "Sum of Variable", 7: "Kurtosis",
#                    8: "Skewness"}, inplace=True)
#
# df
