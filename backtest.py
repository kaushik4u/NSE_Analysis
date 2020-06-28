import backtrader as bt
# import backtrader.indicators as btind
import pandas as pd
import datetime


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
		# self.pp = PivotPoint(self.data1)
		self.pp = bt.ind.PivotPoint(self.data1)
		# self.pp.plotinfo.plotmaster = self.data1
		self.dataclose = self.datas[0].close
		self.order = None
		self.buyprice = None
		self.buycomm = None
		print(self.data,self.data1)
	
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
		buy_price = 0
		if not self.position:  # not in the market
			# if self.data.open < self.vwap and self.vwap < self.data.close and (datetime.time(9, 30, 0) < self.data.datetime.time() and self.data.datetime.time() < datetime.time(11, 30, 0)):
			if self.data.open < self.vwap and self.vwap < self.data.close:
				
				self.log('BUY CREATE, %.2f' % self.dataclose[0])
				buy_price = self.data.close
				self.order = self.buy()
				# print(buy_price)
		# elif self.data.close > (buy_price + 150):	# selling at 2% profit
		elif self.dataclose[0] > (self.buyprice + 150):	# selling at 2% profit
			# self.close()
			self.log('SELL CREATE, %.2f' % self.dataclose[0])
			self.order = self.sell()
			# print(self.data.close)
		# elif self.data.close < (buy_price - 100):	# selling at 1% loss due to SL
		elif self.dataclose[0] < (self.buyprice - 100):	# selling at 1% loss due to SL
			# self.close()
			self.log('SELL CREATE SL HIT, %.2f' % self.dataclose[0])
			self.order = self.sell()
			# print(self.data.close)


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

	# data = bt.feeds.PandasData(dataname=data)
	data = bt.feeds.PandasData(dataname = data , timeframe = bt.TimeFrame.Minutes, compression=1, sessionstart = datetime.time(9,30), sessionend=datetime.time(15,30))
	data_5_min = cerebro.resampledata(data, timeframe = bt.TimeFrame.Minutes, compression=15)
	data_1_day = cerebro.resampledata(data, timeframe = bt.TimeFrame.Days, compression=1)
	# data_1_day.plotinfo.plot = False
	# df_onemin = bt.feeds.PandasData(dataname=df_onemin,name='df_onemin')
	# data_15min = cerebro.resampledata(data,timeframe=bt.TimeFrame.Minutes,compression=15,name='15min_bar')
	# cerebro.adddata(data)
	# cerebro.adddata(data_5_min)
	# cerebro.adddata(df_onemin, name='df_onemin')
	# Add strategy to Cerebro
	cerebro.addstrategy(MyStrategy)
	cerebro.broker.setcommission(commission=0)
	cerebro.broker.setcash(100000.0)
	# Run Cerebro Engine
	cerebro.run()

	print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

	# Plot the result
	cerebro.plot(style='candlestick', barup='green', bardown='red')