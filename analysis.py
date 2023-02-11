'''
Analysis
'''

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

model = ARIMA(stock_A_df['Daily Return Percentage'], order = (8, 0, 1))
result = model.fit()
# print(result.summary())


residuals = pd.DataFrame(result.resid)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (7, 3))
ax1.plot(residuals)
ax2.plot(residuals, density = True)
plt.show()
