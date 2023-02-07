'''
Test
'''

from datetime import datetime
import datetime as dt
import numpy as np

x = dt.datetime(2016,4,30,15,20,6)

def market_hours(x):
    opening_time = dt.time(8,00,00)
    closing_time = dt.time(16,30,00)
    if x.time() > opening_time and x.time() < closing_time:
        return x

    else:
        return np.nan

print(market_hours(x))
