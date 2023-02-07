'''
Processing
'''


import numpy as np
import pandas as pd
import json as js
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp



from cleaning import cleaning_stats_df
from cleaning import stock_df_lst as stock_df_lst_clean

#Normalize data FOR STOCK A

stock_A_df_clean = stock_df_lst_clean[0]
# print(stock_A_df_clean.describe())

# numeric_columns = stock_A_df_clean.select_dtypes(include=[np.number]).columns
# stock_A_df_clean[numeric_columns] = stock_A_df_clean[numeric_columns].apply(sp.stats.zscore)
stock_A_df = stock_A_df_clean

print(stock_A_df['ts'][0])
print(datetime.strptime(stock_A_df['ts'][0]))#, "%m/%d/%y %H:%M:%S"))




