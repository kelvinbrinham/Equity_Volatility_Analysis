'''
Functions
'''
import numpy as np
import pandas as pd
import json as js
import datetime as dt
import matplotlib.pyplot as plt
import string
import stats
import scipy as sp


#Masks column of dates with bool for inside or outside market hours for stocks A and B
def market_hours_AB(x):
    opening_time = dt.time(8, 00, 00)
    closing_time = dt.time(16, 30, 00)
    if x.time() >= opening_time and x.time() <= closing_time:
        return True

    else:
        return False

#Masks column of dates with bool for inside or outside market hours for stocks C and D
def market_hours_CD(x):
    opening_time = dt.time(8, 00, 00)
    closing_time = dt.time(16, 00, 00)
    if x.time() >= opening_time and x.time() <= closing_time:
        return True

    else:
        return False


#Masks columns of deltatimes with np.non/1 for no time/time
def same_day(x):
    if not x:
        return np.nan

    else:
        return 1


def realised_volatility(x):
    return sum([y ** 2 for y in x])


#Assuming 252 trading day year
def annualise_daily_return(x):
    return 252 * x
