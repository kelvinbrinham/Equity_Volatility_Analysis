'''
Processing 2
'''

import numpy as np
import pandas as pd
import json as js
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp
import functions

from cleaning_2 import stock_df_lst


# for i in range(len(stock_df_lst)):
for i in range(1):
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
    # stock_letter_df_processing['Date'][0] = np.nan

    print(stock_letter_df.head())
    stock_letter_df.to_excel('data/T.xlsx')