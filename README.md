# Equity_Volatility_Analysis
A tool to analyse the relationship between volatility and liquidity in high frequency stock trading data. I have included a small report summarising 
the details behind cleaning, processing and analysing the data. 

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

Scripts:

cleaning.py - Cleans the data according to the process in the report

processing.py - Finds the correlation matrix between volatility (realised volatility) and trading volume for each stock

functions.py - Includes useful functions i have defined

data/stock_A.csv - Unclean trading data for stock A (similarly for stocks B, C and D)

figures/ - Example plots which can be produces from the above scripts

Report.pdf - A brief report outlining my process

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

Instructions:

Simply run the processing script, it will call the relevant scripts and functions. If one wishes to gain insight into data regarding the data
cleaning (how many data points were removed for various reasons etc.) then run the cleaning script directly. 

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
