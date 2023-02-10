'''
Processing
'''

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



#List of chunked data
stock_df_processed_lst = []

# for i in range(len(stock_df_lst_clean)):
for i in range(4):
    stock_letter_df_clean = stock_df_lst_clean[i]
    stock_letter_df_chunked_lst = []

    # Set timestamp as index
    stock_letter_df_processing = stock_letter_df_clean.set_index('ts')

    #Create date column so as to chunk dataframes
    stock_letter_df_processing['Date'] = pd.to_datetime(stock_letter_df_processing.index)
    stock_letter_df_processing['Date'] = stock_letter_df_processing['Date'].dt.normalize()
    # stock_letter_df_processing['Date'] = stock_letter_df_processing['Date'].dt.date

    #Chunk dataframe into dataframes for each day
    stock_letter_df_processing['Date'] = stock_letter_df_processing['Date'] - stock_letter_df_processing['Date'].shift()
    stock_letter_df_processing['Date'] = stock_letter_df_processing['Date'].apply(functions.same_day)
    stock_letter_df_processing['Date'][0] = np.nan

    # stock_letter_df_processing = stock_letter_df_processing[:1600] #TESTING
    stock_letter_df_processing = stock_letter_df_processing.reset_index()
    
    day_indices_lst = stock_letter_df_processing.index[stock_letter_df_processing['Date'] == 1].tolist()
    stock_letter_df_processing = stock_letter_df_clean.set_index('ts')

    stock_letter_df_chunk_lst = []
    day_indices_lst.insert(0, 0)
    for j in range(len(day_indices_lst) - 1):
        index_1 = day_indices_lst[j]
        index_2 = day_indices_lst[j + 1]
        stock_letter_df_chunk = stock_letter_df_processing.iloc[index_1:index_2, :]
        stock_letter_df_chunk_lst.append(stock_letter_df_chunk)

    
    stock_letter_df_chunk_resampled_lst = []
    for q in range(len(stock_letter_df_chunk_lst)):
        #1. Resample prices using previous tick method for price. (First value just takes first value from before)
        stock_letter_df_chunk = stock_letter_df_chunk_lst[q]


        first_value = stock_letter_df_chunk['price'][0]
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk[['price']].resample('5min').ffill()
        stock_letter_df_chunk_resample_price['price'][0] = first_value
        
        #2. Work out daily volume
        daily_volume = stock_letter_df_chunk['volume'].sum()

        #3. Calculate 5-minute return 
        stock_letter_df_chunk_resample_price['5-Minute (log) Return'] = np.log(stock_letter_df_chunk_resample_price['price'] / stock_letter_df_chunk_resample_price.shift(1)['price'])
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.dropna()

        #4. Calculate daily realised volatility using square sum of 5-miute returns
        stock_letter_df_chunk_resample_price['Daily RV'] = stock_letter_df_chunk_resample_price['5-Minute (log) Return'].rolling(len(stock_letter_df_chunk_resample_price)).apply(functions.realised_volatility)
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.dropna()

        #5. Add daily volume and RV to new dataframe
        stock_letter_df_chunk_resample_price['volume'] = np.nan
        stock_letter_df_chunk_resample_price['volume'][0] = daily_volume
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.drop(columns = ['price', '5-Minute (log) Return'])
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample_price

        #Formatting
        stock_letter_df_chunk_resample['RV'] = stock_letter_df_chunk_resample['Daily RV']
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.drop(['Daily RV'], axis = 1)
      
        #---
        stock_letter_df_chunk_resampled_lst.append(stock_letter_df_chunk_resample)

            
    stock_data_processed_df = pd.concat(stock_letter_df_chunk_resampled_lst)

    stock_df_processed_lst.append(stock_data_processed_df)


# stock_df_processed_lst[0].to_excel('data/T.xlsx')

for i in range(4):

    stock_A_df = stock_df_processed_lst[i]
    stock_A_df = stock_A_df.apply(sp.stats.zscore)

    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df.volume > 3].index)
    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df.volume < -3].index)
    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df.RV < -3].index)
    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df.RV > 3].index)

    # stock_A_df.RV = stock_A_df.RV.shift(1)
    # stock_A_df = stock_A_df.dropna()


    # plt.figure()
    # plt.plot(stock_A_df.volume, stock_A_df.RV, '.', markersize = 0.8)

    # a, b = np.polyfit(stock_A_df.volume, stock_A_df.RV, 1)
    # plt.plot(stock_A_df.volume, a * stock_A_df.volume + b)


    print(stock_A_df.corr('pearson').iloc[0,1])
    print(stock_A_df.corr('kendall').iloc[0,1])
    print(stock_A_df.corr('spearman').iloc[0,1])
    print('--------')


print('END')


