# Equity_Volatility_Analysis

Note: This task was under time pressure, with more time there are many improvements i would make. For instance, the ARIMA model script would much better
suit a Jupyter notebook and the rest of the scripts could be made into functions/classes etc.


Summary: This project aims to analyse the relationship between liquidity and volatility of four 'fictional' stocks using intraday trading data. I choose
trading volume and realised volatility (RV) to indicate liquidity and volatility. Later, i attempt to predict the stocks return in the week following the 
dataset using an ARIMA model.

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

Scripts/Folders:

cleaning.py - Takes the raw data and cleans it according to a process outlined in my report. Run this script directly to get statistics about the cleaned
data

processing.py - Calculates the correlation matrix between daily RV (calculated from 5-minute returns from each day) and daily volume and processes the data.

processing_hourly_return.py - Calculates the correlation matrix between daily RV (calculated from hourly mean price which itself is calculated 
from the 5-minute returns from each day) and daily volume

processing_alt_data.py - Calculated the correlation matrix between daily RV (calculated from hourly returns) and daily volume using alternative stock/ETF 
data from kaggle

ARIMA_analysis.py - Perform tests to choose ARIMA model parameters and then perform ARIMA model prediction

data - csv files containing raw stock/ETF data

figures - an output folder for figures produces

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

Each script calls the relevant ones so you can run ARIMA_analysis.py first or call individual scripts for correlation matrices etc.

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>





