import nsepy as ny
import concurrent.futures
import pprint
import datetime
import time
from numpy.core.defchararray import split
import pandas as pd
import logging
from pynse import *
import numpy as np
from datetime import  date, timedelta
from swing_trade_logic import *




def swing_backtest(symbols,start,end):
    for i in range(start, end):
        pass

nse = Nse()
symbols = nse.symbols[IndexSymbol.Nifty50.name]

stock_value = get_multiple_stock_data(symbols)
df = pd.DataFrame(stock_value).transpose()
df = df.reset_index()
df = df.rename(columns={"index": "Symbol"})

trading_days = nse.get_hist(from_date=datetime.date(2021,1,1)).index

# print(trading_days)
for td in trading_days:
    # print(td, td.year, td.month)
    pass

test = nse.get_hist(symbols[0],from_date=trading_days[0],to_date=trading_days[-1])
print(symbols[0], test)
tmp = np.unique(np.array(test.index.strftime('%Y-%m')))
print(tmp)

                 
def get_multiple_stock_hist(symbols,start,end):

    df = pd.DataFrame()
    for sym in symbols:
        print('fetching... ', sym)
        temp = pd.DataFrame()
        temp = nse.get_hist(sym,from_date=start,to_date=end)
        temp['Symbol'] = sym
        temp = temp.reset_index()
        tmp_months = np.unique(np.array(test.index.strftime('%Y-%m')))
        for t in tmp_months:
            year = int(t.split('-')[0])
            month = int(t.split('-')[1])
            # temp[["lastmonthHighClosing","lastmonthLowClosing","lastmonthHigh","lastmonthLow"]] = last_Month_hloc(sym,year,month)
            temp.loc[(temp['Date'].dt.year == year) & (temp['Date'].dt.month == month),["lastmonthHighClosing","lastmonthLowClosing","lastmonthHigh","lastmonthLow"]] = last_Month_hloc(sym,year,month)
        # year = trading_days[0].year
        # month = trading_days[0].month
        
        df = df.append(temp)
    return df
    
df = get_multiple_stock_hist(symbols,trading_days[0],trading_days[-1])
# print(trading_days[0].year)
year = trading_days[0].year
month = trading_days[0].month
df = df.reset_index()
df[["avgVol"]] = df["Symbol"].apply(lambda val : vol_TA_pivt(val))
df["priceCrossMonthHigh"] = np.where((df["Close"]>df["lastmonthHighClosing"]) & (df["Open"]< df["lastmonthHighClosing"]),"Yes","No")
df["Vol>avgVOl"] = np.where((df["Volume"]>df["avgVol"]),"Yes","No")
# df[["lastmonthHighClosing","lastmonthLowClosing","lastmonthHigh","lastmonthLow"]] = df["Symbol"].apply(lambda val:last_Month_hloc(val, year, month))
# df[["lastmonthHighClosing","lastmonthLowClosing","lastmonthHigh","lastmonthLow"]] = last_Month_hloc()
print(df)







