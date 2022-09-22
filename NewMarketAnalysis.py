
from pystata import stata
from sfi import Scalar, Matrix
import os
import pandas as pd
import numpy as np
import stata_setup
stata_setup.config('/Applications/Stata', 'be')


# Function for Overall Stats


def iso(key, x):
    # 15 blocks takes 10 observations, decades
    command = 'summarize ' + x + ', ' + 'detail'
    list_of_stats = []
    stata.pdataframe_to_data(DataFrameDict[key], force=True)
    stata.run(command)
    # Get stats for each block
    N = Scalar.getValue('r(N)')
    mean = Scalar.getValue('r(mean)')
    min = Scalar.getValue('r(min)')
    max = Scalar.getValue('r(max)')
    sd = Scalar.getValue('r(sd)')

    # Append results to stats list_df
    list_of_stats.extend((N, mean, max, min, sd))

    # Rename columns DO NOT FORGERT
    return list_of_stats

# Second Function for Overall Statistics


def compile_dic(dic):
    # Compile dictionary created above into a data frame
    dtf = pd.DataFrame.from_dict(dic, orient='index')
    dtf.rename(columns={0: "N", 1: "Mean", 2: "Max",
                        3: "Min", 4: "Sd"}, inplace=True)

    return dtf
# Function for Decades and 30 year blocks


def iso_dtf(key, x, blocks):
    # 15 blocks takes 10 observations, decades
    command = 'summarize ' + x + ', ' + 'detail'
    list_df = np.array_split(DataFrameDict[key], blocks)
    list_of_stats = {elem: [] for elem in range(0, blocks)}
    for i in range(0, blocks):
        stata.pdataframe_to_data(list_df[i], force=True)
        stata.run(command)
        # Get stats for each block
        N = Scalar.getValue('r(N)')
        mean = Scalar.getValue('r(mean)')
        min = Scalar.getValue('r(min)')
        max = Scalar.getValue('r(max)')
        sd = Scalar.getValue('r(sd)')

        # Append results to stats list_df
        list_of_stats[i].extend((N, mean, max, min, sd))

    df = pd.DataFrame.from_dict(list_of_stats, orient='index')
    df.rename(columns={0: "N", 1: "Mean", 2: "Max",
                       3: "Min", 4: "Sd"}, inplace=True)
    # Rename columns DO NOT FORGERT
    return df


#  # #################### Load data ######################


path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Heuristics/DataDos'
os.chdir(path)

dtf = pd.read_csv('JSTdatasetR5.csv', header=0,
                  usecols=['year', 'iso', 'eq_capgain', 'bill_rate'])

# Create dataframes for each country into countries
excludeCountries = ['CHE', 'ESP', 'FIN', 'IRL', 'NLD', 'NOR', 'PRT']
dtfClean = dtf.loc[~dtf.iso.isin(excludeCountries)]


countries = dtfClean.iso.unique()
dummy_years = [(2018), (2019)]
dummy_dtf = pd.DataFrame(dummy_years, columns=['year'])
DataFrameDict = {elem: pd.DataFrame for elem in countries}
list_df = {elem: [] for elem in countries}

GStats = {elem: pd.DataFrame for elem in countries}
GStatsBills = {elem: pd.DataFrame for elem in countries}

for key in DataFrameDict.keys():
    DataFrameDict[key] = dtfClean[dtfClean['iso'] == key]
    DataFrameDict[key] = DataFrameDict[key].append(
        dummy_dtf, ignore_index=True)
    GStats[key] = iso(key, 'eq_capgain')
    GStatsBills[key] = iso(key, 'bill_rate')


# # Performe stata commands for Overall Stats
GSdtf = compile_dic(GStats)
GSdtfBills = compile_dic(GStatsBills)


# # Performe stata commands in all the decades
decades = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
DecadeDict = {elem: pd.DataFrame for elem in countries}
DecadeDictBills = {elem: pd.DataFrame for elem in countries}
for key in DecadeDict.keys():
    DecadeDict[key] = iso_dtf(key, 'eq_capgain', 15)
    DecadeDictBills[key] = iso_dtf(key, 'bill_rate', 15)
    DecadeDict[key].insert(0, "Country", key, True)
    DecadeDict[key].insert(1, "Decades", decades, True)
    DecadeDictBills[key].insert(0, "Country", key, True)
    DecadeDictBills[key].insert(1, "Decades", decades, True)

