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

    # stock_letter_df_volume_resample = stock_letter_df_processing[['volume']].resample('5min', label='right', closed='right').sum()
    stock_letter_df_volume_resample = stock_letter_df_processing[['volume']].resample('5min').sum()

    #Remove entries outside market hours 08:00 - 16:30
    stock_letter_df_resample['Market Hours'] = pd.to_datetime(stock_letter_df_resample.index)
    stock_letter_df_resample['Market Hours'] = stock_letter_df_resample['Market Hours'].apply(market_hours)
    stock_letter_df_resample = stock_letter_df_resample.dropna()

    #Drop market hours column
    stock_letter_df_resample = stock_letter_df_resample.drop(['Market Hours'], axis=1)
    stock_df_processed_lst.append(stock_letter_df_resample)


# print(stock_df_processed_lst[0].head())
