import requests
import pandas as pd
from datetime import date, timedelta
import finplot as fplt
import json
import time
import numpy as np
import sched, time, threading
from fetch_api_data import api_login, fetch_data

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
# print(df.iloc[len(df['Date'])-1])

prev_day_high = float(df.iloc[len(df['Date'])-1]['High'])
prev_day_low = float(df.iloc[len(df['Date'])-1]['Low'])
prev_day_open = float(df.iloc[len(df['Date'])-1]['Open'])
prev_day_close = float(df.iloc[len(df['Date'])-1]['Close'])

with open('temp.txt') as f:
	# temp = [x.strip() for x in f.readlines()]
	# temp = [json.loads(json.dumps(x.strip())) for x in f.readlines()]
	temp = json.load(f)

df1 = pd.read_json('prev_day_temp.txt')
df1 = df1.set_index('Date')
df1 = df1.resample('5min').agg({'Open':'first','Close':'last','High':'max','Low':'min','Volume':'sum'})

prev_day_high = df1['High'].max()
prev_day_low = df1['Low'].min()
prev_day_open = df1['Open'].max()
prev_day_close = df1['Close'].max()


print("prev_day_high",prev_day_high) 
print("prev_day_low",prev_day_low) 
print("prev_day_open",prev_day_open) 
print("prev_day_close",prev_day_close) 




symbol = 'BANK NIFTY'
# df = df.set_index('Date')
# ax,ax2 = fplt.create_plot(symbol, rows=2)
ax = fplt.create_plot(symbol, rows=1)

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
	# candles = df['df.index h_open h_close h_high h_low'.split()]
	fplt.candlestick_ochl(candles, ax=ax)

def plot_ema(df, ax, ema):
	fplt.plot(df.Date, df.Close.ewm(span=ema).mean(), ax=ax, legend='EMA')

def plot_sma(df, ax, sma):
	fplt.plot(df.Date, df['Close'].rolling(sma).mean(), ax=ax, legend='SMA')

def plot_fib_retracemnet(df,ax):
	df3 = df
	df3 = df3.set_index('Date')
	df3 = df3.resample('15min').agg({'Open':'first','Close':'last','High':'max','Low':'min','Volume':'sum'})
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

def plot_prev_day_levels(df,ax):
	line = fplt.add_line((df['Date'].iloc[0], prev_day_high), (df['Date'].iloc[len(df['Date'])-1], prev_day_high), color='#9900ff', interactive=True)
	line2 = fplt.add_line((df['Date'].iloc[0], prev_day_low), (df['Date'].iloc[len(df['Date'])-1], prev_day_low), color='#9900ff', interactive=True)
	line3 = fplt.add_line((df['Date'].iloc[0], prev_day_close), (df['Date'].iloc[len(df['Date'])-1], prev_day_close), color='#9900ff', interactive=True)
	line4 = fplt.add_line((df['Date'].iloc[0], prev_day_open), (df['Date'].iloc[len(df['Date'])-1], prev_day_open), color='#9900ff', interactive=True)

def generate_signals(df):
	sma26 = df['Close'].rolling(26).mean()
	lastest_price_index = len(df['Date'])-1
	print(df['Close'].iloc[lastest_price_index], sma26[lastest_price_index])
	if df['Close'].iloc[lastest_price_index] > sma26[lastest_price_index] and df['Close'].iloc[lastest_price_index] > level1:
		print("BUY CE "+ df['Close'].iloc[lastest_price_index] +" breached SMA26 @ "+ sma26[lastest_price_index] +" and Fib_level @ "+ level1)

api_session = requests.Session()
s = sched.scheduler(time.time, time.sleep)

def repeating_sub_proc(session):
	while True:
		print('Executing sub routines ', time.strftime('%H:%M'))
		fetch_data(session,'BANK NIFTY',None)
		plot_everything()
		time.sleep(60)


def main_procedure():
	session_5p = api_login(api_session)

	fetch_data(session_5p,'BANK NIFTY','20201111')
	fetch_data(session_5p,'BANK NIFTY',None)
	current_hour = int(time.strftime('%H'))
	current_hour = 12
	if current_hour > 9 and current_hour < 16:
		starttime = time.time()
		
		# s.enter(60, 1, plot_everything	, (s,))
		# s.run()
		# while True:
		# 	print('Executing sub routines ', time.strftime('%H:%M'))
		# 	fetch_data(session_5p,'BANK NIFTY',None)
		# 	plot_everything()
		# 	time.sleep(60.0 - ((time.time() - starttime) % 60.0))
		thread = threading.Thread(target=repeating_sub_proc, args=(session_5p,), daemon=True)
		thread.start()
	else:
		plot_everything()


