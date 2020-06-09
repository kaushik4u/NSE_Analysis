import pandas as pd
import numpy as np
from datetime import datetime
import json

with open('./data/temp/test_data/nifty50.json') as f:
    data = json.load(f)

tickers = []
for i in range(len(data)):
    tickers.append(data[i]['chart']['result'][0]['meta']['symbol'])

# df = format_data_for_candlestick(35)

ticker_index = 50


def format_data_for_candlestick(ticker_index):
    timedata = timedata= []
    open = high = low = close = volume = []
    for i in range(len(data[ticker_index]['chart']['result'][0]['timestamp'])):    
        timedata.append(datetime.fromtimestamp(data[ticker_index]['chart']['result'][0]['timestamp'][i]))
    open = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['open']
    high = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['high']
    close = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['close']
    low = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['low']
    volume = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['volume']
    temp = {'datetime':timedata,'Open':open,'Low':low,'High':high,'Close':close,'Volume':volume}
    df = pd.DataFrame(temp)
    df.set_index('datetime',inplace=True)
    # df = format_data_for_candlestick(ticker_index)
    df_onemin = df

    

    ohlc_dict = {'Open':'first', 'High':'max', 'Low':'min', 'Close': 'last','Volume':'sum'}
    df = df.resample("5min").apply(ohlc_dict).dropna()
    # df_day = df.resample("1D").apply(ohlc_dict).dropna()

    # df['vwap'] = (df['Volume']*(df['High']+df['Low']+df['Close'])/3).cumsum() / df['Volume'].cumsum()
    df['vwap'] = (df_onemin['Volume']*(df_onemin['High']+df_onemin['Low']+df_onemin['Close'])/3).rolling(min_periods=1,window=5).sum() / df_onemin['Volume'].rolling(min_periods=1,window=5).sum()


    # print(df_day)
    # df = pivot_points(df)
    # print(df)

    return df

def pivot_points(df):
    ohlc_dict = {'Open':'first', 'High':'max', 'Low':'min', 'Close': 'last','Volume':'sum'}
    df_day = df.resample("1D").apply(ohlc_dict).dropna()

    # df['P'] = (df['High'] + df['Low'] + df['Close'])/3
    # df['R1'] = (df['P'] * 2) - df['Low']
    # df['S1'] = (df['P'] * 2) - df['High']
    # df['R2'] = df['P'] + (df['High'] - df['Low'])
    # df['S2'] = df['P'] - (df['High'] - df['Low'])

    df_day['P'] = (df_day['High'].shift(-1) + df_day['Low'].shift(-1) + df_day['Close'].shift(-1))/3
    df_day['R1'] = (df_day['P'] * 2) - df_day['Low'].shift(-1)
    df_day['S1'] = (df_day['P'] * 2) - df_day['High'].shift(-1)
    df_day['R2'] = df_day['P'] + (df_day['High'].shift(-1) - df_day['Low'].shift(-1))
    df_day['S2'] = df_day['P'] - (df_day['High'].shift(-1) - df_day['Low'].shift(-1))
    
    # P = (df_day['High'] + df_day['Low'] + df_day['Close'])/3
    # R1 = (df_day['P'] * 2) - df_day['Low']
    # S1 = (df_day['P'] * 2) - df_day['High']
    # R2 = df_day['P'] + (df_day['High'] - df_day['Low'])
    # S2 = df_day['P'] - (df_day['High'] - df_day['Low'])

    

    df = df_day    

    return df


def fibbonacci_retracement(df):
    look_back_period = 895
    c = 0 

    ON = []
    SS = []
    TT = []
    ZZ = [] 


    for i in df['Close']:
        if c + look_back_period < len(df): 
            df2 = df.iloc[c : c + look_back_period, : ]
            maxr = df2['Close'].max()
            minr = df2['Close'].min()
            ranr = maxr - minr 

            ON.append(maxr)
            SS.append(maxr - 0.236 * ranr)
            TT.append(minr + 0.236 * ranr)
            ZZ.append(minr)
            c = c + 1
        else: 
            break 



    df = df.head(-look_back_period)
    df['ON'] = ON 
    df['SS'] = SS
    df['TT'] = TT
    df['ZZ'] = ZZ

    return df


