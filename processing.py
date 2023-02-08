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
from cleaning import market_hours


def RealisedVolatility(x):
    return np.sqrt(sum([y ** 2 for y in x]))


def is_5_minutes(x): #CHANGE TO NEW CHUNKED METHOD
    if x.total_seconds() == 300:
        return x
    else:
        return np.nan


stock_df_processed_lst = []
