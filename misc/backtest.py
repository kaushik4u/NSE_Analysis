import backtrader as bt
# import backtrader.indicators as btind
import pandas as pd
import datetime
import pprint
import plotly

class VolumeWeightedAveragePrice(bt.Indicator):
	plotinfo = dict(subplot=False)

	params = (('period', 5), )

	alias = ('VWAP', 'VolumeWeightedAveragePrice',)
	lines = ('VWAP',)
	plotlines = dict(VWAP=dict(alpha=0.50, linestyle='-', linewidth=2.0, color = 'blue'))



	def __init__(self):
		# Before super to ensure mixins (right-hand side in subclassing)
		# can see the assignment operation and operate on the line
		cumvol = bt.ind.SumN(self.data.volume, period = self.p.period)
		typprice = ((self.data.close + self.data.high + self.data.low)/3) * self.data.volume
		cumtypprice = bt.ind.SumN(typprice, period=self.p.period)
		self.lines[0] = cumtypprice / cumvol

		super(VolumeWeightedAveragePrice, self).__init__()

class StochRSI(bt.Indicator):
	lines = ('stochrsi',)
	params = dict(
		period=14,  # to apply to RSI
		pperiod=None,  # if passed apply to HighestN/LowestN, else "period"
	)

	def __init__(self):
		rsi = bt.ind.RSI(self.data, period=self.p.period)

		pperiod = self.p.pperiod or self.p.period
		maxrsi = bt.ind.Highest(rsi, period=pperiod)
		minrsi = bt.ind.Lowest(rsi, period=pperiod)

		self.l.stochrsi = (rsi - minrsi) / (maxrsi - minrsi)


