'''
Processing using previous tick method
'''


import numpy as np
import pandas as pd
import json as js
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp



from cleaning import cleaning_stats_df
from cleaning import stock_df_lst as stock_df_lst_clean
from cleaning import market_hours



def RealisedVolatility(x):
    return np.sqrt(sum([y ** 2 for y in x]))

def is_5_minutes(x):
    if x.total_seconds() == 300:
        return x
    else:
        return np.nan

stock_df_processed_lst = []


#Equally space data using previous tick method, i will use 5 minute data
# for i in range(len(stock_df_lst_clean)):
for i in range(1):
    stock_letter_df_clean = stock_df_lst_clean[i]

    #Set timestamp as index
    stock_letter_df_processing = stock_letter_df_clean.set_index('ts')
    #Resample on 5 minute periods using previous tick method for prices and summation for volume.
    #Unfortunately, pandas has no reliable way (I can find) to resample using different functions for different columns
    #Therefore, I split my data into two data frames, resample and then recombine into one dataframe
    #1. Resample prices using previous tick method. (First value just takes first value from before)
    first_value = stock_letter_df_processing['price'][0]
    stock_letter_df_price_resample = stock_letter_df_processing[['price']].resample('5min').ffill()
    stock_letter_df_price_resample['price'][0] = first_value

    #2. Resample volume by summing volume for each 5 min period. First value just takes first value as before
    stock_letter_df_volume_resample = stock_letter_df_processing[['volume']].resample('5min', label='right', closed='right').sum()
    
    stock_letter_df_resample = pd.concat([stock_letter_df_price_resample, stock_letter_df_volume_resample], axis = 1)

    #Remove entries outside market hours 08:00 - 16:00
    stock_letter_df_resample['Market Hours'] = pd.to_datetime(stock_letter_df_resample.index)
    stock_letter_df_resample['Market Hours'] = stock_letter_df_resample['Market Hours'].apply(market_hours)
    stock_letter_df_resample = stock_letter_df_resample.dropna()

    #Drop market hours column
    stock_letter_df_resample = stock_letter_df_resample.drop(['Market Hours'], axis=1)
    stock_df_processed_lst.append(stock_letter_df_resample)

    #Calculate 5-minute return (just difference in price between rows because i have spaced the data on 5 minute intervals)
    stock_letter_df_resample['5-Minute (log) Return'] = np.log(stock_letter_df_resample['price'] / stock_letter_df_resample.shift(1)['price'])
    # stock_letter_df_resample = stock_letter_df_resample.dropna()
    # stock_letter_df_resample['5-Minute (log) Return'][0] = stock_letter_df_resample['5-Minute (log) Return'][1:6].mean()

    #Drop duplicate returns (non buisness days)
    stock_letter_df_resample = stock_letter_df_resample.drop_duplicates(subset = '5-Minute (log) Return')

    #Drop returns that span > 5-minutes (i.e. returns overnight)
    stock_letter_df_resample['Time Difference'] = pd.to_datetime(stock_letter_df_resample.index)
    stock_letter_df_resample['Time Difference'] = stock_letter_df_resample['Time Difference'] - stock_letter_df_resample['Time Difference'].shift()
    stock_letter_df_resample.to_excel('data/5_minute.xlsx')
    stock_letter_df_resample['Time Difference'] = stock_letter_df_resample['Time Difference'].apply(is_5_minutes)
    stock_letter_df_resample.to_excel('data/5_minute_2.xlsx')

    break

    #Calculate 30-minute realised volatility using the square sum of 5-minute returns for each 30 minute period
    stock_letter_df_resample['30-minute rolling realised volatility'] = stock_letter_df_resample['5-Minute (log) Return'].rolling(6).apply(RealisedVolatility)
    stock_letter_df_resample = stock_letter_df_resample.dropna()
    print(stock_letter_df_resample[:20])


    #Resample only each 30-minute period
    stock_letter_df_resample = stock_letter_df_resample.resample('30min').ffill()
    stock_letter_df_resample = stock_letter_df_resample.drop_duplicates(subset = '30-minute rolling realised volatility')
    print(stock_letter_df_resample[:20])




   

