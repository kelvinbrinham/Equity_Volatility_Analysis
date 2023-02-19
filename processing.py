'''
Processing

Here RV is calculated from 5-minute prices each day. 
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

from cleaning import stock_df_lst as stock_df_lst_clean

stock_string = 'ABCD'

#Dictionary to hold the correct number of 5-minute return slots for each trading day for each stock
stock_data_length_dict = {'A': 101, 'B': 101, 'C': 95, 'D': 95}

#List holding df for each stock
stock_df_processed_lst = [] 

#Loop over each stock
for i in range(len(stock_df_lst_clean)):
    #Load stock df from cleaning.py
    stock_letter_df_clean = stock_df_lst_clean[i]

    #List to hold df for each trading day
    stock_letter_df_chunked_lst = []

    # Set timestamp as index
    stock_letter_df_processing = stock_letter_df_clean.set_index('ts')

    #Create date column so as to chunk dataframe by day
    stock_letter_df_processing['Date'] = pd.to_datetime(stock_letter_df_processing.index)
    #Remove time component of datetime
    stock_letter_df_processing['Date'] = stock_letter_df_processing['Date'].dt.normalize()

    #Chunk dataframe into dataframes for each day
    stock_letter_df_processing['Date'] = stock_letter_df_processing['Date'] - stock_letter_df_processing['Date'].shift()
    stock_letter_df_processing['Date'] = stock_letter_df_processing['Date'].apply(functions.same_day)
    stock_letter_df_processing['Date'][0] = np.nan

    stock_letter_df_processing = stock_letter_df_processing.reset_index()
    
    #Note the indices where the df changes day
    day_indices_lst = stock_letter_df_processing.index[stock_letter_df_processing['Date'] == 1].tolist()
    stock_letter_df_processing = stock_letter_df_clean.set_index('ts')

    #Chunk stock df into df for each day
    stock_letter_df_chunk_lst = []
    day_indices_lst.insert(0, 0)
    for j in range(len(day_indices_lst) - 1):
        index_1 = day_indices_lst[j]
        index_2 = day_indices_lst[j + 1]
        stock_letter_df_chunk = stock_letter_df_processing.iloc[index_1:index_2, :]
        stock_letter_df_chunk_lst.append(stock_letter_df_chunk)

    #List to hold the processed df for each day
    stock_letter_df_chunk_resampled_lst = []
    #Loop over each chunk/day
    for q in range(len(stock_letter_df_chunk_lst)):
        stock_letter_df_chunk = stock_letter_df_chunk_lst[q]

        #Calculate daily return using closing prices
        close_price = stock_letter_df_chunk['price'][-1]
        # daily_return = np.log(close_price / open_price)

        # 1. Resample prices using previous tick method for price. (First value just takes first value from before)
        first_value = stock_letter_df_chunk['price'][0]
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk[['price']].resample('5min').ffill()
        stock_letter_df_chunk_resample_price['price'][0] = first_value
        
        #2. Work out daily volume
        daily_volume = stock_letter_df_chunk['volume'].sum()

        #3. Calculate 5-minute return 
        stock_letter_df_chunk_resample_price['5-Minute (log) Return'] = np.log(stock_letter_df_chunk_resample_price['price'] / stock_letter_df_chunk_resample_price.shift(1)['price'])
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.dropna()
        
        #4. Check number of 5 minute intervals. 
        #The number is only incorrect once, the chunk in question has the 08:05 value missing which i replace with the chunk mean this once through hardcoding. 
        stock_letter = stock_string[i]
        if len(stock_letter_df_chunk_resample_price) != stock_data_length_dict[stock_letter]:
            stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.reset_index()
            stock_letter_df_chunk_resample_price.loc[-1] = [(stock_letter_df_chunk_resample_price['ts'][0] - timedelta(hours=0, minutes=5)), stock_letter_df_chunk_resample_price['price'].mean(), stock_letter_df_chunk_resample_price['5-Minute (log) Return'].mean()]
            stock_letter_df_chunk_resample_price.index = stock_letter_df_chunk_resample_price.index + 1  # shifting index
            stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.sort_index() 
            stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.set_index('ts') 
            stock_letter_df_chunk_resample_price.to_excel('data/TEST.xlsx')
        


        #5. Calculate daily realised volatility using square sum of 5-minute returns
        stock_letter_df_chunk_resample_price['Daily RV'] = stock_letter_df_chunk_resample_price['5-Minute (log) Return'].rolling(len(stock_letter_df_chunk_resample_price)).apply(functions.realised_volatility)
        # stock_letter_df_chunk_resample_price['5-minute return sum'] = stock_letter_df_chunk_resample_price['5-Minute (log) Return'].rolling(len(stock_letter_df_chunk_resample_price)).sum()
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.dropna()

        #6. Add daily volume and RV to new dataframe
        stock_letter_df_chunk_resample_price['volume'] = np.nan
        stock_letter_df_chunk_resample_price['volume'][0] = daily_volume
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.drop(columns = ['price', '5-Minute (log) Return'])
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample_price

        #Formatting
        stock_letter_df_chunk_resample['RV'] = stock_letter_df_chunk_resample['Daily RV']
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.drop(['Daily RV'], axis = 1)
        # stock_letter_df_chunk_resample['Daily Return'] = [daily_return]
        stock_letter_df_chunk_resample['Close'] = [close_price]
    
      
        #---
        #Add df daily chunk to stock_letter_df_chunk_resampled_lst
        stock_letter_df_chunk_resampled_lst.append(stock_letter_df_chunk_resample)

    #Combine daily data into one df for this stock
    stock_data_processed_df = pd.concat(stock_letter_df_chunk_resampled_lst)

    #Add this stocks final df to stock_df_processed_lst
    stock_df_processed_lst.append(stock_data_processed_df)





#Print correlation matrix for each stock
if __name__ == '__main__':
    for i in range(4):
        string = 'ABCD'

        print('--------------')
        print('Stock ', string[i])
        stock_letter_df = stock_df_processed_lst[i]

        #Apply z-score (in case of plotting)
        stock_letter_df = stock_letter_df.apply(sp.stats.zscore)

        print(stock_letter_df.corr('pearson'))
        print('--------------')



print('END 2')