class MyStrategy(bt.Strategy):
	# def next(self):
		# pass # Do something
	# list of parameters which are configurable for the strategy
	params = dict(
		pfast=5,  # period for the fast moving average
		pslow=13   # period for the slow moving average
	)

	# def __init__(self):
	#     sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
	#     sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
	#     self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal


	# def next(self):
	#     if not self.position:  # not in the market
	#         if self.crossover > 0:  # if fast crosses slow to the upside
	#             self.buy()  # enter long

	#     elif self.crossover < 0:  # in the market & cross to the downside
	#         self.close()  # close long position
	def log(self, txt, dt=None):
		# dt = dt or self.datas[0].datetime.date(0)
		# print('%s, %s' % (dt.isoformat(), txt))
		dt = dt or self.datas[0].datetime.datetime(0)
		print('%s, %s' % (dt.isoformat(), txt))
	
	def __init__(self):
		# vwap = self.vwap
		# self.vwap = bt.indicators.VWAP(period=5)
		# print(self.getdatabyname('df_onemin').datetime[0])
		self.vwap = VWAP(period=5)
		self.ADX= bt.indicators.DirectionalMovementIndex(self.data,period=5)
		# self.pp = PivotPoint(self.data1)
		self.pp = bt.ind.PivotPoint(self.data1)
		# self.pp.plotinfo.plotmaster = self.data1
		self.dataclose = self.datas[0].close
		self.dataopen = self.datas[0].open
		self.order = None
		self.buyprice = None
		self.sellprice = None
		self.buycomm = None
		self.size = 25 #self.broker.getcash() / self.data.close 
		# print(self.data,self.data1)
		self.rsi = bt.indicators.RSI(self.data)
		self.stoch_rsi = StochRSI(self.data, period = 5)
		self.ema = bt.indicators.ExponentialSmoothing(self.data, period=5)
		self.ATR = bt.indicators.ATR(self.data, period=5)
		# print("RSI "+str(self.rsi))

	def notify_order(self, order):
		if order.status in [order.Submitted, order.Accepted]:
			return

		if order.status in [order.Completed]:
			if order.isbuy():
				self.log(
					'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
					(order.executed.price,
					 order.executed.value,
					 order.executed.comm))

				self.buyprice = order.executed.price
				self.buycomm = order.executed.comm
			else:  # Sell
				self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
						 (order.executed.price,
						  order.executed.value,
						  order.executed.comm))
				
				self.sellprice = order.executed.price
				# self.buycomm = order.executed.comm
				# print("sellprice: "+self.sellprice)
			
			self.bar_executed = len(self)

		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log('Order Canceled/Margin/Rejected')

		# Write down: no pending order
		self.order = None

	def notify_trade(self, trade):
		if not trade.isclosed:
			return

		self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
				 (trade.pnl, trade.pnlcomm))

	def next(self):
		# buy_price = 0
		# self.log('Pivot: %.2f %.2f %.2f %.2f' %(self.pp.r1[0], self.pp.r2[0], self.pp.s1[0], self.pp.s2[0]))
		long_pos= -1
		short_pos = -1
		
		if not self.position:  # not in the market
			# if self.data.open < self.vwap and self.vwap < self.data.close and (datetime.time(9, 30, 0) < self.data.datetime.time() and self.data.datetime.time() < datetime.time(11, 30, 0)):
			# if self.data.open < self.vwap and self.vwap < self.data.close and self.rsi < 60:
			# if self.data.open < self.vwap and self.vwap < self.data.close and ((self.data.open <self.pp.r1 and self.pp.r1 <self.data.close) or (self.data.open <self.pp.r2 and self.pp.r2 <self.data.close) or (self.data.open <self.pp.s1 and self.pp.s1 <self.data.close) or (self.data.open <self.pp.s2 and self.pp.s2<self.data.close)):
			# if self.data.open < self.vwap and self.vwap < self.data.close and self.data.close > self.ema  and (datetime.time(14, 00, 0) < self.data.datetime.time() and self.data.datetime.time() < datetime.time(15, 15, 0)):
			# if self.data.open < self.vwap and self.vwap < self.data.close and self.data.close > self.ema:
			# if self.data.open < self.vwap and self.vwap < self.data.close and self.data.close > self.ema and self.stoch_rsi < 30 and  self.ADX > 30: and self.ADX > 30 and self.ADX < 40
			if self.data.open < self.vwap and self.vwap < self.data.close and self.data.close > self.ema and  self.ADX.lines.adx > self.ADX.lines.adx[-1]:
				self.log('BUY CREATE, %.2f' % self.dataclose[0])
				buy_price = self.data.close
				self.order = self.buy(size = self.size, exectype=bt.Order.StopTrail, trailamount = trail_amt)
				# self.order = self.buy(size = self.size, exectype=bt.Order.StopTrail, trailpercent =  0.002)
				# self.order = self.buy(size = self.size, exectype=bt.Order.Market, trailamount = trail_amt)
				long_pos = 1
				# print(buy_price)
			# elif self.data.open > self.vwap and self.vwap > self.data.close and self.rsi > 40:
			# elif self.data.open > self.vwap and self.vwap > self.data.close and self.data.close > self.ema  and (datetime.time(14, 00, 0) < self.data.datetime.time() and self.data.datetime.time() < datetime.time(15, 15, 0)):
			# elif self.data.open > self.vwap and self.vwap > self.data.close and self.data.close > self.ema and self.stoch_rsi > 70 and self.ADX > 30: self.ADX.DIplus > self.ADX.DIminus
			elif self.data.open > self.vwap and self.vwap > self.data.close and self.data.close > self.ema and  self.ADX.lines.adx > self.ADX.lines.adx[-1]:
				self.log('SELL CREATE, %.2f' % self.dataclose[0])
				self.order = self.sell(size = self.size, exectype=bt.Order.StopTrail, trailamount = trail_amt)
				# self.order = self.sell(size = self.size, exectype=bt.Order.StopTrail, trailpercent =  0.002)
				# self.order = self.sell(size = self.size, exectype=bt.Order.Market, trailamount = trail_amt)
				self.sellprice = self.dataclose[0]
				short_pos = 1
		# elif self.data.close > (buy_price + 150):	# selling at 2% profit
		elif self.position.size > 0 and self.dataclose[0] >= (self.buyprice + target_price):	# selling at 2% profit
			# self.close()
			self.log('BUY POSITION CLOSE, %.2f' % self.dataclose[0])
			# self.order = self.sell(size = self.size)
			self.order = self.close(size = self.size)
			long_pos = 0
			# print(self.data.close)
		# elif self.data.close < (buy_price - 100):	# selling at 1% loss due to SL
		# elif self.position.size > 0 and self.dataopen[0] <= (self.buyprice - stoploss):	# selling at 1% loss due to SL
		elif self.position.size > 0 and self.dataopen[0] <= (self.buyprice - self.ATR/2):	# selling at 1% loss due to SL
			# self.close()
			self.log('BUY POSITION SL HIT, %.2f' % self.dataopen[0])
			# self.order = self.sell(size = self.size)
			self.order = self.close(size = self.size)
			long_pos = 0
			# print(self.data.close)
		elif self.position.size < 0 and self.dataclose[0] <= (self.sellprice + target_price):	# selling at 2% profit
			# print(self.dataclose[0], self.sellprice , target_price)
			# self.close()
			self.log('SELL POSITION CLOSE, %.2f' % self.dataclose[0])
			# self.order = self.sell(size = self.size)
			self.order = self.close(size = self.size)
			short_pos = 0
			# print(self.data.close)
		# elif self.position.size < 0 and self.dataopen[0] >= (self.sellprice - stoploss):	# selling at 1% loss due to SL
		elif self.position.size < 0 and self.dataopen[0] >= (self.sellprice - self.ATR/2):	# selling at 1% loss due to SL
			# self.close()
			self.log('SELL POSITION SL HIT, %.2f' % self.dataopen[0])
			# self.order = self.sell(size = self.size)
			self.order = self.close(size = self.size)
			short_pos = 0
			# print(self.data


