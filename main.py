import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt 
from pandas_datareader import data as pdr

yf.pdr_override()

# stock = input("Enter a stock ticker symbol: ")
stock = "QQQ"

print(stock)

start = dt.datetime(2019, 1, 1)
now = dt.datetime.now()

df = pdr.get_data_yahoo(stock, start, now)

moving_avarage = 50
sma_string = "Sma_" + str(moving_avarage)

df[sma_string] = df.iloc[:,4].rolling(window=moving_avarage).mean()
df = df.iloc[moving_avarage:]


for row in df.index:
    if df["Adj Close"][row] > df[sma_string][row]:
        print("Its higher")
    else:
        print("its lower")
    # print(df["Adj Close"][row])
    # print(df[][row])



# print(df)
