import requests
import pandas as pd
from datetime import date, timedelta
import finplot as fplt
import json
import time
import numpy as np
from dateutil.tz import gettz


def plot_strategy(df_data):
    df = df_data
    symbol = 'BANK NIFTY'
    ax = fplt.create_plot(symbol, rows=1)
    # fplt.display_timezone = gettz('Asia/Kolkata')
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
        # df['h_close'] = (df.Open+df.Close+df.High+df.Low) * 0.25
        df['h_close'] = (df['Open']+df['Close']+df['High']+df['Low']) * 0.25
        # df['h_open'] = (df.Open.shift()+df.Close.shift()) * 0.5
        df['h_open'] = (df['Open'].shift()+df['Close'].shift()) * 0.5
        df['h_high'] = df[['High','h_open','h_close']].max(axis=1)
        df['h_low'] = df[['Low','h_open','h_close']].min(axis=1)
        candles = df['Date h_open h_close h_high h_low'.split()]
        # candles = df['df.index h_open h_close h_high h_low'.split()]
        fplt.candlestick_ochl(candles, ax=ax)

    def plot_ema(df, ax, ema):
	    # fplt.plot(df.Date, df.Close.ewm(span=ema).mean(), ax=ax, legend='EMA')
        fplt.plot(df['Date'], df['Close'].ewm(span=ema).mean(), ax=ax, legend='EMA')

    def plot_sma(df, ax, sma):
	    # fplt.plot(df.Date, df['Close'].rolling(sma).mean(), ax=ax, legend='SMA')
        fplt.plot(df['Date'], df['Close'].rolling(sma).mean(), ax=ax, legend='SMA')

    def plot_fib_retracemnet(df,ax):
        df3 = df
        df3 = df3.set_index('Date')
        ohlc_dict = {'Open':'first','Close':'last','High':'max','Low':'min'}
        df3 = df3.resample('15min').agg(ohlc_dict)
        print(df3.iloc[4])
        if df3.iloc[4]['Open'] > df3.iloc[4]['Close']:
            price_max = df3.iloc[4]['Open']
            price_min = df3.iloc[4]['Close']
        else:
            price_max = df3.iloc[4]['Close']
            price_min = df3.iloc[4]['Open']
        
        price_diff = price_max - price_min
        # level1 = price_max - 0 * price_diff
        # level2 = price_max - 0.382 * price_diff
        # level3 = price_max - 0.618 * price_diff
        # level4 = price_max - 1 * price_diff
        # level5 = price_max - (-0.382) * price_diff
        # level6 = price_max - (-0.618) * price_diff
        # level7 = price_max - 1.618 * price_diff
        # level8 = price_max - 1.382 * price_diff
        level1 = price_max + 0 * price_diff
        level2 = price_max + 0.382 * price_diff
        level3 = price_max + 0.618 * price_diff
        level4 = price_max + 1 * price_diff
        level5 = price_max + (-0.382) * price_diff
        level6 = price_max + (-0.618) * price_diff
        level7 = price_max + 1.618 * price_diff
        level8 = price_max + 1.382 * price_diff


        print('fib_level1: ',level1)
        print('fib_level2: ',level2)
        print('fib_level3: ',level3)
        print('fib_level4: ',level4)
        print('fib_level5: ',level5)
        print('fib_level6: ',level6)
        print('fib_level7: ',level7)
        print('fib_level8: ',level8)
        level1_line = fplt.add_line((df['Date'].iloc[0], level1), (df['Date'].iloc[len(df['Date'])-1], level1), color='#9900ff', interactive=True)
        level2_line = fplt.add_line((df['Date'].iloc[0], level2), (df['Date'].iloc[len(df['Date'])-1], level2), color='#7fc781', interactive=True)
        level3_line = fplt.add_line((df['Date'].iloc[0], level3), (df['Date'].iloc[len(df['Date'])-1], level3), color='#029686', interactive=True)
        level4_line = fplt.add_line((df['Date'].iloc[0], level4), (df['Date'].iloc[len(df['Date'])-1], level4), color='#787b83', interactive=True)
        level5_line = fplt.add_line((df['Date'].iloc[0], level5), (df['Date'].iloc[len(df['Date'])-1], level5), color='#f04235', interactive=True)
        level6_line = fplt.add_line((df['Date'].iloc[0], level6), (df['Date'].iloc[len(df['Date'])-1], level6), color='#ea1e63', interactive=True)
        level7_line = fplt.add_line((df['Date'].iloc[0], level7), (df['Date'].iloc[len(df['Date'])-1], level7), color='#1f97f4', interactive=True)
        level8_line = fplt.add_line((df['Date'].iloc[0], level8), (df['Date'].iloc[len(df['Date'])-1], level8), color='#9c28b1', interactive=True)
        level1_line_text = fplt.add_text((df['Date'].iloc[int((len(df['Date'])-1)/2)], level1), "0%", color='#bb7700')
        level2_line_text = fplt.add_text((df['Date'].iloc[int((len(df['Date'])-1)/2)], level2), "38.2%", color='#bb7700')
        level3_line_text = fplt.add_text((df['Date'].iloc[int((len(df['Date'])-1)/2)], level3), "61.8%", color='#bb7700')
        level4_line_text = fplt.add_text((df['Date'].iloc[int((len(df['Date'])-1)/2)], level4), "100%", color='#bb7700')
        level5_line_text = fplt.add_text((df['Date'].iloc[int((len(df['Date'])-1)/2)], level5), "-38.2%", color='#bb7700')
        level6_line_text = fplt.add_text((df['Date'].iloc[int((len(df['Date'])-1)/2)], level6), "-61.8%", color='#bb7700')
        level7_line_text = fplt.add_text((df['Date'].iloc[int((len(df['Date'])-1)/2)], level7), "161.8%", color='#bb7700')
        level8_line_text = fplt.add_text((df['Date'].iloc[int((len(df['Date'])-1)/2)], level8), "138.2%", color='#bb7700')

    # df = df.set_index('Date')
    # ohlc_dict = {'Open':'first','Close':'last','High':'max','Low':'min','Volume':'sum'}
    def generate_signals(df):
        l = len(df['Date'])
        if df[l-1]['Close'] > level1:
            print(df[l-1] + 'buy PE next level')
        elif df[l-1]['Close'] > level2:
            print(df[l-1] + 'buy PE next level')



    ohlc_dict = {'Open':'first','Close':'last','High':'max','Low':'min'}
    df = df.resample('5min').agg(ohlc_dict)
    # df['Date'] = df.index
    df.reset_index(level=0, inplace=True)
    plot_heikin_ashi(df, ax)
    # plot_ema(df, ax, 20)
    plot_sma(df,ax,26)
    plot_fib_retracemnet(df,ax)
    # plot_prev_day_levels(df,ax

    fplt.autoviewrestore()

    fplt.show()