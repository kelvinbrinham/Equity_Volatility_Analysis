'''
main
'''

import numpy as np
import pandas as pd
import json as js
import datetime as dt
import matplotlib.pyplot as plt
import string
import stats

from cleaning import cleaning_stats_df
from cleaning import stock_df_lst


stock_A_df = stock_df_lst[0]

print(stock_A_df)

# df_hist = stock_A_df.drop(columns=['ts'], axis=1)
# df_hist.hist(figsize=(5, 5), bins = 20)
# plt.show()

# plt.plot(stock_A_df['ts'][0::20], stock_A_df['price'][0::20])
# # plt.plot(stock_A_df['ts'], stock_A_df['volume'])
# plt.show()
from statsmodels.tsa.seasonal import seasonal_decompose


df_series = stock_A_df.set_index('ts').asfreq('D')
series = pd.Series(df_series['price'], index= df_series.index)
results = seasonal_decompose(series, model='additive', period = 30)
plt.rcParams['figure.figsize'] = (10.0, 5.0)
results.plot()
plt.show()

