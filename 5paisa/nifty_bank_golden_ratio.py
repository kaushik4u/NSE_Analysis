import requests
import pandas as pd
from datetime import date, timedelta
import finplot as fplt
import json
import time
import numpy as np

def prev_weekday(adate):
    adate -= timedelta(days=1)
    while adate.weekday() > 4: # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate


#get prev day Low and Highs
today = date.today()
prev_day = prev_weekday(today).strftime("%d-%m-%Y")
start_date = date(today.year,today.month,1).strftime("%d-%m-%Y")
NSE_url = 'https://www1.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType=NIFTY%20BANK&fromDate=01-10-2020&toDate=19-10-2020'
NSE_url = "https://www1.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType=NIFTY%20BANK&fromDate="+ start_date +"&toDate="+ prev_day

print("Fetching... ",NSE_url)

nse_headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9",
"Connection": "keep-alive",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}
res = requests.get(NSE_url, headers = nse_headers)
print(res)
# print(res.text)

df = pd.read_html(res.text)
df = df[0]
df.columns = ['Date','Open','High','Low','Close','Shares Traded','Turnover ( Cr)']
df = df[:-1]
print(df.iloc[len(df['Date'])-1])

prev_day_high = float(df.iloc[len(df['Date'])-1]['High'])
prev_day_low = float(df.iloc[len(df['Date'])-1]['Low'])
prev_day_open = float(df.iloc[len(df['Date'])-1]['Open'])
prev_day_close = float(df.iloc[len(df['Date'])-1]['Close'])

with open('temp.txt') as f:
    # temp = [x.strip() for x in f.readlines()]
    # temp = [json.loads(json.dumps(x.strip())) for x in f.readlines()]
    temp = json.load(f)

df = pd.read_json('temp.txt')
#if necessary convert to datetime
df['Date'] = pd.to_datetime(df['Date'], format="%Y/%m/%d %H:%M:%S").dt.tz_localize('Asia/Kolkata')
print(df.head())
print(df.dtypes)
df['ema'] = df.Close.ewm(span=20).mean()

symbol = 'BANK NIFTY'
# df = df.set_index('Date')
ax,ax2 = fplt.create_plot(symbol, rows=2)

# change coloring templates for next plots
fplt.candle_bull_color = '#09FC04'
fplt.candle_bear_color = '#FC0426'
fplt.candle_bear_body_color = '#FC0426'
fplt.candle_bull_body_color = '#09FC04'
fplt.volume_bull_color = '#09FC04'
fplt.volume_bear_color = '#FC0426'
fplt.volume_bear_body_color = '#FC0426'
fplt.volume_bull_body_color = '#09FC04'

fplt.background = fplt.odd_plot_background = '#121212'

def plot_heikin_ashi(df, ax):
    df['h_close'] = (df.Open+df.Close+df.High+df.Low) * 0.25
    df['h_open'] = (df.Open.shift()+df.Close.shift()) * 0.5
    df['h_high'] = df[['High','h_open','h_close']].max(axis=1)
    df['h_low'] = df[['Low','h_open','h_close']].min(axis=1)
    candles = df['Date h_open h_close h_high h_low'.split()]
    fplt.candlestick_ochl(candles, ax=ax)

def plot_ema(df, ax, ema):
    fplt.plot(df.Date, df.Close.ewm(span=ema).mean(), ax=ax, legend='EMA')

plot_heikin_ashi(df, ax)
plot_ema(df, ax, 20)
# fplt.add_line([df['Open'].iloc[0],prev_day_high], [df['Open'].iloc[len(df['Open'])-1], prev_day_high],ax=ax)
fplt.plot(df.Date,prev_day_high,ax=ax)

fplt.autoviewrestore()

fplt.show()