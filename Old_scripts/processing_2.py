'''
Processing 2
'''

from statsmodels.tsa.stattools import grangercausalitytests
import numpy as np
import pandas as pd
import json as js
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp
import functions

from cleaning import stock_df_lst

#List of chunked data
stock_df_processed_lst = []



# for i in range(len(stock_df_lst)):
for i in range(4):
    #stock df from cleaning.py
    stock_letter_df = stock_df_lst[i]

    #list of chunked stock df, chunked by trading day
    stock_letter_df_chunked_lst = []

    # Set timestamp as index
    stock_letter_df = stock_letter_df.set_index('ts')

    #Create date (DATE ONLY NO TIME) column to chunk data with. normalise sets time componant to 0
    stock_letter_df['Date'] = pd.to_datetime(stock_letter_df.index)
    stock_letter_df['Date'] = stock_letter_df['Date'].dt.normalize()
    
    #Chunk dataframe into dataframes for each day
    stock_letter_df['Date'] = stock_letter_df['Date'] - stock_letter_df['Date'].shift()
    stock_letter_df['Date'] = stock_letter_df['Date'].apply(functions.same_day)
    stock_letter_df['Date'][0] = np.nan

    #Record indices for the rows where the day changes
    stock_letter_df = stock_letter_df.reset_index()
    day_indices_lst = stock_letter_df.index[stock_letter_df['Date'] == 1].tolist()
    stock_letter_df = stock_letter_df.set_index('ts')

    #Chunk data by day using above indices
    stock_letter_df_chunk_lst = []
    day_indices_lst.insert(0, 0)
    for j in range(len(day_indices_lst) - 1):
        index_1 = day_indices_lst[j]
        index_2 = day_indices_lst[j + 1]
        stock_letter_df_chunk = stock_letter_df.iloc[index_1:index_2, :]
        stock_letter_df_chunk_lst.append(stock_letter_df_chunk)

    
    #Resample data such that i have data for each 5 minute period
    stock_letter_df_chunk_resampled_lst = []
    for q in range(len(stock_letter_df_chunk_lst)):
        #1. Resample prices using previous tick method. 8:00 value just takes the first value from before
        stock_letter_df_chunk = stock_letter_df_chunk_lst[q]
        first_value = stock_letter_df_chunk['price'][0]
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk[['price']].resample('5min').ffill()
        stock_letter_df_chunk_resample_price['price'][0] = first_value

        #2. Resample volume by summing each 5 minute period
        stock_letter_df_chunk_resample_volume = stock_letter_df_chunk[['volume']].resample('5min', label='right', closed='right').sum()

        #3. Combine volume and price columns in one dataframe
        stock_letter_df_chunk_resample = pd.concat([stock_letter_df_chunk_resample_price, stock_letter_df_chunk_resample_volume], axis = 1)

        #4. Calculate 5-minute (log) return 
        stock_letter_df_chunk_resample['5-Minute (log) Return'] = np.log(stock_letter_df_chunk_resample['price'] / stock_letter_df_chunk_resample.shift(1)['price'])
        #Fill first value with mean from rest of first 30 minute slot
        stock_letter_df_chunk_resample['5-Minute (log) Return'][0] = np.mean(stock_letter_df_chunk_resample['5-Minute (log) Return'][1:6])
        
        #5. Calc. 30-minute realised volatility
        stock_letter_df_chunk_resample['30-minute rolling realised volatility'] = stock_letter_df_chunk_resample['5-Minute (log) Return'].rolling(6).apply(functions.realised_volatility)
        # stock_letter_df_chunk_resample['30-minute rolling realised volatility'] = stock_letter_df_chunk_resample['30-minute rolling realised volatility'].shift()
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.resample('30min').ffill()
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.drop(columns = ['5-Minute (log) Return', 'price'])
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.rename(columns = {'30-minute rolling realised volatility': '30-minute RV'})
        
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.dropna()

        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.rolling(len(stock_letter_df_chunk_resample)).mean()

        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.dropna()
        

        #Fixing missing 8:30 values in 4 of the days for stock C. I filled the volume and RV with the mean of the remaining days values.
        # if len(stock_letter_df_chunk_resample) != 15:
        #     df_ = stock_letter_df_chunk_resample.reset_index()
        #     new_first_line = pd.DataFrame([[df_['ts'][0] - timedelta(minutes = 30), df_['volume'].mean(), df_['30-minute RV'].mean()]], columns = df_.columns)
        #     df_ = pd.concat([new_first_line, df_])
        #     stock_letter_df_chunk_resample = df_.set_index('ts')
    
        stock_letter_df_chunk_resampled_lst.append(stock_letter_df_chunk_resample)

    # print([len(x) for x in stock_letter_df_chunk_resampled_lst])
    stock_data_processed_df = pd.concat(stock_letter_df_chunk_resampled_lst)
    stock_df_processed_lst.append(stock_data_processed_df)



for i in range(4):

    stock_A_df = stock_df_processed_lst[i]
    stock_A_df = stock_A_df.apply(sp.stats.zscore)
# print(stock_A_df.head())
# print(stock_A_df.tail())
# stock_A_df.to_excel('data/TEST.xlsx')

# print(len(stock_A_df))


# stock_A_df = stock_A_df[(stock_A_df.volume < 3) & (stock_A_df.volume > -3)]
# stock_A_df = stock_A_df[(stock_A_df['30-minute RV'] < 3) & (stock_A_df['30-minute RV'] > -3)]

# print(len(stock_A_df))

# stock_A_df.volume = stock_A_df.volume.shift(1)
# stock_A_df = stock_A_df.dropna()


# perform Granger-Causality test
# print(grangercausalitytests(stock_A_df[['30-minute RV', 'volume']], maxlag=[3]))
# print(grangercausalitytests(stock_A_df[['30-minute RV', 'volume']], 15))



    print(stock_A_df.corr(method = 'pearson'))

print('END')
