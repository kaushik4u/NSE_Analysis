from datetime import datetime, timedelta
from os import close
from plotly import graph_objs
import requests
import json
import random
import pandas as pd
import numpy as np
import pandas_ta as ta
from tapy import Indicators
import plotly.graph_objects as go
import pytz

# this is for NIFTY bank only
def fetch_yahoo_feed(interval):
    

    user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    # bankniftyurl = 'https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEBANK?region=IN&lang=en-IN&includePrePost=false&interval=5m&range=5d&corsDomain=in.finance.yahoo.com&.tsrc=finance'
    bankniftyurl = 'https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEBANK?region=IN&lang=en-IN&includePrePost=false&interval='+interval+'&range=5d&corsDomain=in.finance.yahoo.com&.tsrc=finance'
    # bankniftyurl = 'https://query1.finance.yahoo.com/v8/finance/chart/BTC-INR?region=IN&lang=en-IN&includePrePost=false&interval='+interval+'&range=5d&corsDomain=in.finance.yahoo.com&.tsrc=finance'
    
    #Pick a random user agent
    user_agent = random.choice(user_agent_list)
    #Set the headers 
    headers = {'User-Agent': user_agent}
    
    # r = requests.Session()
    # r.headers = headers
    
    # res = r.get(bankniftyurl)
    # res = requests.get(bankniftyurl)
    try:
        res = requests.get(bankniftyurl, headers=headers)
        return res.json()
    except:
        print('Retrying...')
        res = fetch_yahoo_feed(interval)
        return res
        # res = requests.get(bankniftyurl, headers=headers)
    # res = requests.get(bankniftyurl, headers=headers)
    # print(res.json())
    

def process_yahoo_feed(interval):
    bn_data = fetch_yahoo_feed(interval)
    with open('bnyahoo.json',mode='w',encoding='utf-8') as f:
        json.dump(bn_data, f)
    # print(bn_data['chart']['result'][0]['timestamp'])
    # print(bn_data['chart']['result'][0]['indicators']['quote'][0]['open'])

    bn_dict = {
        'Datetime':bn_data['chart']['result'][0]['timestamp'],
        'Open':bn_data['chart']['result'][0]['indicators']['quote'][0]['open'],
        'Close':bn_data['chart']['result'][0]['indicators']['quote'][0]['close'],
        'High':bn_data['chart']['result'][0]['indicators']['quote'][0]['high'],
        'Low':bn_data['chart']['result'][0]['indicators']['quote'][0]['low'],
    }

    df = pd.DataFrame(bn_dict)
    df['Datetime'] = pd.to_datetime(df['Datetime'], unit='s', utc=True)
    df['Datetime'] = df['Datetime'].dt.tz_convert('Asia/Kolkata')
    # df['Datetime'] = pd.to_datetime(df['Datetime'], unit='ms', tz=df['tz'])
    # df = df.dt.tz_localize('Asia/Kolkata')
    df['Open'] = df['Open'].round(decimals=2)
    df['Close'] = df['Close'].round(decimals=2)
    df['High'] = df['High'].round(decimals=2)
    df['Low'] = df['Low'].round(decimals=2)
    df['sma26'] = df['Close'].rolling(26).mean()
    # print(df.tail())
    # print(datetime.now().strftime('%d'))
    # dt_match_str = datetime.now().strftime('%Y-%m-%d') +' 9:30:00'
    # print(dt_match_str)
    # # dt_match_str = '2020-12-24 9:30:00'
    # print(df[df['Datetime'] == dt_match_str].index)
    # idx = df[df['Datetime'] == dt_match_str].index.values[0]
    # print(idx)
    # print(df.iloc[idx]['Open'])
    # print(df.index.get_loc([df['Datetime'] == dt_match_str]))
    return df

def calc_heikin_ashi(df_data):
    # df['h_close'] = (df.Open+df.Close+df.High+df.Low) * 0.25
    df_data['h_close'] = (df_data['Open'] + df_data['Close'] + df_data['High'] + df_data['Low']) * 0.25
    # df_data['h_open'] = (df_data.Open.shift()+df_data.Close.shift()) * 0.5
    df_data['h_open'] = (df_data['Open'].shift()+df_data['Close'].shift()) * 0.5
    df_data['h_high'] = df_data[['High','h_open','h_close']].max(axis=1)
    df_data['h_low'] = df_data[['Low','h_open','h_close']].min(axis=1)

    return df_data

