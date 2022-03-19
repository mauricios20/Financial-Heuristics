import os
import pandas as pd
import numpy as np
import stata_setup
import xlsxwriter
stata_setup.config('/Applications/Stata', 'be')
from pystata import stata
from sfi import Scalar, Matrix


# Function for Decades and 30 year blocks


def iso_dtf(key, x, blocks):
    # 15 blocks takes 10 observations, decades
    command = 'summarize '+x+', '+'detail'
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


# Function for Centuries
def iso_dtfC(key, x, blocks):
    # See how many years and slice by century
    years = DataFrameDict[key].year.unique()
    FC = years[:100]  # First century From 1870 to 1969
    SC = years[100:]  # Second Century from 1970 to 2019

    command = 'summarize '+x+', '+'detail'
    # Create data frames for each century
    dtfFC = DataFrameDict[key].loc[DataFrameDict[key].year.isin(FC)]
    dtfSC = DataFrameDict[key].loc[DataFrameDict[key].year.isin(SC)]
    list_dfC = ((dtfFC, dtfSC))

    list_of_stats = {elem: [] for elem in range(0, blocks)}
    for i in range(0, blocks):
        stata.pdataframe_to_data(list_dfC[i], force=True)
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
#  # #################### Load data ######################


path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Heuristics/Data'
os.chdir(path)

dtf = pd.read_csv('JSTdatasetR5.csv', header=0,
                    usecols=['year', 'iso', 'eq_capgain', 'eq_dp'])

# Create dataframes for each country into countries
countries = dtf.iso.unique()
dummy_years = [(2018), (2019)]
dummy_dtf = pd.DataFrame(dummy_years, columns=['year'])
DataFrameDict = {elem: pd.DataFrame for elem in countries}
list_df = {elem: [] for elem in countries}


for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf[dtf['iso'] == key]
    DataFrameDict[key] = DataFrameDict[key].append(dummy_dtf, ignore_index=True)

# # Performe stata commands in all the decades
DecadeDict = {elem: pd.DataFrame for elem in countries}
for key in DecadeDict.keys():
    DecadeDict[key] = iso_dtf(key, 'eq_capgain', 15)

DecadeDict['ITA']
# Write the Results on a Excel Spread Sheet
writer = pd.ExcelWriter('Decades_Output.xlsx', engine='xlsxwriter')
for key in DecadeDict:
    DecadeDict[key].to_excel(writer, sheet_name=key)
writer.save()

# # Performe stata commands in all the 30 year blocks
ThirtyDict = {elem: pd.DataFrame for elem in countries}
for key in ThirtyDict.keys():
    ThirtyDict[key] = iso_dtf(key, 'eq_capgain', 5)

ThirtyDict['AUS']
# Write the Results on a Excel Spread Sheet
writer = pd.ExcelWriter('Thirty_Output.xlsx', engine='xlsxwriter')
for key in ThirtyDict:
    ThirtyDict[key].to_excel(writer, sheet_name=key)
writer.save()

# 'AUS', 'BEL', 'CAN', 'CHE', 'DEU', 'DNK', 'ESP', 'FIN', 'FRA',
# 'GBR', 'IRL', 'ITA', 'JPN', 'NLD', 'NOR', 'PRT', 'SWE', 'USA'

# # Performe stata commands in all the 100 year blocks
CenturyDict = {elem: pd.DataFrame for elem in countries}
for key in CenturyDict.keys():
    CenturyDict[key] = iso_dtfC(key, 'eq_capgain', 2)

CenturyDict['AUS']
# Write the Results on a Excel Spread Sheet
writer = pd.ExcelWriter('Century_Output.xlsx', engine='xlsxwriter')
for key in CenturyDict:
    CenturyDict[key].to_excel(writer, sheet_name=key)
writer.save()


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