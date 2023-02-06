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

df_hist = stock_A_df.drop(columns=['ts'], axis=1)
df_hist.hist(figsize=(15, 15))
