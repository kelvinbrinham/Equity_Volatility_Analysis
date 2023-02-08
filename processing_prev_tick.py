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

    stock_letter_df_processing = stock_letter_df_clean.set_index('ts')

    print(stock_letter_df_processing.head())

    stock_letter_df_processing = stock_letter_df_processing.resample('5min').ffill()

    print(stock_letter_df_processing.head())




