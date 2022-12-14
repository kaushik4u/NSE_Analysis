import nsepy as ny
import concurrent.futures
import pprint
import datetime
import time
import pandas as pd
import logging
from pynse import *
import numpy as np
from datetime import timedelta
import openpyxl
from datetime import datetime


nse = Nse()
start1 = time.time()
print(start1)
# symbols=["tcs","infy","ioc","upl","m&mfin","Reliance","Hdfc","Axisbank","HDFCbank","ICICIBANK","SBIN"]
symbols = ["ACC", "ABBOTINDIA", "ADANIENT", "ADANIGREEN", "ADANIPORTS", "ADANITRANS", "ALKEM", "AMBUJACEM",
           "APOLLOHOSP", "ASIANPAINT", "AUROPHARMA", "DMART", "AXISBANK", "BAJFINANCE", "BAJAJFINSV", "BAJAJHLDNG",
           "BANDHANBNK", "BERGEPAINT", "BPCL", "BAJAJ-AUTO", "BHARTIARTL", "BIOCON", "BOSCHLTD", "BRITANNIA",
           "CADILAHC", "CIPLA", "COALINDIA", "COLPAL", "DLF", "DABUR", "DIVISLAB", "DRREDDY", "EICHERMOT", "GAIL",
           "GODREJCP", "GRASIM", "HCLTECH", "HDFCAMC", "HDFCBANK", "HDFCLIFE", "HAVELLS", "HEROMOTOCO", "HINDALCO",
           "HINDPETRO", "HINDUNILVR", "HDFC", "ICICIBANK", "ICICIGI", "ICICIPRULI", "ITC", "IOC", "IGL", "INDUSINDBK",
           "MCDOWELL-N", "NAUKRI", "INFY", "INDIGO", "JSWSTEEL", "JUBLFOOD", "KOTAKBANK", "LTI", "LT", "LUPIN", "MRF",
           "M&M", "MARICO", "MARUTI", "MUTHOOTFIN", "NMDC", "NTPC", "NESTLEIND", "ONGC", "PETRONET", "PIDILITIND",
           "PEL", "POWERGRID", "PGHH", "PNB", "RELIANCE", "SBICARD", "SBILIFE", "SHREECEM", "SIEMENS", "SBIN",
           "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TECHM", "TITAN", "TORNTPHARM", "UPL",
           "ULTRACEMCO", "UBL", "VEDL", "WIPRO", "YESBANK"]


# symbols=["m&m"]
# pprint.pprint(ny.get_quote(symbol.replace("&","%26"))["data"][0])
def data(symbol):
    data_nse = ny.get_quote(symbol.replace("&", "%26"))["data"][0]
    return {symbol.upper(): {"Open": float(data_nse["open"].replace(",", "")),
                             "High": float(data_nse["dayHigh"].replace(",", "")),
                             "Low": float(data_nse["dayLow"].replace(",", "")),
                             "Close": float(data_nse["lastPrice"].replace(",", "")),
                             "Volume": float(data_nse["totalTradedVolume"].replace(",", "")),
                             "Delivery": float(data_nse["deliveryToTradedQuantity"].replace(",", "").replace("-", "0")),
                             "vwap": float(data_nse["averagePrice"].replace(",", ""))}
            }


def get_multiple_stock_data(symbol_list):
    multiple_stock = {}
    #     for i in symbol_list:
    #         single_stock=data(i)
    #         for k,v in single_stock.items():
    #             multiple_stock[k]=v
    with concurrent.futures.ThreadPoolExecutor() as ex:
        results = ex.map(data, symbol_list)
        for result in results:
            for k, v in result.items():
                multiple_stock[k] = v
    return multiple_stock


stock_value = get_multiple_stock_data(symbols)
df = pd.DataFrame(stock_value).transpose()
df = df.reset_index()
df = df.rename(columns={"index": "Symbol"})


def last_Month_hloc(symbols):
    stockdata = nse.get_hist(symbols, from_date=dt.date(2021, 8, 1), to_date=dt.date(2021, 8, 31))
    x = stockdata["close"]
    y = stockdata["open"]
    z = stockdata["high"]
    z1 = stockdata["low"]
    c = x.tolist()

    lastmonthHighC = max(x.max(), y.max())
    lastmonthlowC = min(x.min(), y.min())
    lastmonthHigh = z.max()
    lastmonthLow = z1.min()
    if c:
        lastmonthclose = x[-1]
    else:
        lastmonthclose = 0

    listy = [lastmonthHighC, lastmonthlowC, lastmonthHigh, lastmonthLow, lastmonthclose]
    return pd.Series(listy)


