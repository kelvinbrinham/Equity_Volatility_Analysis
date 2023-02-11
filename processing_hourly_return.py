'''
processing hourly RV
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

stock_string = 'ABCD'
stock_data_length_dict = {'A': 8, 'B': 8, 'C': 7, 'D': 7}

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
        open_price = stock_letter_df_chunk['price'][0]
        close_price = stock_letter_df_chunk['price'][-1]
        daily_return = np.log(close_price / open_price)


        first_value = stock_letter_df_chunk['price'][0]
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk[['price']].resample('5min').ffill() #HERE
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.resample('60min').mean() #HERE
        stock_letter_df_chunk_resample_price['price'][0] = first_value
        
        #2. Work out daily volume
        daily_volume = stock_letter_df_chunk['volume'].sum()

        #3. Calculate hourly return 
        stock_letter_df_chunk_resample_price['1-hour (log) Return'] = np.log(stock_letter_df_chunk_resample_price['price'] / stock_letter_df_chunk_resample_price.shift(1)['price'])
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.dropna()

        #4. Check number of 1-hour intervals. 
        stock_letter = stock_string[i]
        if len(stock_letter_df_chunk_resample_price) != stock_data_length_dict[stock_letter]:
            print('HERE = ', len(stock_letter_df_chunk_resample_price))
            raise Exception('Data Unequal')


        #5. Calculate daily realised volatility using square sum of 5-miute returns
        stock_letter_df_chunk_resample_price['Daily RV'] = stock_letter_df_chunk_resample_price['1-hour (log) Return'].rolling(len(stock_letter_df_chunk_resample_price)).apply(functions.realised_volatility)
        stock_letter_df_chunk_resample_price.to_excel('data/T.xlsx')
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.dropna()


        #6. Add daily volume and RV to new dataframe
        stock_letter_df_chunk_resample_price['volume'] = np.nan
        stock_letter_df_chunk_resample_price['volume'][0] = daily_volume
        stock_letter_df_chunk_resample_price = stock_letter_df_chunk_resample_price.drop(columns = ['price', '1-hour (log) Return'])
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample_price

        

        #Formatting
        stock_letter_df_chunk_resample['RV'] = stock_letter_df_chunk_resample['Daily RV']
        stock_letter_df_chunk_resample = stock_letter_df_chunk_resample.drop(['Daily RV'], axis = 1)
        # stock_letter_df_chunk_resample['Daily Return'] = [daily_return]
    
      
        #---
        stock_letter_df_chunk_resampled_lst.append(stock_letter_df_chunk_resample)

            
    stock_data_processed_df = pd.concat(stock_letter_df_chunk_resampled_lst)

    stock_df_processed_lst.append(stock_data_processed_df)



stock_A_df = stock_df_processed_lst[0]

plt.figure()
plt.plot(stock_A_df.index, stock_A_df.RV)
plt.show()


print('END')