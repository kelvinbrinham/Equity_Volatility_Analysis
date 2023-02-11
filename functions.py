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


def market_hours(x):
    opening_time = dt.time(8, 00, 00)
    closing_time = dt.time(16, 30, 00)
    if x.time() >= opening_time and x.time() <= closing_time:
        return True

    else:
        return False



def same_day(x):
    if not x:
        return np.nan

    else:
        return 1


def realised_volatility(x):
    return sum([y ** 2 for y in x])


