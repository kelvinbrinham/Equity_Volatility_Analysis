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

plt.figure()
plt.plot(stock_A_df['volume'], stock_A_df['30-minute RV'], '.')
plt.show()

print(stock_A_df.head())

# stock_A_df.to_excel('data/TEST.xlsx')
# corr_df = stock_A_df.corr(method = 'pearson')

# print(corr_df.head())

print('END')