# df = format_data_for_candlestick(ticker_index)
# df_onemin = df

# ohlc_dict = {'Open':'first', 'High':'max', 'Low':'min', 'Close': 'last','Volume':'sum'}
# df = df.resample("5min").apply(ohlc_dict).dropna()

# # df['vwap'] = (df['Volume']*(df['High']+df['Low']+df['Close'])/3).cumsum() / df['Volume'].cumsum()
# df['vwap'] = (df['Volume']*(df['High']+df['Low']+df['Close'])/3).rolling(min_periods=1,window=5).sum() / df['Volume'].rolling(min_periods=1,window=5).sum()
# # for i in df.index:
# #     # df['vwap'][i]
# #     print((df['Volume'][i]*(df['High'][i]+df['Low'][i]+df['Close'][i])/3).cumsum() / df['Volume'][i].cumsum())

# print(df)

"""
test condition: BUY if VWAP < CLOSE and SELL if VWAP > CLOSE
Time bound: 9:30 - 11:30
"""
start = datetime(2020,6,7,9,30,0)
end = datetime(2020,6,7,11,30,0)

# after_start = df['datetime'] >= start
# before_end = df['datetime'] <= end
# between_two_dates = after_start & before_end
# filtered_dates = df.loc[between_two_dates]

# print(start , end)

# df1 = df[(df['datetime'] > '2020-5-18 09:30:00') & (df['datetime'] <= '2020-5-18 11:30:00')]
# df1 = df['2020-5-18 09:30:00':'2020-5-18 11:30:00']
# print(df1)

# trade_taken = {
#     'Price': 0,
#     'Buy': False,
#     'Sell': False,
#     'Profit_margin': 1.02,
#     'Stoploss': 1,
#     'result': None
# }
# print(tickers[ticker_index])

# Buy side
# for i in df1.index:
#     # print(i, df1['Close'][i],df1['vwap'][i])
#     if df1['Close'][i] > df1['vwap'][i] and trade_taken['Buy'] !=True:
#         print('BUY : ' ,i , df1['Close'][i], df1['vwap'][i])
#         trade_taken['Buy'] = True
#         trade_taken['Price'] = df1['Close'][i]
#     elif df1['Close'][i] >= trade_taken['Price'] * 1.02 and trade_taken['Buy'] and trade_taken['Sell'] != True:
#         print('SELL : ' ,i , df1['Close'][i], df1['vwap'][i], df1['Close'][i] - trade_taken['Price'])
#         trade_taken['Sell'] = True
#     elif df1['Close'][i] <= trade_taken['Price'] * .99 and trade_taken['Buy'] and trade_taken['Sell'] != True:
#         print('SELL : ' ,i , df1['Close'][i], df1['vwap'][i], df1['Close'][i] - trade_taken['Price'])
#         trade_taken['Sell'] = True
#     elif i == df1.index[-1]:
#         print('No profitable Trade conditions!')

# trade_taken = {
#     'Price': 0,
#     'Buy': False,
#     'Sell': False,
#     'Profit_margin': 1.02,
#     'Stoploss': 1,
#     'result': None
# }

# # Sell side
# for i in df1.index:
#     # print(i, df1['Close'][i],df1['vwap'][i])
#     if df1['Close'][i] > df1['vwap'][i] and trade_taken['Sell'] !=True:
#         print('SELL : ' ,i , df1['Close'][i], df1['vwap'][i])
#         trade_taken['Sell'] = True
#         trade_taken['Price'] = df1['Close'][i]
#     elif df1['Close'][i] >= trade_taken['Price'] * .98 and trade_taken['Sell'] and trade_taken['Buy'] != True:
#         print('Buy : ' ,i , df1['Close'][i], df1['vwap'][i], trade_taken['Price'] - df1['Close'][i])
#         trade_taken['Buy'] = True
#     elif df1['Close'][i] <= trade_taken['Price'] * 1.01 and trade_taken['Sell'] and trade_taken['Buy'] != True:
#         print('Buy : ' ,i , df1['Close'][i], df1['vwap'][i], df1['Close'][i] - trade_taken['Price'])
#         trade_taken['Buy'] = True
#     elif i == df1.index[-1]:
#         print('No profitable Trade conditions!')

