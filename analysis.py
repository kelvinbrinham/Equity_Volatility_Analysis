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

print(stock_A_df[:20])




print('END')
