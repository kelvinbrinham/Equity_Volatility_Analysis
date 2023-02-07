'''
Processing
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

#Normalize data 
# for i in range(len(stock_df_lst_clean)):
for i in range(1):

    stock_letter_df_clean = stock_df_lst_clean[i]
    # print(stock_A_df_clean.describe())

    # numeric_columns = stock_A_df_clean.select_dtypes(include=[np.number]).columns
    # stock_A_df_clean[numeric_columns] = stock_A_df_clean[numeric_columns].apply(sp.stats.zscore)


    stock_letter_df_processing = stock_letter_df_clean.set_index('ts')

    plt.figure()
    stock_letter_df_processing.price.plot()


    stock_letter_df_processing = stock_letter_df_processing.resample('s').mean()
    stock_letter_df_interpolated = stock_letter_df_processing.interpolate(limit_direction = 'both')
    stock_letter_df_resample = stock_letter_df_interpolated.resample('1min').asfreq().dropna()

    stock_letter_df_resample['Market Hours'] = pd.to_datetime(stock_letter_df_resample.index)
    stock_letter_df_resample['Market Hours'] = stock_letter_df_resample['Market Hours'].apply(market_hours)
    stock_letter_df_resample = stock_letter_df_resample.dropna()


    stock_df_processed_lst.append(stock_letter_df_resample)