def vol_TA_pivt(symbols):
    y = 0
    sum1 = 0
    vma = 5
    # today=date.today()
    today = dt.date(2021, 9, 8)
    endDate = today + timedelta(days=-1)
    startDate = today + timedelta(days=-10)
    stockdata = nse.get_hist(symbols, from_date=startDate, to_date=endDate)
    # stockdata = ny.get_history(symbol=symbols, start=startDate, end=endDate)
    length = len((stockdata.index))
    for i in range(length - 1, 0, -1):
        if y == vma:
            break
        sum1 = stockdata["volume"][i] + sum1
        y = y + 1
    avgvol = sum1 / vma
    return avgvol


def PPSR(df):
    PP = pd.Series((df['lastmonthHigh'] + df['lastmonthLow'] + df['lastmonthclose']) / 3)
    R1 = pd.Series(2 * PP - df['lastmonthLow'])
    S1 = pd.Series(2 * PP - df['lastmonthHigh'])
    R2 = pd.Series(PP + df['lastmonthHigh'] - df['lastmonthLow'])
    S2 = pd.Series(PP - df['lastmonthHigh'] + df['lastmonthLow'])
    R3 = pd.Series(df['lastmonthHigh'] + 2 * (PP - df['lastmonthLow']))
    S3 = pd.Series(df['lastmonthLow'] - 2 * (df['lastmonthHigh'] - PP))
    psr = {'PP': PP, 'R1': R1, 'S1': S1, 'R2': R2, 'S2': S2, 'R3': R3, 'S3': S3}
    PSR = pd.DataFrame(psr)
    df = df.join(PSR)
    return df

def calculate_ema(symbols):
    smoothing = 2
    days=40
    price = nse.get_hist(symbols, from_date=dt.date(2021, 4, 1), to_date=dt.date(2021, 9, 12))
    prices=price["close"]
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    EMA=ema[-1]
    return EMA


df[["lastmonthHighClosing", "lastmonthLowClosing", "lastmonthHigh", "lastmonthLow", "lastmonthclose"]] = df[
    "Symbol"].apply(lambda val: last_Month_hloc(val))

df[["avgVol"]] = df["Symbol"].apply(lambda val: vol_TA_pivt(val))
df[["40EMA"]]=df["Symbol"].apply(lambda val: calculate_ema(val))

df["priceCrossMonthHigh"] = np.where(
    (df["Close"] > df["lastmonthHighClosing"]) & (df["Open"] < df["lastmonthHighClosing"]), "Yes", "No")

df["Vol>avgVOl"] = np.where((df["Volume"] > df["avgVol"]), "Yes", "No")

df = PPSR(df)
def targetSL(df):
    target,SL=0,0
    if df["S3"]>df["Close"]:
        target=df["S3"]
        SL=df["Close"]*.98
    elif df["S3"]<df["Close"] and df["S2"]>df["Close"]:
        target=df["S2"]
        SL=df["S3"]
    elif df["S2"]<df["Close"] and df["S1"]>df["Close"]:
        target=df["S1"]
        SL=df["S2"]
    elif df["S1"]<df["Close"] and df["PP"]>df["Close"]:
        target=df["PP"]
        SL=df["S1"]
    elif df["PP"]<df["Close"] and df["R1"]>df["Close"]:
        target=df["R1"]
        SL=df["PP"]
    elif df["R1"]<df["Close"] and df["R2"]>df["Close"]:
        target=df["R2"]
        SL=df["R1"]
    elif df["R2"]<df["Close"] and df["R3"]>df["Close"]:
        target=df["R3"]
        SL=df["R2"]
    elif df["R3"]<df["Close"]:
        target=df["Close"]*5
        SL=df["R3"]
    list=[target,SL]
    return pd.Series(list)

df[['Target','SL']] = df.apply(targetSL, axis=1)


pprint.pprint(df)
end1 = time.time()
print(end1)
print(end1 - start1)

today1 = datetime.now()
file_name = 'Analysis_' + str(today1)
file_name = file_name.strip()
file_name = file_name.split(".", 1)[0]
file_name = file_name.replace(":", "").replace(" ", "_")
file_name = file_name + '.xlsx'
# saving the excel
df.to_excel("C:\\Users\\SOURAV\\Desktop\\Files\\"+file_name)
print('DataFrame is written to Excel File successfully.')