def calc_fib_levels(df_data, dt):
    df_data = df_data.set_index('Datetime')
    df_data = df_data['Close'].resample('15T').ohlc()
    # print(df_data)
    df_data = df_data.reset_index()
    # print(df_data)
    idx = df_data[df_data['Datetime'] == dt].index.values[0]
    # idx = df_data[df_data.index == dt].index.values[0]
    # if df_data[df_data['Datetime'] == dt]['Open'] > df_data[df_data['Datetime'] == dt]['Close']:
    #     price_max = df_data[df_data['Datetime'] == dt]['Open']
    #     price_min = df_data[df_data['Datetime'] == dt]['Close']
    # else:
    #     price_max = df_data[df_data['Datetime'] == dt]['Close']
    #     price_min = df_data[df_data['Datetime'] == dt]['Open']

    if df_data.iloc[idx]['open'] > df_data.iloc[idx]['close']:
        price_max = df_data.iloc[idx]['open']
        price_min = df_data.iloc[idx]['close']
    else:
        price_max = df_data.iloc[idx]['close']
        price_min = df_data.iloc[idx]['open']
    
    price_diff = price_max - price_min
    
    level0 = price_max + 0 * price_diff
    level382 = price_max + 0.382 * price_diff
    level618 = price_max + 0.618 * price_diff
    level1 = price_max + 1 * price_diff
    leveln382 = price_max + (-0.382) * price_diff
    leveln618 = price_max + (-0.618) * price_diff
    level1618 = price_max + 1.618 * price_diff
    level1382 = price_max + 1.382 * price_diff
    leveln1382 = price_max + (-1.382) * price_diff
    leveln1618 = price_max + (-1.618) * price_diff


    # print('fib_level1: [    0%] ',level0)
    # print('fib_level2: [ 38.2%] ',level382)
    # print('fib_level3: [ 61.8%] ',level618)
    # print('fib_level4: [  100%] ',level1)
    # print('fib_level5: [-38.2%] ',leveln382)
    # print('fib_level6: [-61.8%] ',leveln618)
    # print('fib_level5: [-138.2%] ',leveln1382)
    # print('fib_level6: [-161.8%] ',leveln1618)
    # print('fib_level7: [161.8%] ',level1618)
    # print('fib_level8: [138.2%] ',level1382)

    fib_levels = [
        leveln1618,
        leveln1382,
        leveln618,
        leveln382,
        level0,
        level382,
        level618,
        level1,
        level1382,
        level1618
    ]
    fib_levels = {
        '-161.8%' : leveln1618,
        '-138.2%' : leveln1382,
        '-61.8%' : leveln618,
        '-38.2%' : leveln382,
        '0%': level0,
        '38.2%' : level382,
        '61.8%' : level618,
        '100%' : level1,
        '138.2%' : level1382,
        '161.8%' : level1618
    }
    return fib_levels
    
def prev_weekday(adate):
    _offsets = (3, 1, 1, 1, 1, 1, 2)
    return adate - timedelta(days=_offsets[adate.weekday()])

def find_pd_extremes(df,dt):
    pday = prev_weekday(datetime.strptime(dt,'%Y-%m-%d'))
    pday = pytz.timezone('Asia/Kolkata').localize(pday)
    curr_day = pytz.timezone('Asia/Kolkata').localize(datetime.strptime(dt,'%Y-%m-%d'))
    # print(pday)
    df = df[(df['Datetime'] >= pday) & (df['Datetime'] < curr_day)]
    # print(df)
    pdh = df['High'].max()
    pdl = df['Low'].min()
    pdch = df['Close'].max()
    pdol = df['Open'].min()
    return pdol, pdh, pdl, pdch

   

