from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sb
import scipy.stats as stats

from pandas import Series, DataFrame, merge
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

#Oil and Gold
oilDataFile = 'CRUDE_OIL_30_years.csv'
goldDataFile = 'GOLD_30_years.csv'
#Factors
sp500DataFile = 'SP500_INDEX_30_years.csv'
nyseDataFile = 'NYSE_INDEX_30_years.csv'
usdIndexDataFile = 'USD_30_years.csv'
csiDataFile = 'CSI_30_years.csv'
infDataFile = 'INF_30_years.csv'

#CPI - For Inflation Adjustment
cpiDataFile = 'CPI_30_years.csv'

#Read CSV to pandas data frame
dfOil = pd.read_csv(oilDataFile)
dfGold = pd.read_csv(goldDataFile)

dfSP500 = pd.read_csv(sp500DataFile)
dfNyse = pd.read_csv(nyseDataFile)
dfUsInd = pd.read_csv(usdIndexDataFile)
dfCsi = pd.read_csv(csiDataFile)

dfCpi = pd.read_csv(cpiDataFile)

def Inflation_adjustments(quantity):
    return quantity * (dfCpi['CPI'][0]/dfCpi['CPI']) 

dfOil['Oil_Value'] = Inflation_adjustments(dfOil['Oil_Value'])
dfGold['Gold_Value'] = Inflation_adjustments(dfGold['Gold_Value'])
dfSP500['SP500_Value'] = Inflation_adjustments(dfSP500['SP500_Value'])
dfNyse['NYSE_Value'] = Inflation_adjustments(dfNyse['NYSE_Value'])
dfUsInd['USD_Value'] = Inflation_adjustments(dfUsInd['USD_Value'])
dfCsi['CSI_Value'] = Inflation_adjustments(dfCsi['CSI_Value'])

def Oil_Data_Frame_Generator():
    merged_data_frame = merge(dfOil,dfSP500,on='Date',how='inner')
    merged_data_frame = merge(merged_data_frame,dfNyse,on='Date',how='inner')
    merged_data_frame = merge(merged_data_frame,dfUsInd,on='Date',how='inner')
    merged_data_frame = merge(merged_data_frame,dfGold,on='Date',how='inner')     
    candidatesListOil = ['Oil_Value','SP500_Value','NYSE_Value','USD_Value','Gold_Value']
    return merged_data_frame, candidatesListOil

def Gold_Data_Frame_Generator():
    merged_data_frame = merge(dfGold,dfSP500,on='Date',how='inner')
    merged_data_frame = merge(merged_data_frame,dfNyse,on='Date',how='inner')
    merged_data_frame = merge(merged_data_frame,dfUsInd,on='Date',how='inner')
    merged_data_frame = merge(merged_data_frame,dfCsi,on='Date',how='inner')
    merged_data_frame = merge(merged_data_frame,dfOil,on='Date',how='inner')
    candidatesListGold = ['Gold_Value','SP500_Value','NYSE_Value','USD_Value','CSI_Value','Oil_Value']
    return merged_data_frame, candidatesListGold

def computeCorrelation(dataFrame, candidatesList,name):
    fig, axes = plt.subplots(figsize=(12,12))
    dfCorr = dataFrame[candidatesList]
    cmap = sb.blend_palette(["#6B229F", "#FD3232", "#F66433",
                          "#E78520", "#FFBB39"], as_cmap=True)
    sb.corrplot(dfCorr, annot=False, sig_stars=False,
             diag_names=False, cmap=cmap)
    axes.set_title("Correlation Matrix - " + name )
    plt.savefig('Correlation_'+candidatesList[0]+'_.png')
    
merged_data_frameOil,candidatesListOil = Oil_Data_Frame_Generator()
print(merged_data_frameOil)
print(candidatesListOil)
    
computeCorrelation(merged_data_frameOil,candidatesListOil, "Oil")

merged_data_frameGold,candidatesListGold = Gold_Data_Frame_Generator()
computeCorrelation(merged_data_frameGold,candidatesListGold, "Gold")
