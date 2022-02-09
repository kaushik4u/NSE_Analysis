from datetime import datetime, timedelta
from plotly import graph_objs
import requests
import json
import random
import pandas as pd
import plotly.graph_objects as go
import pytz

# this is for NIFTY bank only
def fetch_yahoo_feed(interval):
    # bankniftyurl = 'https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEBANK?region=IN&lang=en-IN&includePrePost=false&interval=5m&range=5d&corsDomain=in.finance.yahoo.com&.tsrc=finance'
    bankniftyurl = 'https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEBANK?region=IN&lang=en-IN&includePrePost=false&interval='+interval+'&range=5d&corsDomain=in.finance.yahoo.com&.tsrc=finance'
    # bankniftyurl = 'https://query1.finance.yahoo.com/v8/finance/chart/BTC-INR?region=IN&lang=en-IN&includePrePost=false&interval='+interval+'&range=5d&corsDomain=in.finance.yahoo.com&.tsrc=finance'
    res = requests.get(bankniftyurl)
    # print(res.json())
    return res.json()

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

def identify_trades(df,flvl,dt):
        
    level1382 = flvl['138.2%']
    level1618 = flvl['161.8%']
    leveln382 = flvl['-38.2%']
    leveln618 = flvl['-61.8%']
    leveln1382 = flvl['-138.2%']
    leveln1618 = flvl['-161.8%']

    df_15 = process_yahoo_feed('15m')
    df_15 = df_15.reset_index()
    idx = df_15[df_15['Datetime'] == dt].index.values[0]
    curr_dt = dt.split(' ')[0]

    pdol, pdh, pdl, pdch = find_pd_extremes(df,curr_dt)
    df = df[df['Datetime'] >= curr_dt]
    price_diff = df_15.iloc[idx]['Close'] - df_15.iloc[idx]['Open']
    
    up_points = {}
    down_points = []
    df['up_tick'] = ""
    df['down_tick'] = ""
    print("Opening Price diff [close - open]: " + str(price_diff))
    
    df['up_tick'] = df[(df['Close'] > level1382) | (df['Close'] >  level1618) | (df['Close'] > pdch) | (df['Close'] >  pdh) & (df['Close'] > df['sma26'])]['Close']
    # df['up_tick'] = df[(df['Close'] > pdch) | (df['Close'] >  pdh)]['Close']
    df['down_tick'] = df[(df['Close'] < leveln382) | (df['Close'] <  leveln618) | (df['Close'] < pdol) | (df['Close'] <  pdl) & (df['Close'] < df['sma26'])]['Close']
    entry_point = 0
    exit_point = 0
    on_going_trade = False
    # if abs(price_diff) > 50:
    #     for i in range(len(df)):
    #         if df.iloc[i]['Close'] > df.iloc[i]['sma26']:
    #             if df.iloc[i]['Close'] > level1382 or df.iloc[i]['Close'] > level1618 and on_going_trade == False:
    #                 entry_point = df.iloc[i]['Close']
    #                 # print(df.iloc[i])
    #         if df.iloc[i]['Close'] > entry_point + 100 and on_going_trade:
    #             exit_point = df.iloc[i]['Close']
    #             print('PnL: {} trade side: up entry: {} exit: {}'.format(exit_point - entry_point, entry_point, exit_point))
    #             entry_point = 0
    #             on_going_trade = False
    #         if df.iloc[i]['Close'] < entry_point - 50 and on_going_trade:
    #             exit_point = df.iloc[i]['Close']
    #             print('SL: {} trade side: up entry: {} exit: {}'.format(exit_point - entry_point, entry_point, exit_point))
    #             entry_point = 0
    #             on_going_trade = False
    # print(df[['Close','down_tick','up_tick']])

    for i in range(len(df)):
        if df.iloc[i]['up_tick'] > 0 and entry_point == 0:
            entry_point = df.iloc[i]['up_tick']
        # profit booked CE side
        if entry_point > 0 and df.iloc[i]['Close'] > entry_point + 100:
            exit_point = df.iloc[i]['Close']
            pnl = round(exit_point - entry_point, 2)
            print('[{}] PnL: {} trade side: CE entry: {} exit: {}'.format(df.iloc[i]['Datetime'], pnl, entry_point, exit_point))
            entry_point = 0
        # SL hit CE side
        if entry_point > 0 and df.iloc[i]['Close'] < entry_point - 50:
            exit_point = df.iloc[i]['Close']
            pnl = round(exit_point - entry_point, 2)
            print('[{}] SL: {} trade side: CE entry: {} exit: {}'.format(df.iloc[i]['Datetime'], pnl, entry_point, exit_point))
            entry_point = 0
        
        if df.iloc[i]['down_tick'] > 0 and entry_point == 0:
            entry_point = df.iloc[i]['down_tick']
        # profit booked PE side
        if entry_point > 0 and df.iloc[i]['Close'] < entry_point - 100:
            exit_point = df.iloc[i]['Close']
            pnl = round(entry_point - exit_point, 2)
            print('[{}] PnL: {} trade side: PE entry: {} exit: {}'.format(df.iloc[i]['Datetime'], pnl, entry_point, exit_point))
            entry_point = 0
        # SL hit CE side
        if entry_point > 0 and df.iloc[i]['Close'] > entry_point + 50:
            exit_point = df.iloc[i]['Close']
            pnl = round(exit_point - entry_point, 2)
            print('[{}] SL: {} trade side: PE entry: {} exit: {}'.format(df.iloc[i]['Datetime'], pnl, entry_point, exit_point))
            entry_point = 0
            
    

    # df['down_tick'] = df[(df['Close'] < pdol) | (df['Close'] <  pdl)]['Close']
    # if (abs(price_diff) > 50):
    #     for i in range(len(df)):
    #         if df.iloc[i]['Close'] > df.iloc[i]['sma26']:
    #             if df.iloc[i]['Close'] > level1382 or df.iloc[i]['Close'] > level1618:
    #                 # up_points.append(df.iloc[i])
    #                 # up_points[df.iloc[i]['Datetime'].strftime("%d/%m %H:%M")] = df.iloc[i]['Close']
    #                 df.iloc[i]['up_tick'] = df.iloc[i]['Close']
    #         else:
    #             if df.iloc[i]['Close'] < leveln382 or df.iloc[i]['Close'] < leveln618:
    #                 down_points.append(df.iloc[i])
    
    #     if df.iloc[i]['Close'] > pdch or df.iloc[i]['Close'] > pdh:
    #         up_points.append(df.iloc[i])
    #     if df.iloc[i]['Close'] < pdol or df.iloc[i]['Close'] < pdl:
    #         down_points.append(df.iloc[i])

    # print("Up points: ", up_points)
    # print("Down points: ", down_points)

    # return up_points, down_points
    return df


               