def plotly_graph(df_data):    
    # df_data = calc_heikin_ashi(df_data)
    # df_data['SuperTrend'] = ta.supertrend(high=df_data['High'],low=df_data['Low'], open=df_data['Open'], close=df_data['Close'], period=7, multiplier=3)['SUPERT_7_3.0']
    df_data['SuperTrend'] = ta.supertrend(high=df_data['High'],low=df_data['Low'], open=df_data['Open'], close=df_data['Close'], period=7, multiplier=3).iloc[:,[0]]
    i = Indicators(df_data)
    i.alligator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_jaws='alligator_jaw', column_name_teeth='alligator_teeth', column_name_lips='alligator_lips')
    df_data = i.df
    dt_match_str = datetime.now().strftime('%Y-%m-%d') +' 09:15:00'
    print(dt_match_str)
    dt_match_str = '2021-06-11 09:15:00'
    # df_15min = process_yahoo_feed('15m')
    fib_retracement = calc_fib_levels(df_data,dt_match_str)
    curr_date = dt_match_str.split(' ')[0]
    pd_extermes = {}
    pd_extermes['ol'], pd_extermes['hh'], pd_extermes['ll'], pd_extermes['ch'] = find_pd_extremes(df_data,curr_date)
    pdol, pdh, pdl, pdch = find_pd_extremes(df_data,curr_date)
    print('Previous day Lowest Open: {} Highest High: {} Lowest Low: {} and Highest Close: {}'.format(pdol, pdh, pdl, pdch))
    # locks df for current date for easy zoomed graph
    df_data = df_data[df_data['Datetime'] >= curr_date]
    # df_data = df_data[(df_data['Datetime'] >= dt_match_str) & (df_data['Datetime'] <= '2021-04-13 15:30:00')]
    # print(df_data)
    graph_list = [
        go.Candlestick(
        # go.Ohlc(
            x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
            # open = df_data['Open'],
            # high = df_data['High'],
            # low = df_data['Low'],
            # close = df_data['Close'],
            open = df_data['Open'],
            high = df_data['High'],
            low = df_data['Low'],
            close = df_data['Close'],
            increasing_line_color = '#26a69a',
            increasing_fillcolor = '#26a69a',
            decreasing_line_color = '#f44336',
            decreasing_fillcolor = '#f44336'
            ),
        go.Scatter(
            x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
            y = df_data['sma26'],
            line = dict(color = 'blue', width = 1),
            name = 'SMA 26'
            ),
        go.Scatter(
            x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
            y = df_data['SuperTrend'],
            line = dict(color = 'Orange', width = 2),
            name = 'SuperTrend'
            ),
        go.Scatter(
            x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
            y = df_data['alligator_jaw'],
            line = dict(color = 'pink', width = 2),
            name = 'JAW'
            )
            
    ]

    # for i in range(len(fib_retracement)):
    #     graph_list.append(
    #         go.Scatter(
    #         x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
    #         y = [fib_retracement[i]] * len(df_data['Datetime']),
    #         line = dict(color = 'purple', width = 1),
    #         name = 'fib retracement'
    #         )
    #     )
    for key in fib_retracement.keys():
        graph_list.append(
            go.Scatter(
            x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
            y = [fib_retracement[key]] * len(df_data['Datetime']),
            line = dict(color = 'purple', width = 1),
            name = key
            )
        )
    for key in pd_extermes.keys():
        graph_list.append(
            go.Scatter(
            x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
            y = [pd_extermes[key]] * len(df_data['Datetime']),
            line = dict(color = 'red', width = 1),
            name = key
            )
        )
    
    # fig = go.Figure(data=[
    #     go.Candlestick(
    #         x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
    #         # open = df_data['Open'],
    #         # high = df_data['High'],
    #         # low = df_data['Low'],
    #         # close = df_data['Close'],
    #         open = df_data['h_open'],
    #         high = df_data['h_high'],
    #         low = df_data['h_low'],
    #         close = df_data['h_close'],
    #         ),
    #     go.Scatter(
    #         x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
    #         y = df_data['sma26'],
    #         line = dict(color = 'blue', width = 1),
    #         name = 'SMA 26'
    #         ),
    #     go.Scatter(
    #         x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
    #         y = [fib_retracement[0]] * len(df_data['Datetime']),
    #         line = dict(color = 'green', width = 1),
    #         )
    #         ],
    #     layout = dict(
    #         paper_bgcolor = '#131516',
    #         plot_bgcolor = '#131516',
            
    #     ))
    # fig = go.Figure(data=graph_list, layout=dict(paper_bgcolor = '#121212',plot_bgcolor = '#121212'))
    fig = go.Figure(data=graph_list)
    fig.update_layout(dict(paper_bgcolor = '#121212', plot_bgcolor = '#121212'))
    fig.update_xaxes(showline=False, linewidth=0, linecolor='#121212', gridcolor='#121212')
    fig.update_yaxes(showline=False, linewidth=0, linecolor='#d8d4cf', gridcolor='#d8d4cf')
    fig.update_xaxes(showgrid=False, linewidth=0, linecolor='#121212', gridcolor='#121212')
    fig.update_yaxes(showgrid=False, linewidth=0, linecolor='#d8d4cf', gridcolor='#d8d4cf')
    
    def zoom(layout, xrange):
        in_view = df_data.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
        fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]
    
    fig.layout.on_change(zoom, 'xaxis.range')
    fig.update_layout(xaxis_rangeslider_visible=False)
    # fig.update_layout(grid=False)
    # fig.update_layout(xaxis=dict(tick=30))
    # fig.show()
    return fig

def generate_fake_ticks():
    # [{"name": "tm", "tvalue": "18/12/2020 14:28:28"}, {"c": "30847.05", "cng": "-163.75", "e": "nse_cm", "ltp": "30683.30", "ltt": "NA", "name": "sf", "nc": "-00.53", "tk": "26009"}]
    tvalue = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    ltp = random.randrange(29500,30500)

    return [{"tvalue":tvalue},{"ltp":str(ltp)}]

# plotly_graph(df)
# fig = plotly_graph(process_yahoo_feed())
# fig.show()

if __name__ == "__main__":
    # plotly_graph
    fig = plotly_graph(process_yahoo_feed('15m'))
    fig.show()
    print("All done!")
