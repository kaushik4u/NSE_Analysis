import nsepy as ny
import concurrent.futures
import pprint
import datetime
import time
import pandas as pd
import logging
from pynse import *
import numpy as np
from datetime import  date, timedelta

nse = Nse()
start1 = time.time()
# print(start1)
symbols=["tcs","infy","ioc","upl","m&mfin","Reliance","Hdfc","Axisbank","HDFCbank","ICICIBANK","SBIN"]

#pprint.pprint(ny.get_quote(symbol.replace("&","%26"))["data"][0])
def data(symbol):
    data_nse = ny.get_quote(symbol.replace("&","%26"))["data"][0]
    
    return {symbol.upper():{"Open":float(data_nse["open"].replace(",","")),
                       "High":float(data_nse["dayHigh"].replace(",","")),
                       "Low":float(data_nse["dayLow"].replace(",","")),
                       "Close":float(data_nse["lastPrice"].replace(",","")),
                       "Volume":float(data_nse["totalTradedVolume"].replace(",","")),
                       "Delivery":float(data_nse["deliveryToTradedQuantity"].replace(",","")),
                       "vwap":float(data_nse["averagePrice"].replace(",",""))}
                      }
   
   

def get_multiple_stock_data(symbol_list):
   
    multiple_stock={}
#     for i in symbol_list:
#         single_stock=data(i)
#         for k,v in single_stock.items():
#             multiple_stock[k]=v
    with concurrent.futures.ThreadPoolExecutor() as ex:
        results= ex.map(data,symbol_list)
        for result in results:
                for k,v in result.items():
                    multiple_stock[k]=v
    return multiple_stock







def last_Month_hloc(symbols, year, month):
    month_end = datetime.date(year + int(month/12), month%12+1, 1)-datetime.timedelta(days=1)
    # stockdata = nse.get_hist(symbols, from_date=dt.date(year,month,1),to_date=dt.date(year,month,30))
    stockdata = nse.get_hist(symbols, from_date=dt.date(year,month,1),to_date= month_end)
    x=stockdata["close"]
    y=stockdata["open"]
    z=stockdata["high"]
    z1=stockdata["low"]
   
    lastmonthHighC = max(x.max(),y.max())
    lastmonthlowC = min(x.min(),y.min())
    lastmonthHigh = z.max()
    lastmonthLow = z1.min()
   
    listy=[lastmonthHighC,lastmonthlowC,lastmonthHigh,lastmonthLow]
    return pd.Series(listy)

def vol_TA_pivt(symbols):
    y = 0
    sum1 = 0
    vma = 5
    today = date.today()
    # today=dt.date(2021,8,27)
    endDate = today + timedelta(days=-1)
    startDate = today + timedelta(days=-10)
    stockdata = nse.get_hist(symbols, from_date = startDate, to_date = endDate)
    #stockdata = ny.get_history(symbol=symbols, start=startDate, end=endDate)
    length=len((stockdata.index))
    for i in range(length-1,0,-1):
        if y == vma:
            break
        sum1 = stockdata["volume"][i] + sum1
        y = y+1
    avgvol = sum1/vma
    return avgvol




   


# end1 = time.time()
# print(end1)
# print(end1 - start1)

if __name__ == "__main__":
    symbols = nse.symbols[IndexSymbol.Nifty50.name]

    print(symbols)

    stock_value = get_multiple_stock_data(symbols)
    df = pd.DataFrame(stock_value).transpose()
    df = df.reset_index()
    df = df.rename(columns={"index": "Symbol"})
    year = 2021
    month = 8
    df[["lastmonthHighClosing","lastmonthLowClosing","lastmonthHigh","lastmonthLow"]] = df["Symbol"].apply(lambda val:last_Month_hloc(val, year, month))

    df[["avgVol"]] = df["Symbol"].apply(lambda val : vol_TA_pivt(val))

    df["priceCrossMonthHigh"] = np.where((df["Close"]>df["lastmonthHighClosing"]) & (df["Open"]< df["lastmonthHighClosing"]),"Yes","No")

    df["Vol>avgVOl"] = np.where((df["Volume"]>df["avgVol"]),"Yes","No")


    pprint.pprint(df)