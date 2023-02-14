'''
Cleaning
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
    if letter in 'AB':
        stock_letter_df_unclean['Market Hours'] = stock_letter_df_unclean['ts'].apply(functions.market_hours_AB)
    else:
        stock_letter_df_unclean['Market Hours'] = stock_letter_df_unclean['ts'].apply(functions.market_hours_CD)
    stock_letter_df_unclean = stock_letter_df_unclean[stock_letter_df_unclean['Market Hours']]
    stock_letter_df_unclean = stock_letter_df_unclean.drop(['Market Hours'], axis = 1)

    stock_letter_data_cleaning_stats_df['Rows with missing/invalid data'] = stock_letter_df_unclean_length - len(stock_letter_df_unclean)

    stock_df_lst.append(stock_letter_df_unclean)
    cleaning_stats_df_lst.append(stock_letter_data_cleaning_stats_df)


    #Remove outliers
    #I choose to define an outlier by a point which is largely different to 2 similar points either side of it. 
    #Specfically, 
    #~Differnce matrix... FINISH
    stock_letter_df_unclean['Price Difference'] = stock_letter_df_unclean['price'].diff()
    price_diff_std = stock_letter_df_unclean['Price Difference'].std()
    cutoff = 3 * price_diff_std
    stock_letter_df_unclean = stock_letter_df_unclean.dropna()

    for i in range(1, len(stock_letter_df_unclean) - 1):
        if stock_letter_df_unclean['Price Difference'][i] > cutoff and stock_letter_df_unclean['Price Difference'][i + 1] < - cutoff:
            stock_letter_df_unclean['price'][i + 1] = np.nan

        elif stock_letter_df_unclean['Price Difference'][i] < -cutoff and stock_letter_df_unclean['Price Difference'][i + 1] > cutoff:
            stock_letter_df_unclean['price'] = np.nan

    outlier_length = len(stock_letter_df_unclean)
    stock_letter_df_unclean = stock_letter_df_unclean.dropna()
    outliers = outlier_length - len(stock_letter_df_unclean)
    print(outliers)
    plt.plot(stock_letter_df_unclean.index, stock_letter_df_unclean['price'])
    plt.show()
    break
    





    
# stock_df = stock_df_lst[1]
# plt.plot(stock_df.index, stock_df.price, '.', markersize = 0.8)
# plt.show()




cleaning_stats_df = pd.concat(cleaning_stats_df_lst, axis = 0, ignore_index = True)
# print(cleaning_stats_df)


