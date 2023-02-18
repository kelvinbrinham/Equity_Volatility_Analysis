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
    if np.isnan(x):
        return 0
    
    elif abs(x) > cutoff:
        return np.nan
    
    else:
        return 0
    

cutoff = 300


df = pd.DataFrame(np.array([10, 11, 13, 200, 8, 10]), columns = ['price'])
df['price_diff_2nd'] = df.price.diff().diff()
df.price_diff_2nd = df.price_diff_2nd.shift(-1)


df.price_diff_2nd = df.price_diff_2nd.apply(outlier)

df = df.dropna()


# df = df.dropna()

print(df)





