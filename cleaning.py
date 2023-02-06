'''
Cleaning data
'''

import numpy as np
import pandas as pd
import json as js
import datetime as dt
import matplotlib.pyplot as plt
import string

columns_lst = ['Dataset', 'No. repeated rows', 'No. Missing time stamps', 'No. Missing prices', 'No. Missing volumes', 'No. Negative Values']
cleaning_stats_df = pd.DataFrame(columns = columns_lst)
cleaning_stats_df_lst = []
stock_df_lst = []

#For each data set...
for letter in [*string.ascii_uppercase][:4]:
    filename = f'data/stock_{letter}.csv'

    #Import raw data
    stock_letter_df_unclean = pd.read_csv(filename)
    stock_letter_df_unclean_length = len(stock_letter_df_unclean)

    #Dictionary of cleaning stats for current dataset
    stock_letter_data_cleaning_stats_dict = {'Dataset': 0, 'No. repeated rows': 0, 'No. Missing time stamps': 0, 'No. Missing prices': 0, 'No. Missing volumes': 0, 'No. Negative Values': 0}
    stock_letter_data_cleaning_stats_dict['Dataset'] = letter

    #Drop duplicate rows and count duplicates
    stock_letter_df = stock_letter_df_unclean.drop_duplicates(ignore_index = True)
    stock_letter_data_cleaning_stats_dict['No. repeated rows'] = stock_letter_df_unclean_length - len(stock_letter_df)

    #Count Missing values
    i = 2
    for column in stock_letter_df_unclean.columns:
        key = columns_lst[i]
        stock_letter_data_cleaning_stats_dict[key] = stock_letter_df[column].isnull(
        ).sum()
        i += 1

    #Remove missing values
    stock_letter_df_clean = stock_letter_df.dropna()

    #Count and remove Negative values
    for column_ in stock_letter_df_unclean.columns[1:]:
        stock_letter_data_cleaning_stats_dict['No. Negative Values'] += sum(n < 0 for n in stock_letter_df_unclean[column_].values.flatten())
        stock_letter_df_clean.drop(stock_letter_df_clean[stock_letter_df_clean[column_] < 0].index, inplace = True)


    #Add cleaning stats to list
    cleaning_stats_df_lst.append(pd.DataFrame([stock_letter_data_cleaning_stats_dict]))

    #Add cleaned data to one list
    stock_df_lst.append(stock_letter_df_clean)


cleaning_stats_df = pd.concat(cleaning_stats_df_lst, axis=0, ignore_index=True)

