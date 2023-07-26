"""Cleaning script"""

import datetime as dt
from typing import Tuple

import functions
import pandas as pd


def clean_stock_data(
    stock_data: pd.DataFrame,
    market_open: dt.datetime,
    market_close: dt.datetime,
    outlier_cutoff: float,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cleans stock data by removing outliers, removing duplicate entries and
    invalid entries.

    Args:
        stock_data: Raw stock data.
        market_open: Time of market open.
        market_close: Time of market close.
        outlier_cutoff: Cutoff values for outliers in the stock price. The
        cutoff is the sum of the difference between a price and its prior and
        subsequent prices. For example, prices 3, 400, 4 would have a cutoff of
        793.

    Returns:
        Cleaned stock data and cleaning stats.
    """
    cleaning_columns_lst = [
        "Unclean size",
        "Repeated entries",
        "Rows with missing/invalid data",
    ]
    cleaning_df = pd.DataFrame(
        [[None] * len(cleaning_columns_lst)], columns=cleaning_columns_lst
    )
    cleaning_df["Unclean size"] = len(stock_data)
    stock_df_unclean_length = cleaning_df["Unclean size"]

    # Count duplicate time entries
    stock_data = stock_data.drop_duplicates(subset=["ts"], ignore_index=True)
    cleaning_df["Repeated entries"] = stock_df_unclean_length - len(stock_data)

    # Count number of rows containing missing values or negative values or
    # invalid (i.e. non numeric values)
    stock_df_unclean_length = len(stock_data)
    stock_data = stock_data.dropna()
    stock_data = stock_data.drop(stock_data[stock_data["price"] < 0].index)
    stock_data = stock_data.drop(stock_data[stock_data["volume"] < 0].index)

    # Convert times into datetime objects
    stock_data["ts"] = pd.to_datetime(stock_data["ts"])

    # Ensure time ordered
    if not stock_data.equals(stock_data.sort_values(by=["ts"])):
        print("Raw data not in ascending time series")
        stock_data = stock_data.sort_values(by=["ts"])

    # Remove data outside of market hours
    stock_data["Market Hours"] = stock_data["ts"].apply(
        functions.market_hours, args=(market_open, market_close)
    )

    stock_data = stock_data[stock_data["Market Hours"]]
    stock_data = stock_data.drop(["Market Hours"], axis=1)

    cleaning_df[
        "Rows with missing/invalid data"
    ] = stock_df_unclean_length - len(stock_data)

    # Remove outliers
    # I choose to define an outlier by a point which is largely different to 2
    # similar points either side of it.
    # cutoff is defined as TWICE the distance from the outlier to the two
    # neighbouring points

    stock_data["2nd_price_difference"] = stock_data.price.diff().diff()
    stock_data["2nd_price_difference"] = stock_data[
        "2nd_price_difference"
    ].shift(-1)

    stock_data["2nd_price_difference"] = stock_data[
        "2nd_price_difference"
    ].apply(functions.outlier, args=(outlier_cutoff,))
    stock_letter_df_unclean_length = len(stock_data)
    stock_data = stock_data.dropna()
    cleaning_df["Outliers"] = int(
        stock_letter_df_unclean_length - len(stock_data)
    )
    stock_data = stock_data.drop(columns=["2nd_price_difference"])

    # Check if first and/or last prices are outliers becuase the previous
    # outlier method cannot handle these
    if (
        abs(stock_data.price.values[0] - stock_data.price.values[1])
        > outlier_cutoff
    ):
        stock_data = stock_data.drop(index=stock_data.index[0], axis=0)

    if (
        abs(stock_data.price.values[-1] - stock_data.price.values[-2])
        > outlier_cutoff
    ):
        stock_data = stock_data.drop(index=stock_data.index[-1], axis=0)

    return stock_data, cleaning_df
