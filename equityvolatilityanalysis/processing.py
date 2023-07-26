"""
Processing

Here RV is calculated from 5-minute prices each day.
"""

from datetime import timedelta
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp


class Processor:
    """
    Class to process the intra-day stock data and return realised volatility
    (RV) (according to the prescription in the report) and daily volume.

    Args:
        data: Clean stock data.

    Returns:
        Processed stock data. I.e. daily stock data including volume and RV.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        # List of chunked dataframes (1 for each day)
        self._chunked_df_lst = []
        self._processed_chunks_lst = []
        self._processed_data_df = None

    def __call__(self, stock_data_length: int) -> pd.DataFrame:
        """
        Process the data.

        Args:
            stock_data_length: Correct number of 5-minute return ticks for the
            stock.

        Returns:
            Processed daily data.
        """
        # Reset timestamp as index
        self.data = self.data.set_index("ts")
        # Create date column to chunk data

        # Chunk dataframe into dataframes for each day
        self._chunked_df_lst = self._chunk_data(data=self.data)

        # Process the data for each day
        for i in range(len(self._chunked_df_lst)):
            chunk = self._chunked_df_lst[i]

            # Daily return using closing price
            close = chunk["price"][-1]

            # 1. Resample using previous tick method over 5-minute intervals
            first_tick = chunk["price"][0]
            chunk_res = chunk[["price"]].resample("5min").ffill()
            chunk_res["price"][0] = first_tick

            # 2. Daily volume
            volume = chunk["volume"].sum()

            # 3. Calculate 5-minute returns
            chunk_res["5-Minute (log) Return"] = self._returns(data=chunk_res)
            chunk_res = chunk_res.dropna()

            # 4. Check number of 5 minute intervals.
            if len(chunk_res) != stock_data_length:
                chunk_res = self._fix_missing_intervals(data=chunk_res)

            # 5. Daily realised volatility
            chunk_res["RV"] = (
                chunk_res["5-Minute (log) Return"]
                .rolling(len(chunk_res))
                .apply(self._realised_volatility)
            )
            chunk_res = chunk_res.dropna()

            # 6. Add daily volume and RV to new dataframe
            chunk_res["volume"] = np.nan
            chunk_res["volume"][0] = volume
            chunk_res = chunk_res.drop(
                columns=["price", "5-Minute (log) Return"]
            )

            chunk_res["Close"] = [close]

            # 7. Add chunk to list of chunks
            self._processed_chunks_lst.append(chunk_res)

        # Concatenate all chunks into one dataframe
        self._processed_data_df = pd.concat(self._processed_chunks_lst)

        return self._processed_data_df

    @property
    def plot(self) -> None:
        """Plot all processed data correlation matrices."""
        if self._processed_data_df is None:
            raise ValueError("Data not processed yet.")

        data = self._processed_data_df
        data = data.apply(sp.stats.zscore)
        plt.figure()
        plt.plot(data.volume, data.RV, ".", markersize=1)

        # Plot line of best fit (least squares)
        a, b = np.polyfit(data.volume, data.RV, 1)
        plt.plot(data.volume, a * data.volume + b)

        plt.ylabel("Volume [z-score]", fontsize=16)
        plt.xlabel("RV [z-score]", fontsize=16)
        # plt.title(f'Stock {letter}')

        # plt.savefig(f"data/Final_{letter}.png", format="png", dpi=800)

        print(data.corr("pearson"))

    def _realised_volatility(self, x: Union[list, pd.Series]) -> float:
        """Calculate realised volatility."""
        return sum([y**2 for y in x])

    def _fix_missing_intervals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Fill missing value in data with the mean of the data.

        Args:
            data: Data.

        Returns:
            Filled data.
        """
        out = pd.DataFrame()
        out = data.reset_index()
        out.loc[-1] = [
            (out["ts"][0] - timedelta(hours=0, minutes=5)),
            out["price"].mean(),
            out["5-Minute (log) Return"].mean(),
        ]
        out.index = out.index + 1  # shifting index
        out = out.sort_index()
        out = out.set_index("ts")

        return out

    def _chunk_data(self, data: pd.DataFrame) -> List[pd.DataFrame]:
        """
        Chunk dataframe into dataframes for each day.

        Args:
            data: Stock data.

        Returns:
            List of dataframes, one for each day.
        """
        data["Date"] = pd.to_datetime(data.index)

        data["Date"] = data["Date"].dt.normalize()

        data["Date"] = data["Date"] - data["Date"].shift()

        data["Date"] = data["Date"].apply(self._same_day)

        data["Date"][0] = np.nan
        data = data.reset_index()

        # Note the inices where the df changes day
        day_indices_lst = data.index[data["Date"] == 1].tolist()
        data = data.set_index("ts")
        data = data.drop(columns=["Date"])

        # Chunk stock df into df for each day
        stock_letter_df_chunk_lst = []
        day_indices_lst.insert(0, 0)
        for j in range(len(day_indices_lst) - 1):
            index_1 = day_indices_lst[j]
            index_2 = day_indices_lst[j + 1]
            stock_letter_df_chunk = data.iloc[index_1:index_2, :]
            stock_letter_df_chunk_lst.append(stock_letter_df_chunk)

        return stock_letter_df_chunk_lst

    def _same_day(self, x: int) -> int:
        """
        Mask value with np.nan if it is the first value of the day. 1
        otherwise.
        """
        if not x:
            return np.nan

        else:
            return 1

    def _returns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate log returns of neighbouring data points in data."""
        returns = np.log(data["price"] / data.shift(1)["price"])

        return returns.dropna()