def trade_conditions(df1,side,trade_taken):    
    if side == "BUY":
        # Buy side
        for i in df1.index:    
            if df1['Close'][i] > df1['vwap'][i] and trade_taken['Buy'] !=True:
                print('BUY : ' ,i , df1['Close'][i], df1['vwap'][i])
                trade_taken['Buy'] = True
                trade_taken['Price'] = df1['Close'][i]
            elif df1['Close'][i] >= trade_taken['Price'] * 1.02 and trade_taken['Buy'] and trade_taken['Sell'] != True:
                print('SELL : ' ,i , df1['Close'][i], df1['vwap'][i], df1['Close'][i] - trade_taken['Price'])
                print('P/L : ',df1['Close'][i] - trade_taken['Price'])
                trade_taken['Sell'] = True
            elif df1['Close'][i] <= trade_taken['Price'] * .99 and trade_taken['Buy'] and trade_taken['Sell'] != True:
                print('SELL : ' ,i , df1['Close'][i], df1['vwap'][i], df1['Close'][i] - trade_taken['Price'])
                print('P/L : ',df1['Close'][i] - trade_taken['Price'])
                trade_taken['Sell'] = True
            elif i == df1.index[-1]:
                print('No profitable Trade conditions!')
            # Sell side
    if side == "SELL":
        for i in df1.index:
            # print(i, df1['Close'][i],df1['vwap'][i])
            if df1['Close'][i] < df1['vwap'][i] and trade_taken['Sell'] !=True:
                print('SELL : ' ,i , df1['Close'][i], df1['vwap'][i])
                trade_taken['Sell'] = True
                trade_taken['Price'] = df1['Close'][i]
            elif df1['Close'][i] <= trade_taken['Price'] * .98 and trade_taken['Sell'] and trade_taken['Buy'] != True:
                print('BUY : ' ,i , df1['Close'][i], df1['vwap'][i], trade_taken['Price'] - df1['Close'][i])
                print('P/L : ',trade_taken['Price'] - df1['Close'][i])
                trade_taken['Buy'] = True
            elif df1['Close'][i] >= trade_taken['Price'] * 1.01 and trade_taken['Sell'] and trade_taken['Buy'] != True:
                print('BUY : ' ,i , df1['Close'][i], df1['vwap'][i], df1['Close'][i] - trade_taken['Price'])
                print('P/L : ',df1['Close'][i] - trade_taken['Price'])
                trade_taken['Buy'] = True
            elif i == df1.index[-1]:
                print('No profitable Trade conditions!')

# print(df1)



# print(filtered_dates)

# trade_conditions(df1,"SELL",trade_taken)

with open('./nifty200.txt') as f:
    symbols = f.readlines()

# print(symbols)



trades_setup = [
    {
        'ticker':'CHOLAFIN',
        'side':'SELL'
    },
    {
        'ticker':'APOLLOTYRE',
        'side':'BUY'
    },
    {
        'ticker':'AMARAJABAT',
        'side':'BUY'
    },
    {
        'ticker':'BEL',
        'side':'SELL'
    },
    {
        'ticker':'VEDL',
        'side':'BUY'
    },
    {
        'ticker':'SBIN',
        'side':'SELL'
    },
    {
        'ticker':'ICICIBANK',
        'side':'SELL'
    },
    {
        'ticker':'TATAMOTORS',
        'side':'SELL'
    }
]

for i in range(len(trades_setup)):    
    print(symbols.index(trades_setup[i]['ticker']+'\n'),trades_setup[i]['ticker'],trades_setup[i]['side'])
    trade_taken = {
    'Price': 0,
    'Buy': False,
    'Sell': False,
    'Profit_margin': 1.02,
    'Stoploss': 1,
    'result': None
    }
    df = format_data_for_candlestick(symbols.index(trades_setup[i]['ticker']+'\n'))
    trade_conditions(df,trades_setup[i]['side'],trade_taken)
    # print(fibbonacci_retracement(df))
