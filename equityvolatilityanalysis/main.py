"""Main Script"""

import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd
from cleaning import clean_stock_data
from functions import remove_stock_split
from processing import Processor

outlier_cutoff_dict = {"A": 20, "B": 100, "C": 0.9, "D": 100}
stock_data_length_dict = {"A": 101, "B": 101, "C": 95, "D": 95}

market_hours_dict = {
    "A": {
        "market_open": dt.time(8, 00, 00),
        "market_close": dt.time(16, 30, 00),
    },
    "B": {
        "market_open": dt.time(8, 00, 00),
        "market_close": dt.time(16, 30, 00),
    },
    "C": {
        "market_open": dt.time(8, 00, 00),
        "market_close": dt.time(16, 00, 00),
    },
    "D": {
        "market_open": dt.time(8, 00, 00),
        "market_close": dt.time(16, 00, 00),
    },
}

cleaning_df = pd.DataFrame(
    columns=[
        "Stock",
        "Unclean size",
        "Repeated entries",
        "Rows with missing/invalid data",
    ]
)

for ticker, cutoff in outlier_cutoff_dict.items():

    filename = f".data/stock_{ticker}.csv"

    # Import raw data
    stock_letter_df_unclean = pd.read_csv(filename)

    # Remove observed stock split from stock D
    if ticker == "D":
        stock_letter_df_unclean = remove_stock_split(
            data=stock_letter_df_unclean, split_index=32601
        )

    # Clean data
    market_open = market_hours_dict[ticker]["market_open"]
    market_close = market_hours_dict[ticker]["market_close"]

    stock_letter_df_clean, cleaning_df_internal = clean_stock_data(
        stock_data=stock_letter_df_unclean,
        market_open=market_open,
        market_close=market_close,
        outlier_cutoff=cutoff,
    )

    cleaning_df_internal = cleaning_df_internal.assign(Stock=ticker)

    cleaning_df = pd.concat(
        [cleaning_df, cleaning_df_internal], ignore_index=True
    )

    # Process data
    processor = Processor(data=stock_letter_df_clean)
    stock_letter_df_processed = processor(
        stock_data_length=stock_data_length_dict[ticker]
    )


print(cleaning_df)

processor.plot
plt.show()
