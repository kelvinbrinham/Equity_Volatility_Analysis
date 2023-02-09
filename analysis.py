'''
Analysis
'''

import numpy as np
import pandas as pd
import json as js
# import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp

from processing import stock_df_processed_lst

stock_corr_df_lst = []

for i in range(4):
    stock_A_df = stock_df_processed_lst[i]
#     stock_letter_corr_df = stock_letter_df.corr(method = 'pearson')
#     stock_corr_df_lst.append(stock_letter_corr_df['30-minute RV'][0])

    stock_A_df = stock_df_processed_lst[0]
    stock_A_df = stock_A_df.apply(sp.stats.zscore)

    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df['volume'] > 3].index)
    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df['volume'] < -3].index)
    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df['30-minute RV'] > 3].index)
    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df['30-minute RV'] < -3].index)

    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df['Prior Day Rolling Average Trading Volume'] > 3].index)
    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df['Prior Day Rolling Average Trading Volume'] < -3].index)
    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df['Prior Day Rolling Average RV'] > 3].index)
    stock_A_df = stock_A_df.drop(stock_A_df[stock_A_df['Prior Day Rolling Average RV'] < -3].index)

    stock_corr_df_lst.append(stock_A_df)


df_total = pd.concat(stock_corr_df_lst)
print(df_total)

# plt.figure()
# plt.plot(stock_A_df.index, stock_A_df['30-minute RV'])
plt.plot(df_total['Prior Day Rolling Average Trading Volume'], df_total['Prior Day Rolling Average RV'], '.', markersize = 0.8)
# plt.plot(df_total['volume'], df_total['30-minute RV'], '.', markersize = 0.8)

# a, b = np.polyfit(df_total['Prior Day Rolling Average Trading Volume'], df_total['Prior Day Rolling Average RV'], 1)
# plt.plot(df_total['Prior Day Rolling Average Trading Volume'], (a * df_total['Prior Day Rolling Average Trading Volume']) + b)
plt.show()

# print(df_total.corr(method = 'pearson'))




print('END')
