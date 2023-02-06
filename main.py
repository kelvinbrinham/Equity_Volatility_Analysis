'''
main
'''

import numpy as np
import pandas as pd
import json as js
import datetime as dt
import matplotlib.pyplot as plt
import string

from cleaning import cleaning_stats_df
from cleaning import stock_df_lst


stock_A_df = stock_df_lst[0]

plt.figure()
plt.plot(stock_A_df['ts'][0::1000], stock_A_df['price'][0::1000])
plt.show()