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

for i in range(4):
    print(stock_df_lst[i].head())