def plot_everything():
	# if sc == None:
	df = pd.read_json('temp.txt')
	#if necessary convert to datetime
	df['Date'] = pd.to_datetime(df['Date'], format="%Y/%m/%d %H:%M:%S").dt.tz_localize('Asia/Kolkata')
	print(df.head())
	print(df.dtypes)
	df['ema'] = df.Close.ewm(span=20).mean()

	df = df.set_index('Date')
	df = df.resample('5min').agg({'Open':'first','Close':'last','High':'max','Low':'min','Volume':'sum'})
	# df['Date'] = df.index
	df.reset_index(level=0, inplace=True)
	plot_heikin_ashi(df, ax)
	# plot_ema(df, ax, 20)
	plot_sma(df,ax,26)
	plot_fib_retracemnet(df,ax)
	plot_prev_day_levels(df,ax)
	# generate_signals(df)
	# fplt.add_line([df['Open'].iloc[0],prev_day_high], [df['Open'].iloc[len(df['Open'])-3], prev_day_high],ax=ax)

	# line = fplt.add_line((df['Date'].iloc[0], prev_day_high), (df['Date'].iloc[len(df['Date'])-1], prev_day_high), color='#9900ff', interactive=True)
	# line2 = fplt.add_line((df['Date'].iloc[0], prev_day_low), (df['Date'].iloc[len(df['Date'])-1], prev_day_low), color='#9900ff', interactive=True)
	# line3 = fplt.add_line((df['Date'].iloc[0], prev_day_close), (df['Date'].iloc[len(df['Date'])-1], prev_day_close), color='#9900ff', interactive=True)
	# line4 = fplt.add_line((df['Date'].iloc[0], prev_day_open), (df['Date'].iloc[len(df['Date'])-1], prev_day_open), color='#9900ff', interactive=True)
	# fplt.plot(df.Date,prev_day_high,ax=ax)

	fplt.autoviewrestore()

	fplt.show()
	# else:
		# s.enter(60, 1, plot_everything, (sc,))


# df = pd.read_json('temp.txt')
# #if necessary convert to datetime
# df['Date'] = pd.to_datetime(df['Date'], format="%Y/%m/%d %H:%M:%S").dt.tz_localize('Asia/Kolkata')
# print(df.head())
# print(df.dtypes)
# df['ema'] = df.Close.ewm(span=20).mean()

# df = df.set_index('Date')
# df = df.resample('5min').agg({'Open':'first','Close':'last','High':'max','Low':'min','Volume':'sum'})
# # df['Date'] = df.index
# df.reset_index(level=0, inplace=True)
# plot_heikin_ashi(df, ax)
# # plot_ema(df, ax, 20)
# plot_sma(df,ax,26)
# plot_fib_retracemnet(df,ax)
# plot_prev_day_levels(df,ax)
# generate_signals(df)
# # fplt.add_line([df['Open'].iloc[0],prev_day_high], [df['Open'].iloc[len(df['Open'])-3], prev_day_high],ax=ax)

# # line = fplt.add_line((df['Date'].iloc[0], prev_day_high), (df['Date'].iloc[len(df['Date'])-1], prev_day_high), color='#9900ff', interactive=True)
# # line2 = fplt.add_line((df['Date'].iloc[0], prev_day_low), (df['Date'].iloc[len(df['Date'])-1], prev_day_low), color='#9900ff', interactive=True)
# # line3 = fplt.add_line((df['Date'].iloc[0], prev_day_close), (df['Date'].iloc[len(df['Date'])-1], prev_day_close), color='#9900ff', interactive=True)
# # line4 = fplt.add_line((df['Date'].iloc[0], prev_day_open), (df['Date'].iloc[len(df['Date'])-1], prev_day_open), color='#9900ff', interactive=True)
# # fplt.plot(df.Date,prev_day_high,ax=ax)

# fplt.autoviewrestore()

# fplt.show()
main_procedure()