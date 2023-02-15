'''
Test
'''

import numpy as np
import pandas as pd
import json as js
import datetime as dt
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp
import functions

def outlier(x):
    cutoff = 100
    if x > cutoff and  


df = pd.DataFrame(np.array([10, 11, 13, 200, 9, 8, 10]), columns = ['price'])
df['price_diff'] = df.price.diff()
df['price_diff_shift'] = df.price_diff.shift()
cutoff = 100




print(df)





