import requests
from datetime import datetime, timedelta
import json
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from finta import TA
import numpy as np

def fetch_live_feed(ticker):
    # print(int(datetime.now().timestamp()))
    prevDay = datetime.now() + timedelta(days=-5)
    # print(int(prevDay.timestamp()))
    yahoo_url= 'https://query1.finance.yahoo.com/v8/finance/chart/'+ ticker +'.NS?symbol='+ ticker +'.NS&period1='+ str(int(prevDay.timestamp())) +'&period2=' + str(int(datetime.now().timestamp())) +'&interval=1h'
    yahoo_url=  'https://query1.finance.yahoo.com/v8/finance/chart/' + ticker +'.NS?region=IN&lang=en-IN&includePrePost=false&interval=1h&range=1mo'
    print(yahoo_url)
    res = requests.get(yahoo_url)
    # print(res.text)
    fileName = ticker + '.json'
    with open('./data/temp/test_data/'+fileName, 'w', encoding='utf-8') as outfile:
        json.dump(json.JSONDecoder().decode(res.text), outfile)
    print('Data fetched : ', datetime.now().strftime('%d-%m-%Y %HH:%MM'))

def HA(df):
    df['HA_Close']=(df['Open']+ df['High']+ df['Low']+df['Close'])/4
    idx = df.index.name
    df.reset_index(inplace=True)
    for i in range(0, len(df)):
        if i == 0:
            df.set_value(i, 'HA_Open', ((df.get_value(i, 'Open') + df.get_value(i, 'Close')) / 2))
        else:
            df.set_value(i, 'HA_Open', ((df.get_value(i - 1, 'HA_Open') + df.get_value(i - 1, 'HA_Close')) / 2))
    if idx:
        df.set_index(idx, inplace=True)
    df['HA_High']=df[['HA_Open','HA_Close','High']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','Low']].min(axis=1)
    return df



ticker = 'AXISBANK'
srcPath = './data/temp/test_data/'

# fetch_live_feed(ticker)

with open(srcPath + ticker + '.json') as f:
    data = json.load(f)

# print(data['chart']['result'][0]['timestamp'])
# print(data['chart']['result'][0]['indicators']['quote'][0]['high'])

timedata= []
open = high = low = close = volume = []
for i in range(len(data['chart']['result'][0]['timestamp'])):
    # print(data['chart']['result'][0]['timestamp'][i], datetime.fromtimestamp(data['chart']['result'][0]['timestamp'][i]))
    timedata.append(datetime.fromtimestamp(data['chart']['result'][0]['timestamp'][i]))

open = data['chart']['result'][0]['indicators']['quote'][0]['open']
high = data['chart']['result'][0]['indicators']['quote'][0]['high']
close = data['chart']['result'][0]['indicators']['quote'][0]['close']
low = data['chart']['result'][0]['indicators']['quote'][0]['low']
volume = data['chart']['result'][0]['indicators']['quote'][0]['volume']

# for i in range(len(timedata)):
#     print(timedata[i],open[i],low[i],high[i],close[i],volume[i])

temp = {'datetime':timedata,'Open':open,'Low':low,'High':high,'Close':close,'Volume':volume}

df = pd.DataFrame(temp)
print(df)

ha_data = HA(df)
print(ha_data)
mpf_data = df
mpf_data.set_index('datetime',inplace=True)
print(mpf_data)
mpf_data = mpf_data.drop(['index','HA_Open','HA_Close','HA_High','HA_Low'], axis=1)
mpf_data.columns = ['Open','High','Low','Close','Volume']
ohlc_dict = {'Open':'first', 'High':'max', 'Low':'min', 'Close': 'last','Volume':'sum'}
mpf_data = mpf_data.resample("1H").apply(ohlc_dict).dropna()
print(mpf_data)
mpf.plot(mpf_data,type='candle',volume=True,show_nontrading=False,style='yahoo')
mpf_data['price_diff'] = mpf_data['Close'] - mpf_data['Open']
mpf_data['normalized_vol'] = (mpf_data['price_diff'].abs()/mpf_data['price_diff']) * mpf_data['Volume']
mpf_data['vol_momentum'] = mpf_data['price_diff'] * mpf_data['Volume']
# mpf_data = mpf_data.apply(vwap)
print(mpf_data[['Volume','Open','Close','price_diff','normalized_vol','vol_momentum']])

plt_df = mpf_data['vol_momentum'].groupby(pd.Grouper(freq='4H')).sum()
plt_df = plt_df[plt_df!=0]
# plt_df = plt_df.strftime('%d-%m %H:%M')
plt_df.index = plt_df.index.strftime('%d-%m %H:%M')
print(plt_df)
# plt_df.drop(plt_df[plt_df['normalized_vol']]==0,inplace=True)


# mpf_data['vol_momentum'].groupby(pd.Grouper(freq='1H')).sum().plot.bar()
# ax = plt.gca()
fig, ax = plt.subplots(figsize=(15,7))
fig.suptitle(ticker, fontsize=20)
# formatter = mdates.DateFormatter("%d-%m")
# formatter = matplotlib.dates.DateFormatter('%H:%M:%S')
# ax.xaxis.set_major_formatter(formatter)
#set ticks every week
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
#set major ticks format
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# plt.xticks(rotation=90)

# plt_df.plot(kind='bar',ax=ax,color=plt_df[plt_df>0].map({True: 'g', False: 'r'}))
clrs = ['green' if (y > 0) else 'red' for y in plt_df.values ]
plt_df.plot(kind='bar',ax=ax, color=clrs)
# print(TA.SMA(mpf_data, 20))
plt.draw()
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
plt.show()

plt_df = mpf_data['vol_momentum'].groupby(pd.Grouper(freq='1D')).sum()
plt_df = plt_df[plt_df!=0]
print(plt_df)
print(plt_df.index.get_loc('2020-04-29'))
print(plt_df[plt_df.index.get_loc('2020-04-29')-5:plt_df.index.get_loc('2020-04-29')])




def momentum_trend(ticker,df,date):
    date_loc = df.index.get_loc(date)
    # norm_vol_sum = df[date].sum()
    norm_vol_sum = df[date_loc - 5: date_loc].sum()
    if (norm_vol_sum > 0):
        trend = "up"
    else:
        trend = "down"
    
    print("\nDate :" + date + " ticker : " + ticker + " trend : " + trend + " cum_momemtum : " + str(norm_vol_sum))


momentum_trend(ticker,plt_df,'2020-04-30')