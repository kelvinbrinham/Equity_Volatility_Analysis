"""Functions"""

import datetime as dt

import numpy as np
import pandas as pd


def market_hours(
    time: dt.datetime, market_open: dt.datetime, market_close: dt.datetime
) -> bool:
    """
    Masks a point with True if it is within market hours and False if it is
    outside market hours.

    Args:
        time: Current time.
        market_open: Market opening time.
        market_close: Market closing time.

    Returns:
        True if time is within market hours, False otherwise.
    """
    if time.time() >= market_open and time.time() <= market_close:
        return True

    else:
        return False


def outlier(data_point: float, cutoff: float) -> float:
    """
    Mask a point above cutoff with np.nan. Mask a point below cutoff with 0.

    Args:
        data_point: Data point.
        cutoff: Cutoff value.

    Returns:
        np.nan if data_point is above cutoff, 0 otherwise.
    """
    if np.isnan(data_point):
        return 0

    elif abs(data_point) > cutoff:
        return np.nan

    else:
        return 0


def remove_stock_split(data: pd.DataFrame, split_index: int) -> pd.DataFrame:
    """
    Remove stock split from data.

    Args:
        data: Stock price data.
        split_index: Index on which stock split occurs.

    Returns:
        Adjusted data.
    """
    split_factor = (
        data.price.values[split_index] / data.price.values[split_index + 1]
    )
    data.price[split_index + 1 :] = data.price[split_index + 1 :] * split_factor
    data.volume[split_index + 1 :] = (
        data.volume[split_index + 1 :] / split_factor
    )

    return data
