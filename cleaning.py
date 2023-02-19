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

#Outlier price range for each stock. These numbers represent the sum of the difference of the outlier price to its two neighbours. 
#E.g. say we have prices 3, 400, 4. We see 400 is likely an outlier, the relevant cutoff in this case is 400 - 3 + 400 - 4 = 793
outlier_cutoff_dict = {'A': 20, 'B': 100, 'C': 0.9, 'D': 100}

#For each stock...
for letter in [*string.ascii_uppercase][:4]:
    filename = f'data/stock_{letter}.csv'

    #Import raw data
    stock_letter_df_unclean = pd.read_csv(filename)

    plt.figure()
    plt.plot(stock_letter_df_unclean.ts, stock_letter_df_unclean.price, label = 'Before Cleaning')
    
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


    #Remove outliers
    #I choose to define an outlier by a point which is largely different to 2 similar points either side of it. 
    # cutoff is defined as TWICE the distance from the outlier to the two neighbouring points
    stock_letter_df_unclean['2nd_price_difference'] = stock_letter_df_unclean.price.diff().diff()
    stock_letter_df_unclean['2nd_price_difference'] = stock_letter_df_unclean['2nd_price_difference'].shift(-1)
    cutoff__ = outlier_cutoff_dict[letter]
    stock_letter_df_unclean['2nd_price_difference'] = stock_letter_df_unclean['2nd_price_difference'].apply(functions.outlier, args = (cutoff__,))
    stock_letter_df_unclean_length = len(stock_letter_df_unclean)
    stock_letter_df_unclean = stock_letter_df_unclean.dropna()
    stock_letter_data_cleaning_stats_df['Outliers'] = stock_letter_df_unclean_length - len(stock_letter_df_unclean)
    stock_letter_df_unclean = stock_letter_df_unclean.drop(columns = ['2nd_price_difference'])
    
   
    #Removing stock split with stock D
    if letter == 'D':
        #Index on which the split happens is observed
        split_index = 32435
        split_factor = stock_letter_df_unclean.price.values[split_index] / stock_letter_df_unclean.price.values[split_index + 1]
        stock_letter_df_unclean.price[split_index + 1:] = stock_letter_df_unclean.price[split_index + 1:] * split_factor
        stock_letter_df_unclean.volume[split_index + 1:] = stock_letter_df_unclean.volume[split_index + 1:] / split_factor
        
   
    #Check if first and/or last prices are outliers becuase the previous outlier method cannot handle these
    if abs(stock_letter_df_unclean.price.values[0] - stock_letter_df_unclean.price.values[1]) > outlier_cutoff_dict[letter]:
        stock_letter_df_unclean = stock_letter_df_unclean.drop(index = stock_letter_df_unclean.index[0], axis = 0)

    if abs(stock_letter_df_unclean.price.values[-1] - stock_letter_df_unclean.price.values[-2]) > outlier_cutoff_dict[letter]:
        stock_letter_df_unclean = stock_letter_df_unclean.drop(index = stock_letter_df_unclean.index[-1], axis = 0)

    plt.plot(stock_letter_df_unclean.ts, stock_letter_df_unclean.price, label = 'After Cleaning')
    plt.title('Stock A')
    plt.ylabel('Price')
    plt.xlabel('Time')
    plt.legend()
    plt.savefig('data/price.png', format = 'png', dpi = 800)
    plt.show()

    break

    stock_df_lst.append(stock_letter_df_unclean)
    cleaning_stats_df_lst.append(stock_letter_data_cleaning_stats_df)


    





    
stock_df = stock_df_lst[0]

# plt.plot(stock_df.index, stock_df.price, '.', markersize = 0.8)
plt.plot(stock_df.index, stock_df.price)
plt.show()

cleaning_stats_df = pd.concat(cleaning_stats_df_lst, axis = 0, ignore_index = True)
print(cleaning_stats_df)


