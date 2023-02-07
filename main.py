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

from processing import stock_df_processed_lst as stock_df_lst


#Calculate 1-day return using the resampled data
stock_A_df = stock_df_lst[0]

stock_A_df['1-Minute Return'] = stock_A_df.shift(1)['price'] - stock_A_df['price']
#Drop duplicates (Non buisness days)
stock_A_df = stock_A_df.drop_duplicates(subset='1-Minute Return')
#Drop empty rows (First row)
stock_A_df = stock_A_df.dropna()


def RealisedVolatility(x):
    return (1 / 10) * np.sqrt(sum([y ** 2 for y in x]))


#Calculate 1-day RV (relative vortility)
stock_A_df['10-Minute Relative Vortility'] = stock_A_df['1-Minute Return'].rolling(10).apply(RealisedVolatility)
stock_A_df = stock_A_df.dropna()

#Define trading year as 252 days, each with 
# stock_A_df['10-Minute Relative Vortility (Annualised)'] = stock_A_df['10-Minute Relative Vortility'] * np.sqrt(252/)

print(stock_A_df[:1100])
# plt.figure()
# stock_A_df['30-Minute Relative Vortility'].plot()
# plt.show()