class PandasData(bt.feeds.PandasData):
	# lines = ('adj_close','pct','pct2','pct3')
	params = (
		('datetime', None),
		('open','open'),
		('high','high'),
		('low','low'),
		('close','close'),
		('volume','volume'),
		('openinterest',None)
	)


if __name__ == '__main__':
	# Instantiate Cerebro engine
	cerebro = bt.Cerebro()

	# Create a Data Feed
	src = './data/temp/onemin_dump/2020/IntradayData_MAY2020/'
	# src = './data/temp/onemin_dump/IntradayData_JAN_JUN2019/IntradayData_JAN_JUN2019/'
	# src = './data/temp/onemin_dump/IntradayData_JUL_DEC2019/IntradayData_JUL_DEC2019/'
	# src = './data/temp/onemin_dump/IntradayData_2018/IntradayData_2018/'
	
	ticker = 'BANKNIFTY_F1'
	src_file_path = src + ticker + '.txt'
	temp = pd.read_csv(src_file_path, names=['ticker', 'date','time','open','high','low','close','volume','garbage'])
	temp = temp.drop(['garbage'],axis= 1)
	data = temp
	data['temp'] = data['date'].astype(str) +' '+ data['time']
	data['datetime'] = pd.to_datetime(data['temp'],format = '%Y%m%d %H:%M')
	data = data.drop(['date','time','temp'],axis=1)
	data.set_index('datetime',inplace=True)
	print(data.head())
	# df_onemin = data
	# ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close': 'last','volume':'sum'}
	# data = data.resample("15min").apply(ohlc_dict).dropna()
	# data['vwap'] = (df_onemin['volume']*(df_onemin['high']+df_onemin['low']+df_onemin['close'])/3).rolling(min_periods=1,window=5).sum() / df_onemin['volume'].rolling(min_periods=1,window=5).sum()
	# print(data)

	print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

	#setup:
	target_price =  50	#percent or point (e.g. 2% or 10 points up)
	stoploss = 10		#percent or point (e.g. 2% or 10 points up)

	timeframe = 5		#3/5/10/15 mins candles
	trail_amt = 5

	# data = bt.feeds.PandasData(dataname=data)
	data = bt.feeds.PandasData(dataname = data , timeframe = bt.TimeFrame.Minutes, compression=1, sessionstart = datetime.time(9,30), sessionend=datetime.time(15,30))
	data_5_min = cerebro.resampledata(data, timeframe = bt.TimeFrame.Minutes, compression = timeframe)
	data_1_day = cerebro.resampledata(data, timeframe = bt.TimeFrame.Days, compression = 1)
	data_1_day.plotinfo.plot = False
	# df_onemin = bt.feeds.PandasData(dataname=df_onemin,name='df_onemin')
	# data_15min = cerebro.resampledata(data,timeframe=bt.TimeFrame.Minutes,compression=15,name='15min_bar')
	# cerebro.adddata(data)
	# cerebro.adddata(data_5_min)
	# cerebro.adddata(df_onemin, name='df_onemin')
	# Add strategy to Cerebro
	cerebro.addstrategy(MyStrategy)
	cerebro.broker.setcommission(commission=0.000)
	cerebro.broker.setcash(1000000.0)

	# Analyze the trades
	cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

	# cerebro.addwriter(bt.WriterFile, csv='temp_test.csv', rounding=2)
	cerebro.addwriter(bt.WriterFile, csv = True, out='temp_test.csv', rounding=2)
	# Run Cerebro Engine
	backtests = cerebro.run()
	backtest = backtests[0]

	print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
	trades = backtest.analyzers.trades.get_analysis()
	total_trades = trades.total.closed
	total_won = trades.won.total
	perc_won = total_won / total_trades
	win_streak = trades.streak.won.longest
	loss_streak = trades.streak.lost.longest
	total_won_amt = trades.won.pnl.total
	total_loss_amt = trades.lost.pnl.total
	print('Test Summary: Trades {} - Won {} - %_Won: {:.2f}'.format(total_trades, total_won, perc_won))
	print('Lognest win streak: {} - Longest loss streak {} '.format(win_streak, loss_streak))
	print('Total won amount: {:.2f} - Total loss amount {:.2f} '.format(total_won_amt, total_loss_amt))
	# pprint.pprint(trades)
	# print(backtest.analyzers.trades.get_analysis())

	# Plot the result
	# cerebro.plot(style='candlestick', barup='green', bardown='red')
	# b = Bokeh(style='bar', scheme=Tradimo())
	# cerebro.plot(b)
	# Store the figures returned by cerebro.plot() and plot them w/plotly
	result = cerebro.plot(style='candlestick', barup='green', bardown='red')
	plotly.offline.plot_mpl(result[0][0], filename='backtest.html')