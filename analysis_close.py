'''
Analysis Close price
'''

from statsmodels.graphics.tsaplots import plot_predict
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import json as js
from datetime import datetime
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp

from processing import stock_df_processed_lst


stock_A_close_df = stock_df_processed_lst[1][['Close']]
stock_A_close_df['Date_Temp'] = stock_A_close_df.index 
stock_A_close_df['Date_Temp'] = stock_A_close_df['Date_Temp'].dt.normalize()
stock_A_close_df = stock_A_close_df.set_index('Date_Temp')
stock_A_close_df['Daily pcnt return'] = stock_A_close_df['Close'].pct_change()
stock_letter_df = stock_A_close_df.dropna()
stock_letter_df = stock_letter_df.drop(columns = ['Close'])

print(stock_letter_df.head())


#Perform ADF test for stationarity of our daily percentage returns
from statsmodels.tsa.stattools import adfuller

result = adfuller(stock_letter_df['Daily pcnt return'])
print(result)
print('ADF statistic = ', result[0]) 
print('p-value = %.20f' % result[1]) 
print('1% = ', result[4]['1%']) 
print('5% = ', result[4]['5%']) 
print('10% = ', result[4]['10%']) 