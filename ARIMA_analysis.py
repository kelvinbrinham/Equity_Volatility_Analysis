'''
Perform prediction of stock return using ARIMA model

NB: In hindsight this script would much better suit a jupyter notebook. Or at least a function which accepts options for different parts of the analysis.
'''


import numpy as np
import pandas as pd
import json as js
from datetime import datetime
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp
import functions

from processing import stock_df_processed_lst

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima.model import ARIMA


#Loop over each Stock
for i in range(4):
    letter = 'ABCD'[i]
    #Import daily close data
    stock_A_close_df = stock_df_processed_lst[i][['Close']]

    stock_A_close_df['Date_Temp'] = stock_A_close_df.index 
    stock_A_close_df['Date_Temp'] = stock_A_close_df['Date_Temp'].dt.normalize()
    stock_A_close_df = stock_A_close_df.set_index('Date_Temp')
    #Daily percentage return using closing prices
    stock_A_close_df['Daily pcnt return'] = stock_A_close_df['Close'].pct_change()
    # print(stock_A_close_df.head())
    stock_letter_df = stock_A_close_df.dropna()
    stock_letter_df = stock_letter_df.drop(columns = ['Close'])
   

    #Perform ADF test 
    #Perform ADF test for stationarity of our daily percentage returns
    result = adfuller(stock_letter_df['Daily pcnt return'])
    # print(result)
    print('Stock ', 'ABCD'[i])
    print('ADF statistic = ', result[0]) 
    print('p-value = %.20f' % result[1]) 
    print('1% = ', result[4]['1%']) 
    print('5% = ', result[4]['5%']) 
    print('10% = ', result[4]['10%']) 



    #Plot ACF plots to deduce q term for ARIMA
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 5))
    ax1.plot(stock_letter_df['Daily pcnt return'])
    ax1.set_title(f'Daily Percentage Return Stock {letter}')
    ax2.set_ylim(0, 1.1)
    # ax1.set_xticks
    ax2.set_xlabel('Lag', fontsize = 10)
    ax1.set_xlabel('Date', fontsize = 10)
    plot_acf(stock_letter_df['Daily pcnt return'], ax = ax2)
    plt.savefig(f'figures/ACF_stock{letter}.png', dpi = 800, format = 'png')
    plt.show()

    

    stock_letter_df = stock_letter_df.reset_index()

    #Reseting index to just numbers to ensure data is evenly spaced for ARIMA model
    stock_letter_df['Daily pcnt return'] = stock_letter_df['Daily pcnt return'].apply(functions.annualise_daily_return)
    model = ARIMA(stock_letter_df['Daily pcnt return'], order= (10, 0, 12))
    result = model.fit()
    # print(result.summary())


    fig, ax = plt.subplots(figsize=(15, 5))

    # Plot the data (here we are subsetting it to get a better look at the forecasts)
    stock_letter_df['Daily pcnt return'].plot(ax=ax)

    # Construct the forecasts and plot
    fcast = result.get_forecast(7).summary_frame()
    print(fcast)
    fcast['mean'].plot(ax=ax, style='k--')
    ax.fill_between(fcast.index, fcast['mean_ci_lower'], fcast['mean_ci_upper'], color='k', alpha=0.1)
    # plt.savefig(f'figures/Prediction_stock{letter}.png', dpi = 800, format = 'png')
    plt.show()

print('END')