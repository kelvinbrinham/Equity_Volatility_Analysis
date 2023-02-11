'''
Processing ALT DATA
'''


import statsmodels.api as sm
import numpy as np
import pandas as pd
import json as js
# import datetime as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp
import functions


from cleaning import stock_df_lst as stock_df_lst_clean


# List of chunked data
stock_df_processed_lst = []

# data_df = pd.read_csv('data/AAPL.csv')
data_df = pd.read_csv('data/ivv_HOURLY.csv')



stock_letter_df_clean = data_df
stock_letter_df_clean = stock_letter_df_clean.drop(columns = ['Open', 'High', 'Low', 'OpenInt'])
stock_letter_df_clean['Date'] = pd.to_datetime(stock_letter_df_clean['Date'] + ' ' + stock_letter_df_clean['Time'])
stock_letter_df_clean = stock_letter_df_clean.drop(columns = ['Time'])
stock_letter_df_clean['Date_ONLY'] = stock_letter_df_clean['Date'].dt.normalize()
stock_letter_df_clean = stock_letter_df_clean.set_index('Date')

stock_letter_df_clean['Date_ONLY'] = stock_letter_df_clean['Date_ONLY'] - stock_letter_df_clean['Date_ONLY'].shift()
stock_letter_df_clean['Date_ONLY'] = stock_letter_df_clean['Date_ONLY'].apply(functions.same_day)
stock_letter_df_clean['Date_ONLY'][0] = np.nan

stock_letter_df_clean = stock_letter_df_clean.reset_index()
day_indices_lst = stock_letter_df_clean.index[stock_letter_df_clean['Date_ONLY'] == 1].tolist()
stock_letter_df_clean = stock_letter_df_clean.set_index('Date')

stock_letter_df_chunk_lst = []
day_indices_lst.insert(0, 0)
for j in range(len(day_indices_lst) - 1):
    index_1 = day_indices_lst[j]
    index_2 = day_indices_lst[j + 1]
    stock_letter_df_chunk = stock_letter_df_clean.iloc[index_1:index_2, :]
    stock_letter_df_chunk_lst.append(stock_letter_df_chunk)


stock_letter_df_chunk_resampled_lst = []
for q in range(len(stock_letter_df_chunk_lst)):
    stock_df_chunk = stock_letter_df_chunk_lst[q]
    stock_df_chunk = stock_df_chunk.drop(columns = ['Date_ONLY'])
    
    stock_df_chunk['Return'] = np.log(stock_df_chunk['Close'] / stock_df_chunk.shift(1)['Close'])
    stock_df_chunk = stock_df_chunk.dropna()


    daily_volume = stock_df_chunk['Volume'].sum()

    length_ = len(stock_df_chunk)
    stock_df_chunk['Daily RV'] = stock_df_chunk['Return'].rolling(len(stock_df_chunk)).apply(functions.realised_volatility) / length_


    stock_df_chunk['Volume'][0] = daily_volume

    stock_df_chunk = stock_df_chunk.dropna()
    stock_df_chunk = stock_df_chunk.drop(columns = ['Close', 'Return'])

    stock_df_chunk = stock_df_chunk.rename(columns = {'Daily RV': 'RV', 'Volume': 'volume'})

    stock_letter_df_chunk_resampled_lst.append(stock_df_chunk)

data_df_FINAL = pd.concat(stock_letter_df_chunk_resampled_lst)

data_df_FINAL = data_df_FINAL.apply(sp.stats.zscore)
# data_df_FINAL.drop()
# print(data_df_FINAL)
# data_df_FINAL.to_excel('data/T.xlsx')

# data_df_FINAL = data_df_FINAL.drop(data_df_FINAL[data_df_FINAL.volume > 3].index)
# data_df_FINAL = data_df_FINAL.drop(data_df_FINAL[data_df_FINAL.volume < -3].index)
# data_df_FINAL = data_df_FINAL.drop(data_df_FINAL[data_df_FINAL.RV > 3].index)
# data_df_FINAL = data_df_FINAL.drop(data_df_FINAL[data_df_FINAL.RV < -3].index)


plt.plot(data_df_FINAL.volume, data_df_FINAL.RV, '.', markersize = 0.8)
a, b = np.polyfit(data_df_FINAL.volume, data_df_FINAL.RV, 1)
plt.plot(data_df_FINAL.volume, a * data_df_FINAL.volume + b, linewidth = 1, color = 'black')
plt.show()

# define predictor and response variables
# import statsmodels.api as sm
# y = data_df_FINAL.RV
# x = data_df_FINAL.volume

# #add constant to predictor variables
# x = sm.add_constant(x)

# #fit linear regression model
# model = sm.OLS(y, x).fit()

# #view model summary
# print(model.summary())

print(data_df_FINAL.corr(method = 'pearson'))

print(len(data_df_FINAL))

print('END')