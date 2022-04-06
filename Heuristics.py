import os
import pandas as pd
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

for key in countries:
    print(key)
    ResultsDtfDict[key], StatisticDict[key] = heuristics(
        DataFrameDict[key], 0, 0.025, 15)

writer = pd.ExcelWriter(
    'Heuristics_Analysis_Decades.xlsx', engine='xlsxwriter')
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


# print(ResultsDtfDict['USA'][['Recency', '60/40',
#       'AllStocks', '2down', 'Naive', 'RecencyV2']])
