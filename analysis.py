'''
Analysis
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

stock_A_df = stock_df_processed_lst[0][['Daily Return Percentage']]

# plt.figure()
# plt.plot(stock_A_df.index, stock_A_df['Daily Return Percentage'])
# plt.show()
# print(stock_A_df.head())

from statsmodels.tsa.stattools import adfuller

# result = adfuller(stock_A_df['Daily Return Percentage'])
# print(result[0]) #ADF statistic
# print(result[1]) #p value

from statsmodels.graphics.tsaplots import plot_acf

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (7, 3))
# ax1.plot(stock_A_df['Daily Return Percentage'])
# ax1.set_title('Original')
# plot_acf(stock_A_df['Daily Return Percentage'], ax = ax2)
# plt.show()


#Estimate difference term for ARIMA. Ours is 0 by intuition given we are using returns which is price differenced once. 
from pmdarima.arima.utils import ndiffs

# result = ndiffs(stock_A_df['Daily Return Percentage'], test = 'adf')
# print(result)

from statsmodels.graphics.tsaplots import plot_pacf

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (7, 3))
# ax1.plot(stock_A_df['Daily Return Percentage'])
# ax1.set_title('Difference once')
# ax2.set_ylim(0, 1)
# plot_pacf(stock_A_df['Daily Return Percentage'], ax = ax2)
# plt.show()


from statsmodels.tsa.arima.model import ARIMA

# model = ARIMA(stock_A_df['Daily Return Percentage'], order = (8, 0, 1))
# result = model.fit()

# print(result.summary())


# residuals = pd.DataFrame(result.resid)

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (7, 3))
# ax1.plot(residuals)
# ax2.hist(residuals, density = True)
# plt.show()
# print(stock_A_df.index)

# fig, ax = plt.subplots()
# ax = stock_A_df.plot(ax = ax)

# plot_predict(result, start = stock_A_df.index[80], end = stock_A_df.index[-1], dynamic = False, ax = ax)
# plt.show()

stock_A_df.index = pd.date_range('2017-03-01', periods=121, freq='D')
stock_A_df = stock_A_df.reset_index()
print(stock_A_df)
stock_A_df = stock_A_df.drop(columns = 'index')

#Train test split
n = int(len(stock_A_df) * 0.75)
train = stock_A_df['Daily Return Percentage'][:n]
test = stock_A_df['Daily Return Percentage'][n:]

model = ARIMA(train, order = (8, 0, 1))
result = model.fit()



fig, ax = plt.subplots(figsize=(15, 5))

# Plot the data (here we are subsetting it to get a better look at the forecasts)
stock_A_df['Daily Return Percentage'].plot(ax=ax)

print('--------')
# stock_A_df.index = pd.date_range('2017-03-01', periods = 121, freq='D') 
print(stock_A_df.index)
print('--------')


# Construct the forecasts
fcast = result.get_forecast('96').summary_frame()
print(fcast)
fcast['mean'].plot(ax=ax, style='k--')
ax.fill_between(fcast.index, fcast['mean_ci_lower'], fcast['mean_ci_upper'], color='k', alpha=0.1)

# fc = result.forecast(steps = step)
# conf = result.get_forecast(steps = step).conf_int()
# se = output.stderr


# fc = pd.Series(fc, index = test[:step].index)
# lower = pd.Series(conf[:, 0], index = test[:step].index)
# upper = pd.Series(conf[:, 1], index = test[:step].index)

# plt.figure(figsize = (7, 3))
# plt.plot(test[:step], label = 'Actual')
# plt.plot(fc, label = 'Forecast')
# plt.fill_between(lower.index, lower, upper, color = 'k', alpha = 0.1)
# plt.title('H')
# plt.legend(loc = 'upper left')

plt.show()
