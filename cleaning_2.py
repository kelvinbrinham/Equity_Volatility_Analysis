'''
Cleaning 2.0
'''

import numpy as np
import pandas as pd
import json as js
import datetime as dt
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp
import functions


columns_lst = ['Stock', 'Unclean size', 'Repeated entries', 'Rows with missing/invalid data']

cleaning_stats_df_lst = []
stock_df_lst = []


#For each stock...
for letter in [*string.ascii_uppercase][:4]:
    filename = f'data/stock_{letter}.csv'

    #Import raw data
    stock_letter_df_unclean = pd.read_csv(filename)
    
    #Length before cleaning
    stock_letter_df_unclean_length = len(stock_letter_df_unclean)
    
    
    #df of cleaning stats for current dataset
    data = [letter, stock_letter_df_unclean_length] + [0] * (len(columns_lst) - 2)
    stock_letter_data_cleaning_stats_df = pd.DataFrame([data], columns=columns_lst)    

    #Count duplicate time entries
    stock_letter_df_unclean = stock_letter_df_unclean.drop_duplicates(subset = ['ts'], ignore_index = True)
    stock_letter_data_cleaning_stats_df['Repeated entries'] = stock_letter_df_unclean_length - len(stock_letter_df_unclean)

    #Count number of rows containing missing values or negative values or invalid (i.e. non numeric values)
    stock_letter_df_unclean_length = len(stock_letter_df_unclean)
    stock_letter_df_unclean = stock_letter_df_unclean.dropna()
    stock_letter_df_unclean = stock_letter_df_unclean.drop(stock_letter_df_unclean[stock_letter_df_unclean['price'] < 0].index)
    stock_letter_df_unclean = stock_letter_df_unclean.drop(stock_letter_df_unclean[stock_letter_df_unclean['volume'] < 0].index)
    

    #Convert times into datetime objects
    stock_letter_df_unclean['ts'] = pd.to_datetime(stock_letter_df_unclean['ts'])


    #Ensure time ordered
    if not stock_letter_df_unclean.equals(stock_letter_df_unclean.sort_values(by = ['ts'])):
        print('Raw data not in ascending time series')
        stock_letter_df_unclean = stock_letter_df_unclean.sort_values(by = ['ts'])


    #Remove data outside of market hours
    stock_letter_df_unclean['Market Hours'] = stock_letter_df_unclean['ts'].apply(functions.market_hours)
    stock_letter_df_unclean = stock_letter_df_unclean[stock_letter_df_unclean['Market Hours']]
    stock_letter_df_unclean = stock_letter_df_unclean.drop(['Market Hours'], axis = 1)

    stock_letter_data_cleaning_stats_df['Rows with missing/invalid data'] = stock_letter_df_unclean_length - len(stock_letter_df_unclean)


    stock_df_lst.append(stock_letter_df_unclean)
    cleaning_stats_df_lst.append(stock_letter_data_cleaning_stats_df)



cleaning_stats_df = pd.concat(cleaning_stats_df_lst, axis = 0, ignore_index = True)
# print(cleaning_stats_df)
