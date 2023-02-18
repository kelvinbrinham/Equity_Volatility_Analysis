'''
Processing alternative (hourly) data (AAPL, S&P500...)
'''


import statsmodels.api as sm
import numpy as np
import pandas as pd
import json as js
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp
import functions


#Import data (downloaded from Kaggle)
# data_df = pd.read_csv('data/AAPL.csv')
data_df = pd.read_csv('data/ivv_HOURLY.csv')


#Data from Kaggle already clean
stock_letter_df_clean = data_df

#Format df to inc. variables of importance
stock_letter_df_clean = stock_letter_df_clean.drop(columns = ['Open', 'High', 'Low', 'OpenInt'])
stock_letter_df_clean['Date'] = pd.to_datetime(stock_letter_df_clean['Date'] + ' ' + stock_letter_df_clean['Time'])
stock_letter_df_clean = stock_letter_df_clean.drop(columns = ['Time'])
stock_letter_df_clean['Date_ONLY'] = stock_letter_df_clean['Date'].dt.normalize()
stock_letter_df_clean = stock_letter_df_clean.set_index('Date')


stock_letter_df_clean['Date_ONLY'] = stock_letter_df_clean['Date_ONLY'] - stock_letter_df_clean['Date_ONLY'].shift()
stock_letter_df_clean['Date_ONLY'] = stock_letter_df_clean['Date_ONLY'].apply(functions.same_day)
stock_letter_df_clean['Date_ONLY'][0] = np.nan

#Note indices in df where the day changes (This method could be made simpler by assuming the same number of slots per day
# and that the data is therefore already perfectly clean)
stock_letter_df_clean = stock_letter_df_clean.reset_index()
day_indices_lst = stock_letter_df_clean.index[stock_letter_df_clean['Date_ONLY'] == 1].tolist()
stock_letter_df_clean = stock_letter_df_clean.set_index('Date')

#Chunk data by day
stock_letter_df_chunk_lst = []
day_indices_lst.insert(0, 0)
for j in range(len(day_indices_lst) - 1):
    index_1 = day_indices_lst[j]
    index_2 = day_indices_lst[j + 1]
    stock_letter_df_chunk = stock_letter_df_clean.iloc[index_1:index_2, :]
    stock_letter_df_chunk_lst.append(stock_letter_df_chunk)


#Loop over each day
stock_letter_df_chunk_resampled_lst = []
for q in range(len(stock_letter_df_chunk_lst)):
    stock_df_chunk = stock_letter_df_chunk_lst[q]
    stock_df_chunk = stock_df_chunk.drop(columns = ['Date_ONLY'])
    
    #Calculate hourly return
    stock_df_chunk['Return'] = np.log(stock_df_chunk['Close'] / stock_df_chunk.shift(1)['Close'])
    stock_df_chunk = stock_df_chunk.dropna()

    #Calc. daily volume
    daily_volume = stock_df_chunk['Volume'].sum()

    #Calculate daily RV using hourly returns
    length_ = len(stock_df_chunk)
    stock_df_chunk['Daily RV'] = stock_df_chunk['Return'].rolling(len(stock_df_chunk)).apply(functions.realised_volatility) / length_

    #Formatting
    stock_df_chunk['Volume'][0] = daily_volume

    stock_df_chunk = stock_df_chunk.dropna()
    stock_df_chunk = stock_df_chunk.drop(columns = ['Close', 'Return'])

    stock_df_chunk = stock_df_chunk.rename(columns = {'Daily RV': 'RV', 'Volume': 'volume'})

    #Add daily df to stock_letter_df_chunk_resampled_lst
    stock_letter_df_chunk_resampled_lst.append(stock_df_chunk)

#Combine daily data into one df for the ~6 month period
data_df_FINAL = pd.concat(stock_letter_df_chunk_resampled_lst)

#Normalise data
data_df_FINAL = data_df_FINAL.apply(sp.stats.zscore)


# plt.plot(data_df_FINAL.volume, data_df_FINAL.RV, '.', markersize = 0.8)
# a, b = np.polyfit(data_df_FINAL.volume, data_df_FINAL.RV, 1)
# plt.plot(data_df_FINAL.volume, a * data_df_FINAL.volume + b, linewidth = 1, color = 'black')
# plt.show()

#Calculate pearson correlation
print(data_df_FINAL.corr(method = 'pearson'))



print('END')