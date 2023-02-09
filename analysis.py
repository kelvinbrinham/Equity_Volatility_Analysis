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

# stock_corr_df_lst = []

# for i in range(4):
#     stock_letter_df = stock_df_processed_lst[i]
#     stock_letter_corr_df = stock_letter_df.corr(method = 'pearson')
#     stock_corr_df_lst.append(stock_letter_corr_df['30-minute RV'][0])




stock_A_df = stock_df_processed_lst[0]

stock_A_df = stock_A_df.apply(sp.stats.zscore)
stock_A_df['30-minute RV'] = stock_A_df['30-minute RV'].shift(1)
stock_A_df = stock_A_df.dropna()
stock_A_df = stock_A_df.apply(sp.stats.zscore)


# print(stock_A_df[:20])

# plt.figure()
# plt.plot(stock_A_df['volume'], stock_A_df['30-minute RV'], '.', markersize = 0.8)
# plt.show()

# stock_A_df.to_excel('data/TEST.xlsx')
corr_df = stock_A_df.corr(method = 'pearson')

print(corr_df)

print('END')
