'''
Cleaning data
'''

import numpy as np
import pandas as pd
import json as js
import datetime as dt
import matplotlib.pyplot as plt

#For each data set...

#Import raw data
stock_A_df_unclean = pd.read_csv('data/stock_A.csv')
stock_A_df_unclean_length = len(stock_A_df_unclean)

stock_A_data_cleaning_stats_dict = {'No. repeated rows': 0, 'No. Missing time stamps': 0, 'No. Missing prices': 0, 'No. Missing volumes': 0}

#Drop duplicate rows and count duplicates
stock_A_df = stock_A_df_unclean.drop_duplicates(ignore_index = True)
stock_A_data_cleaning_stats_dict['No. repeated rows'] = stock_A_df_unclean_length - len(stock_A_df)

#Count and remove Missing values
i = 1
for column in stock_A_df_unclean.columns:
    key = list(stock_A_data_cleaning_stats_dict.keys())[i]
    stock_A_data_cleaning_stats_dict[key] = stock_A_df_unclean[column].isnull().sum()
    i += 1

stock_A_df.dropna(inplace = True)

print(stock_A_data_cleaning_stats_dict)
print(stock_A_df)



