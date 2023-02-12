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

stock_A_close_df = stock_df_processed_lst[0][['Close']]

#Define week as 5 trading days

stock_A_close_df = stock_A_close_df.rolling(5).mean()
stock_A_close_df = stock_A_close_df.dropna()
stock_A_close_df['Rolling 5 day return'] = (stock_A_close_df['Close'] - stock_A_close_df['Close'].shift(5)) / stock_A_close_df['Close'].shift(5)
stock_A_close_df = stock_A_close_df.dropna()
stock_A_close_df = stock_A_close_df.apply(sp.stats.zscore)


from statsmodels.tsa.arima.model import ARIMA

stock_A_df = stock_A_close_df.drop(columns = ['Close'])

stock_A_df = stock_A_df.resample('D').mean()


# Train test split
n = int(len(stock_A_df) * 0.75)
train = stock_A_df['Rolling 5 day return'][:n]
test = stock_A_df['Rolling 5 day return'][n:]

model = ARIMA(train, order=(8, 0, 1))
result = model.fit()


fig, ax = plt.subplots(figsize=(15, 5))

# Plot the data (here we are subsetting it to get a better look at the forecasts)
stock_A_df['Rolling 5 day return'].plot(ax=ax)



# Construct the forecasts
fcast = result.get_forecast().summary_frame()
print(fcast)
fcast['mean'].plot(ax=ax, style='k--')
ax.fill_between(fcast.index, fcast['mean_ci_lower'], fcast['mean_ci_upper'], color='k', alpha=0.1)

plt.show()
