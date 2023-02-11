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


from cleaning import cleaning_stats_df
from cleaning import stock_df_lst as stock_df_lst_clean
from cleaning import market_hours


def RealisedVolatility(x):
    return np.sqrt(sum([y ** 2 for y in x]))

def Same_day(x):
    if not x:
        return np.nan

    else:
        return 1


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
    stock_letter_df_processing['Date'] = stock_letter_df_processing['Date'].apply(Same_day)
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
        #1. Resample prices using previous tick method. (First value just takes first value from before)
        stock_letter_df_chunk = stock_letter_df_chunk_lst[q]
        first_value = stock_letter_df_chunk['price'][0]
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk[['price']].resample('5min').ffill()
        stock_letter_df_chunk_resample_price['price'][0] = first_value
        
        #2. Resample volume by summing volume for each 5 min period. First value just takes first value as before
        stock_letter_df_chunk_resample_volume = stock_letter_df_chunk[['volume']].resample('5min', label='right', closed='right').sum()

        #3. Combine volume and price columns in one dataframe
        stock_letter_df_chunk_resample = pd.concat([stock_letter_df_chunk_resample_price, stock_letter_df_chunk_resample_volume], axis = 1)
        # stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.dropna()

        #4. Calculate 5-minute retusn 
        stock_letter_df_chunk_resample['5-Minute (log) Return'] = np.log(stock_letter_df_chunk_resample['price'] / stock_letter_df_chunk_resample.shift(1)['price'])
        # stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.dropna()

        #5. Calculate 30-minute realised volatility using square sum of 5-miute returns
        stock_letter_df_chunk_resample['30-minute rolling realised volatility'] = stock_letter_df_chunk_resample['5-Minute (log) Return'].rolling(6).apply(RealisedVolatility)
        # stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.dropna()

        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.resample('30min').ffill()
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.drop(columns = ['5-Minute (log) Return', 'price'])
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.rename(columns = {'30-minute rolling realised volatility': '30-minute RV'})


        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.dropna()
        #---
        stock_letter_df_chunk_resampled_lst.append(stock_letter_df_chunk_resample)

        #Fixing missing 8:30 values in 4 of the days for stock C. I filled the volume and RV with the mean of the remaining days values.
        if len(stock_letter_df_chunk_resample) != 15:
            df_ = stock_letter_df_chunk_resample.reset_index()
            new_first_line = pd.DataFrame([[df_['ts'][0] - timedelta(minutes = 30), df_['volume'].mean(), df_['30-minute RV'].mean()]], columns = df_.columns)
            df_ = pd.concat([new_first_line, df_])
            stock_letter_df_chunk_resample = df_.set_index('ts')

            
    stock_data_processed_df = pd.concat(stock_letter_df_chunk_resampled_lst)

    #Calculate prior day rolling average volatility 
    stock_data_processed_df['Prior Day Rolling Average Trading Volume'] = stock_data_processed_df['volume'].rolling(15).mean()

    stock_data_processed_df['Prior Day Rolling Average RV'] = stock_data_processed_df['30-minute RV'].rolling(15).mean()


    stock_data_processed_df = stock_data_processed_df.dropna()


    stock_df_processed_lst.append(stock_data_processed_df)




# print('END')