def plotly_graph(df_data):    
    # df_data = calc_heikin_ashi(df_data)
    dt_match_str = datetime.now().strftime('%Y-%m-%d') +' 09:15:00'
    print(dt_match_str)
    # dt_match_str = '2021-04-13 09:15:00'
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
    # up_ticks, downticks = identify_trades(df_data,fib_retracement,dt_match_str)
    tick_df =  identify_trades(df_data,fib_retracement,dt_match_str)
    # print(up_df['up_tick'])
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
            x = tick_df['Datetime'].dt.strftime("%d/%m %H:%M"),
            y = tick_df['up_tick'],
            # line = dict(color = 'blue', width = 1),
            marker_symbol='triangle-up',
            marker_line_color="white",
            marker_line_width=1,
            mode='markers',
            marker_color="#FFDA00",
            marker_size=12,
            name = 'Up Trends'
            ),
        go.Scatter(
            x = tick_df['Datetime'].dt.strftime("%d/%m %H:%M"),
            y = tick_df['down_tick'],
            # line = dict(color = 'blue', width = 1),
            marker_symbol='triangle-down',
            marker_line_color="white",
            marker_line_width=1,
            mode='markers',
            marker_color="#0025FF",
            marker_size=12,
            name = 'Down Trends'
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
    # for key in up_ticks.keys():
    #     graph_list.append(
    #         go.Scatter(
    #         # x = df_data['Datetime'].dt.strftime("%d/%m %H:%M"),
    #         # y = [pd_extermes[key]] * len(df_data['Datetime']),
    #         x = key,
    #         y = up_ticks[key],
    #         # line = dict(color = 'red', width = 1),
    #         mode='markers',
    #         name = key
    #         )
    #     )
    
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
    fig.update_xaxes(showline=True, linewidth=.1, linecolor='#121212', gridcolor='#121212')
    fig.update_yaxes(showline=True, linewidth=.1, linecolor='#d8d4cf', gridcolor='#d8d4cf')
    
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
    fig = plotly_graph(process_yahoo_feed('5m'))
    fig.show()
    print("All done!")
