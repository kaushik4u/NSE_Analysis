#/usr/bin/python3

from datetime import time
import json
from os import error
import pandas as pd
from banknifty_goldenrule import plot_strategy

with open('ticks.json', mode='r', encoding='utf-8') as f:
    ticks = json.load(f) 

print(ticks[35][0]['tvalue'])
print(ticks[35])
i = 34
print(ticks[i][0]['tvalue'], ticks[i][1]['c']) # close price


ltp = []
timeticks = []
print(len(ticks))
for i in range(4,len(ticks)):
    try:
        ltp.append(ticks[i][1]['ltp'])
        timeticks.append(ticks[i][0]['tvalue'])
    except (IndexError, KeyError):
        # print(i,ticks[i])
        pass

# for i in range(4,len(ticks)):
#     if (ticks[i][0] and ticks[i][1]):
#         print(i, ticks[i][0], ticks[i][1])
#         timeticks.append(ticks[i][0]['tvalue'])
#         ltp.append(ticks[i][1]['ltp'])
    
d = {'ts':timeticks,'ltp':ltp}
# df = pd.DataFrame(data=[timeticks,ltp], columns=['ts','ltp'])
df = pd.DataFrame(d)
print(df.head())
print(len(df['ts']))

# df['ts'] = pd.to_datetime(df['ts'], format='%d/%m/%Y %H:%M:%S')
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format = True)
df = df.set_index('ts')
df = df.apply(pd.to_numeric, errors = 'coerce')
print(df.head())
print(df.dtypes)
ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close': 'last','volume':'sum'}
# df_1_min = df['ltp'].resample('1min').apply(ohlc_dict).dropna()
df_1_min = df['ltp'].resample('1min').ohlc()
print(df_1_min.head())

df_5_min = df['ltp'].resample('5min').ohlc()
print(df_5_min.head())