print(DecadeDict['AUS'])

overallDtfDC = pd.concat(DecadeDict.values())
overallDtfBills = pd.concat(DecadeDictBills.values())


# # Performe stata commands in all the 30 year blocks
blocks = [1, 2, 3, 4, 5]
ThirtyDict = {elem: pd.DataFrame for elem in countries}
ThirtyDictBills = {elem: pd.DataFrame for elem in countries}
for key in ThirtyDict.keys():
    ThirtyDict[key] = iso_dtf(key, 'eq_capgain', 5)
    ThirtyDictBills[key] = iso_dtf(key, 'bill_rate', 5)
    ThirtyDict[key].insert(0, "Country", key, True)
    ThirtyDict[key].insert(1, "30yrsPeriods", blocks, True)
    ThirtyDictBills[key].insert(0, "Country", key, True)
    ThirtyDictBills[key].insert(1, "30yrsPeriods", blocks, True)

ThirtyDict['AUS']

overall30Dtf = pd.concat(ThirtyDict.values())
overall30DtfBills = pd.concat(ThirtyDictBills.values())


# Write the Results on a Excel Spread Sheet
writer = pd.ExcelWriter('DescriptiveStats_Output.xlsx', engine='xlsxwriter')
GSdtf.to_excel(writer, sheet_name='General Overview')
GSdtfBills.to_excel(writer, sheet_name='General Overview',
                    startrow=0, startcol=8)
overallDtfDC.to_excel(writer, sheet_name='Decades', index=False)
overallDtfBills.to_excel(writer, sheet_name='Decades',
                         startrow=0, startcol=10, index=False)
overall30Dtf.to_excel(writer, sheet_name='30yrs', index=False)
overall30DtfBills.to_excel(writer, sheet_name='30yrs',
                           startrow=0, startcol=10, index=False)
writer.save()

# 'AUS', 'BEL', 'CAN', 'CHE', 'DEU', 'DNK', 'ESP', 'FIN', 'FRA',
# 'GBR', 'IRL', 'ITA', 'JPN', 'NLD', 'NOR', 'PRT', 'SWE', 'USA'

# list_df = np.array_split(DataFrameDict['USA'], 5)
# list_df[0]

# years = DataFrameDict['USA'].year.unique()
# # Ylen = len(years)
# years
# # Ylen
# FC = years[:100] # First century From 1870 to 1969
# SC = years[100:] # Second Century from 1970 to 2019
#
# dtfFC = DataFrameDict['USA'].loc[DataFrameDict['USA'].year.isin(FC)]
# dtfSC = DataFrameDict['USA'].loc[DataFrameDict['USA'].year.isin(SC)]
#
# list_dfC = ((dtfFC, dtfSC))
# print(type(d))
#
# list_of_stats = {elem: [] for elem in range(0, 2)}
# list_of_stats
# for i in range(0, 2):
#     stata.pdataframe_to_data(list_dfC[i], force=True)
#     stata.run('summarize eq_capgain, detail')
#     # Get stats for each block
#     N = Scalar.getValue('r(N)')
#     mean = round(Scalar.getValue('r(mean)'), 3)
#     min = round(Scalar.getValue('r(min)'), 3)
#     max = round(Scalar.getValue('r(max)'), 3)
#     sd = round(Scalar.getValue('r(sd)'), 3)
#     sum = round(Scalar.getValue('r(sum)'), 3)
#     var = round(Scalar.getValue('r(Var)'), 3)
#     kurt = round(Scalar.getValue('r(kurtosis)'), 3)
#     skw = round(Scalar.getValue('r(skewness)'), 3)
#
#     # Append results to stats list_df
#     list_of_stats[i].extend((N, mean, min, max, sd, var, sum, kurt, skw))
#
#
# list_of_stats
# df = pd.DataFrame.from_dict(list_of_stats, orient = 'index')
# df
