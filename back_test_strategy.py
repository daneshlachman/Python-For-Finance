import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt 
from pandas_datareader import data as pdr
import pdb

yf.pdr_override()

# stock = input("Insert stock ticker here: ")

stock = "ABN.AS"
stock = "ING"

print(stock)

# define starting date and current date
start = dt.datetime(2020, 4, 10)
now = dt.datetime.now()

df = pdr.get_data_yahoo(stock, start, now)


# define emas and add the ema's to existing df structure using pandas functions
emas = [3,5,8,10,12,15,30,35,40,45,50,60]
for ema in emas:
    df["Ema_"+ str(ema)] = round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)

pos = 0
index = 0
percent_changes = []

# loop through indexes and define the dates when ema's are profitible to buy and to sell.
for row in df.index:
    short_term_min = min(df["Ema_3"][row],df["Ema_5"][row],df["Ema_8"][row],df["Ema_10"][row],df["Ema_12"][row],df["Ema_15"][row],)
    long_term_max = max(df["Ema_30"][row],df["Ema_35"][row],df["Ema_40"][row],df["Ema_45"][row],df["Ema_50"][row],df["Ema_60"][row])

    close_price = df["Adj Close"][row]
    
    # if red line is higher than blue line, buy
    if short_term_min > long_term_max:
        if pos == 0:
            buy_price = close_price
            pos = 1
            print("Buying now at ", str(buy_price))

    # if red line is lower than blue line, sell
    elif short_term_min < long_term_max:
        if pos == 1:
            pos = 0
            sell_price = close_price
            print("Selling at", str(sell_price))
            change = (sell_price / buy_price -1) * 100
            percent_changes.append(change)

    # if last date found in df, sell as well
    elif index == df["Adj Close"].count() -1 and pos == 1:
        pos = 0
        sell_price = close_price
        print("Selling at", str(sell_price))
        change = (sell_price / buy_price -1) * 100
        percent_changes.append(change)
    index += 1

print("Percent changes: " + str(percent_changes))

gains = 0
number_of_gains = 0
losses = 0
number_of_losses=0
total_return = 1

# loop through the percent changes of the bought and sold stocks, 
# and keep up how many times profit/loss is made.
for percent_change in percent_changes:
	if percent_change > 0:
		gains += percent_change
		number_of_gains += 1
	else:
		losses += percent_change
		number_of_losses += 1
	total_return = total_return*((percent_change/100)+1)

total_return = round((total_return-1)*100,2)

if number_of_gains > 0:
	avg_gain = gains/number_of_gains
	max_return = str(max(percent_changes))
else:
	avg_gain = 0
	max_return = "no return available"

if number_of_losses > 0:
	avg_loss = losses/number_of_losses
	max_loss = str(min(percent_changes))
	ratio = str(-avg_gain /avg_loss)
else:
	avg_loss = 0
	max_loss = "no loss available"
	ratio = "no ratio available"

if (number_of_gains > 0 or number_of_losses > 0):
	batting_avg = number_of_gains/(number_of_gains+number_of_losses)
else:
	batting_avg = 0

# print all sorts of information about the stock analysis
print("Results for "+ stock +" going back to "+str(df.index[0])+", Sample size: "+str(number_of_gains+number_of_losses)+" trades")
print("EMAs used: "+str(emas))
print("Batting Avg: "+ str(batting_avg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avg_gain))
print("Average Loss: " + str(avg_loss))
print("Max Return: " + max_return)
print("Max Loss: " + max_loss)
print("Total return over " + str(number_of_gains+number_of_losses)+ " trades: "+ str(total_return)+"%" )