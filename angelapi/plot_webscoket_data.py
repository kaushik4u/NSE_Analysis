#/usr/bin/python3

from datetime import time
import json
from os import error
import pandas as pd
from banknifty_goldenrule import plot_strategy
import time

ticks_file = 'ticks.json'
# ticks_file = 'ticks - Copy (3).json'
def read_ticks():
    with open(ticks_file, mode='r', encoding='utf-8') as f:
        try:
            ticks = json.load(f) 
        except:
            print('file is being used by other process!')
            time.sleep(5)
            read_ticks()

# read_ticks()
ticks_file = './myticks.txt'
def read_my_ticks():
    with open(ticks_file, mode='r', encoding='utf-8') as f:
        ticks = f.readlines()
    return ticks
        # try:
        #     ticks = f.readlines() 
        # except:
        #     print('file is being used by other process!')

ticks = read_my_ticks()
# print(ticks)
# exit()
# with open(ticks_file, mode='r', encoding='utf-8') as f:
#     try:
#         ticks = json.load(f) 
#     except:
#         print('file is being used by other process!')
#         exit()
    

# print(ticks[35][0]['tvalue'])
# print(ticks[35])
i = 34
# print(ticks[i][0]['tvalue'], ticks[i][1]['c']) # close price


ltp = []
timeticks = []
# print(len(ticks))

def convert_ticks2df():
    for i in range(len(ticks)):
        timeticks.append(ticks[i].split('=')[0].strip())
        ltp.append(ticks[i].split('=')[1].strip())

convert_ticks2df()
print(timeticks,ltp)
# for i in range(4,len(ticks)):
#     try:
#         ltp.append(ticks[i][1]['ltp'])
#         timeticks.append(ticks[i][0]['tvalue'])
#     except (IndexError, KeyError):
#         # print(i,ticks[i])
#         pass

# for i in range(4,len(ticks)):
#     if (ticks[i][0] and ticks[i][1]):
#         print(i, ticks[i][0], ticks[i][1])
#         timeticks.append(ticks[i][0]['tvalue'])
#         ltp.append(ticks[i][1]['ltp'])
    
d = {'ts':timeticks,'ltp':ltp}
# df = pd.DataFrame(data=[timeticks,ltp], columns=['ts','ltp'])
df = pd.DataFrame(d)
print(df.head())
# print(len(df['ts']))

# df['ts'] = pd.to_datetime(df['ts'], format='%d/%m/%Y %H:%M:%S')
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format = True)
df = df.set_index('ts')
# df['Date'] = pd.to_datetime(df['ts'], infer_datetime_format = True)
# df['Date'] = pd.to_datetime(df['ts'], format='%d/%m/%Y %H:%M:%S')
# 
# df = df.set_index('Date')
df = df.apply(pd.to_numeric, errors = 'coerce')
print(df.head())
print(df.dtypes)
ohlc_dict = {'Open':'first', 'High':'max', 'Low':'min', 'Close': 'last','Volume':'sum'}
# df_1_min = df['ltp'].resample('1min').apply(ohlc_dict).dropna()



df_1_min = df['ltp'].resample('1min').ohlc()

# df_1_min.index.name  = ['Date']

df_1_min.columns = ['Open', 'High', 'Low', 'Close']
df_1_min['Date'] = df_1_min.index
# df_1_min['Date'] = df_1_min['Date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
df_1_min['Date'] = pd.to_datetime(df_1_min['Date'], infer_datetime_format = True).dt.tz_localize('Asia/Kolkata')
# # df_1_min.reset_index(drop=True, inplace=True)
# df_1_min['h_close'] = (df_1_min['Open']+df_1_min['Close']+df_1_min['High']+df_1_min['Low']) * 0.25
df_1_min.reset_index(level=0, inplace=True)
df_1_min = df_1_min.set_index('Date')

print(df_1_min.head())

df_5_min = df['ltp'].resample('5min').ohlc()
print(df_5_min.head())

# df_1_min['Date'] = df_1_min.index
# df_1_min['Open'] = df_1_min.open
# df_1_min['High'] = df_1_min.high
# df_1_min['Low'] = df_1_min.low
# df_1_min['Close'] = df_1_min.close

# def plot_heikin_ashi(df, ax):
#     # df['h_close'] = (df.Open+df.Close+df.High+df.Low) * 0.25
#     df['h_close'] = (df['Open']+df['Close']+df['High']+df['Low']) * 0.25
#     # df['h_open'] = (df.Open.shift()+df.Close.shift()) * 0.5
#     df['h_open'] = (df['Open'].shift()+df['Close'].shift()) * 0.5
#     df['h_high'] = df[['High','h_open','h_close']].max(axis=1)
#     df['h_low'] = df[['Low','h_open','h_close']].min(axis=1)
#     candles = df['Date h_open h_close h_high h_low'.split()]
    # candles = df['df.index h_open h_close h_high h_low'.split()]
    # fplt.candlestick_ochl(candles, ax=ax)

# plot_heikin_ashi(df_1_min,None)
# plot_strategy(df_1_min)