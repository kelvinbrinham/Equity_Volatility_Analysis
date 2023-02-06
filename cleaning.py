'''
Cleaning data
'''

import numpy as np
import pandas as pd
import json as js
import datetime as dt
import matplotlib.pyplot as plt
import string
import stats

columns_lst = ['Dataset', 'Unclean size', 'No. repeated rows', 'No. Missing time stamps', 'No. Missing prices', 'No. Missing volumes', 'No. Negative Values', 'Outliers']
# cleaning_stats_df = pd.DataFrame(columns = columns_lst)
cleaning_stats_df_lst = []
stock_df_lst = []
k = 1.5

#For each data set...
for letter in [*string.ascii_uppercase][:4]:
    filename = f'data/stock_{letter}.csv'

    #Import raw data
    stock_letter_df_unclean = pd.read_csv(filename)
    stock_letter_df_unclean_length = len(stock_letter_df_unclean)

    #df of cleaning stats for current dataset
    data = [letter, stock_letter_df_unclean_length] + [0] * (len(columns_lst) - 2)
    stock_letter_data_cleaning_stats_df = pd.DataFrame([data], columns=columns_lst)    

    #Drop duplicate rows and count duplicates
    stock_letter_df_unclean = stock_letter_df_unclean.drop_duplicates(ignore_index = True)
    stock_letter_data_cleaning_stats_df['No. repeated rows'] = stock_letter_df_unclean_length - len(stock_letter_df_unclean)

    #Count Missing values
    i = 3
    for column in stock_letter_df_unclean.columns:
        key = columns_lst[i]
        stock_letter_data_cleaning_stats_df[key] = stock_letter_df_unclean[column].isnull().sum()
        i += 1

    #Remove missing values
    stock_letter_df_unclean = stock_letter_df_unclean.dropna()

    #Count and remove Negative values as well as outliers using the k*IQR method where k is a parameter of user choice
    for column_ in stock_letter_df_unclean.columns[1:]:
        #Count negative values
        stock_letter_data_cleaning_stats_df['No. Negative Values'] += sum(n < 0 for n in stock_letter_df_unclean[column_].values.flatten())
        #Remove negative values
        stock_letter_df_unclean = stock_letter_df_unclean.drop(stock_letter_df_unclean[stock_letter_df_unclean[column_] < 0].index)

        #Count outliers
        IQR = stats.iqr(stock_letter_df_unclean[column_])
        lower_bound = stats.quantile(stock_letter_df_unclean[column_], p=0.25) - (k * IQR)
        if lower_bound < 0:
            lower_bound = 0

        upper_bound = stats.quantile(stock_letter_df_unclean[column_], p=0.75) + (k * IQR)

        stock_letter_data_cleaning_stats_df['Outliers'] += sum(n < lower_bound for n in stock_letter_df_unclean[column_].values.flatten())
        stock_letter_data_cleaning_stats_df['Outliers'] += sum(n > upper_bound for n in stock_letter_df_unclean[column_].values.flatten())

        #Remove outliers
        stock_letter_df_unclean = stock_letter_df_unclean.drop(stock_letter_df_unclean[stock_letter_df_unclean[column_] < lower_bound].index)
        stock_letter_df_unclean = stock_letter_df_unclean.drop(stock_letter_df_unclean[stock_letter_df_unclean[column_] > upper_bound].index)

    stock_letter_df_clean = stock_letter_df_unclean

    #Add cleaning stats to list
    cleaning_stats_df_lst.append(stock_letter_data_cleaning_stats_df)

    #Add cleaned data to one list
    stock_df_lst.append(stock_letter_df_clean)


cleaning_stats_df = pd.concat(cleaning_stats_df_lst, axis=0, ignore_index=True)


# print(cleaning_stats_df)

