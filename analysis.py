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

stock_A_df = stock_df_processed_lst[0]

print(stock_A_df.head())

stock_A_df.to_excel('data/TEST.xlsx')


print('END')