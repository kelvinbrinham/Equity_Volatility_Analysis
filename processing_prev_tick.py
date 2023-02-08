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
    #Resample on 5 minute periods using previous tick method
    # stock_letter_df_resample = stock_letter_df_processing.resample('5min').ffill().dropna()
    stock_letter_df_resample = stock_letter_df_processing.resample('5min').agg({'price': np.maximum, 'volume': np.sum})
    print(stock_letter_df_resample.head())

    #Remove entries outside market hours 08:00 - 16:30
    stock_letter_df_resample['Market Hours'] = pd.to_datetime(stock_letter_df_resample.index)
    stock_letter_df_resample['Market Hours'] = stock_letter_df_resample['Market Hours'].apply(market_hours)
    stock_letter_df_resample = stock_letter_df_resample.dropna()

    #Drop market hours column
    stock_letter_df_resample = stock_letter_df_resample.drop(['Market Hours'], axis=1)
    stock_df_processed_lst.append(stock_letter_df_resample)


print(stock_df_processed_lst[0].head())
