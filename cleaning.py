'''
Cleaning data
'''

import numpy as np
import pandas as pd
import json as js
import datetime as dt
import matplotlib.pyplot as plt

#Import first 10,000 rows for speed and testing
stock_A_df = pd.read_csv('data/stock_A.csv')#, nrows = 0000)
stock_A_df_length = len(stock_A_df)

data_cleaning_stats_dict = {'No. repeated rows': 0, 'No. Missing time stamps': 0, 'No. Missing prices': 0, 'No. Missing volumes': 0}

#Drop duplicate rows
stock_A_df.drop_duplicates(inplace = True, ignore_index = True)
data_cleaning_stats_dict['No. repeated rows'] = stock_A_df_length - len(stock_A_df)

#Count Missing values
data_cleaning_stats_dict['No. Missing time stamps'] = stock_A_df['ts'].isnull().sum()
data_cleaning_stats_dict['No. Missing prices'] = stock_A_df['price'].isnull().sum()
data_cleaning_stats_dict['No. Missing volumes'] = stock_A_df['volume'].isnull().sum()
print(data_cleaning_stats_dict)

#Drop missing values

