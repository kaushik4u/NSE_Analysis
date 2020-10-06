import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import json
import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.finance import candlestick_ohlc
import mplfinance as mpf
import matplotlib.dates as mdates
import finplot as fplt
import datetime
import numpy as np

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# def animate(i):
#     pullData = open("sampleText.txt","r").read()
#     dataArray = pullData.split('\n')
#     xar = []
#     yar = []
#     for eachLine in dataArray:
#         if len(eachLine)>1:
#             x,y = eachLine.split(',')
#             xar.append(int(x))
#             yar.append(int(y))
#     ax1.clear()
#     ax1.plot(xar,yar)
# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.show()

with open('temp.txt') as f:
    # temp = [x.strip() for x in f.readlines()]
    # temp = [json.loads(json.dumps(x.strip())) for x in f.readlines()]
    temp = json.load(f)

# print(temp[0]['Open'])

df = pd.read_json('temp.txt')

#if necessary convert to datetime
df['Date'] = pd.to_datetime(df['Date'], format="%Y/%m/%d %H:%M:%S").dt.tz_localize('Asia/Kolkata')
# df['Date'] = pd.to_datetime(df['Date']).astype('int64')
# df['Date'] = datetime.datetime.fromtimestamp(df['Date'])

# df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
# df["date"] = df["date"].apply(mdates.date2num)

# f1 = plt.subplot2grid((6, 4), (1, 0), rowspan=6, colspan=4, axisbg='#07000d')
# candlestick_ohlc(f1, df.values, width=.6, colorup='#53c156', colordown='#ff1717')
# f1.xaxis_date()
# f1.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))

# plt.xticks(rotation=45)
# plt.ylabel('Stock Price')
# plt.xlabel('Date Hours:Minutes')
# plt.show()

print(df.head())
print(df.dtypes)

df['ema'] = df.Close.ewm(span=20).mean()
print(df)

symbol = 'TATAMOTORS'
# df = df.set_index('Date')
ax,ax2 = fplt.create_plot(symbol, rows=2)


# change to b/w coloring templates for next plots
fplt.candle_bull_color = '#09FC04'
fplt.candle_bear_color = '#FC0426'
fplt.candle_bear_body_color = '#FC0426'
fplt.candle_bull_body_color = '#09FC04'
fplt.volume_bull_color = '#09FC04'
fplt.volume_bear_color = '#FC0426'
fplt.volume_bear_body_color = '#FC0426'
fplt.volume_bull_body_color = '#09FC04'



Signals_file ="Signals.txt"

def plot_ema(df, ax, ema):
    fplt.plot(df.Date, df.Close.ewm(span=ema).mean(), ax=ax, legend='EMA')

def plot_volume(df, ax):
    # volume = df['time h_open h_close volume'.split()]
    volume = df['Volume']
    fplt.volume_ocv(volume, ax=ax)

def plot_heikin_ashi(df, ax):
    df['h_close'] = (df.Open+df.Close+df.High+df.Low) * 0.25
    df['h_open'] = (df.Open.shift()+df.Close.shift()) * 0.5
    df['h_high'] = df[['High','h_open','h_close']].max(axis=1)
    df['h_low'] = df[['Low','h_open','h_close']].min(axis=1)
    candles = df['Date h_open h_close h_high h_low'.split()]
    fplt.candlestick_ochl(candles, ax=ax)

def plot_heikin_ashi_volume(df, ax):
    volume = df['Date h_open h_close Volume'.split()]
    fplt.volume_ocv(volume, ax=ax)



def plot_signals(df,ax):
    df['ema'] = df.Close.ewm(span=20).mean()
    signal_up = np.where(df['Close'] > df['ema'],df['ema'],None)
    signal_down = np.where(df['Close'] > df['ema'],None,df['ema'])
    df['Signal'] = 0
    # df['position'] = 0
    for i in range(len(df['Close'])):
        if df['Close'].iloc[i] > df['ema'].iloc[i]:
            df['Signal'].iloc[i] = 1
        else:
            df['Signal'].iloc[i] = 0
    df['position'] = df['Signal'].diff()
    # df['Signal'] = compare_df
    # print(signal_up,signal_down)
    # for i in range(len(signal_up)):
    #     if signal_up[i]!=None and signal_up[i] > 0 and signal_down[i] == None and (i+1) < (len(signal_up)):
    #         signal_up[i+1] = None
    #     if signal_down[i]!=None and signal_down[i] > 0 and signal_up[i] == None and (i+1) < (len(signal_up)):
    #         signal_down[i+1] = None
    
    print(df['ema'][df['position']==-1])
    # fplt.plot(signal_up, style='^', color='#00ff00', width=2, ax=ax)
    # fplt.plot(signal_down, style='v', color='#ff0000', width=2, ax=ax)
    fplt.plot(df['ema'][df['position'] == 1],style='^', color='#00ff00', width=2, ax=ax)
    # if df['ema'] > df['Close']:
    #     df['Signal'] = df['ema']
    #     save_signal(Signals_file,df['Date'],df['Close'],'ema>closing price')
    #     fplt.plot(df['Signal'], style='△', color='green', ax=ax)


def save_signal(file,ts,price,condition):
    line = ts +' '+price+' '+condition
    with open(file,'a') as f:
        f.write(line)

# fplt.candlestick_ochl(df[['Date','Open', 'Close', 'High', 'Low']], ax=ax)
# price chart
plot_heikin_ashi(df, ax)
plot_heikin_ashi_volume(df, ax2)
plot_ema(df, ax, 20)
plot_signals(df,ax)
# plot_volume(df,ax)
# restore view (X-position and zoom) when we run this example again
fplt.autoviewrestore()

fplt.show()
# fplt.show()
# df.index.name = 'Date'
# df = df.set_index('Date')
# mpf.plot(df,type='candle',mav=(3,6,9),volume=True)

