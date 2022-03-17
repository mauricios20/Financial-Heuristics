import os
import pandas as pd
import numpy as np
import stata_setup
stata_setup.config('/Applications/Stata', 'be')
from pystata import stata
from sfi import Scalar, Matrix


def iso_dtf(key, blocks):
    # 15 blocks takes 10 observations, decades
    list_df = np.array_split(DataFrameDict[key], blocks)
    list_of_stats = {elem: [] for elem in range(0, blocks)}
    for i in range(0, blocks):
        stata.pdataframe_to_data(list_df[i], force=True)
        stata.run('summarize eq_capgain, detail')
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
        list_of_stats[i].extend((N, mean, min, max, sd, var, sum, kurt, skw))

    df = pd.DataFrame.from_dict(list_of_stats, orient = 'index')
    # Rename columns DO NOT FORGERT
    return df
#  # #################### Load data ######################

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Heuristics/Data'
os.chdir(path)

dtf = pd.read_csv('JSTdatasetR5.csv', header=0,
                    usecols=['year', 'iso', 'eq_capgain', 'eq_dp'])

# Create dataframes for each country into countries
countries = dtf.iso.unique()
dummy_years = [(2018), (2019), (2020)]
dummy_dtf = pd.DataFrame(dummy_years, columns = ['year'])
DataFrameDict = {elem: pd.DataFrame for elem in countries}
list_df = {elem: [] for elem in countries}


for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf[dtf['iso'] == key]
    DataFrameDict[key] = DataFrameDict[key].append(dummy_dtf, ignore_index=True)
    # Split into 15 chuncks of 10 years
    list_df[key] = np.array_split(DataFrameDict[key], 15)

# Performe stata commands in all the splits
FinalFrameDict = {elem: pd.DataFrame for elem in countries}
for key in FinalFrameDict.keys():
    FinalFrameDict[key] = iso_dtf(key, 15)

FinalFrameDict['PRT']


# list_df = np.array_split(DataFrameDict['USA'], 15)
# list_of_stats = {elem: [] for elem in range(0, 15)}
# list_of_stats
# for i in range(0, 15):
#     stata.pdataframe_to_data(list_df[i], force=True)
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
#
#
#     # Append results to stats list_df
#     list_of_stats[i].extend((N, mean, min, max, sd, var, sum, kurt, skw))
#
#
# list_of_stats
# df = pd.DataFrame.from_dict(list_of_stats, orient = 'index')
# df
