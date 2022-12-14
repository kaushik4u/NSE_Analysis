import backtrader as bt
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


class TestingStrategy(bt.Strategy):
	params = (
        ('ema',10), # Tuple of tuples containing any variable settings required by the strategy.
		('trail_amt',5),
		('target_price',30),
		('stoploss',10)
        # ('printlog',False), # Stop printing the log of the trading strategy
        
    )
	def log(self, txt, dt=None, doprint=False):
		if doprint:
			dt = dt or self.datas[0].datetime.datetime(0)
			print('%s, %s' % (dt.isoformat(), txt))
	
	def __init__(self):
		self.vwap = VWAP(period=5)
		self.dataclose = self.datas[0].close
		self.order = None
		self.buyprice = None
		self.sellprice = None
		self.buycomm = None
		self.size = 1 #self.broker.getcash() / self.data.close 
		self.rsi = bt.indicators.RSI(self.data)
		self.ema = bt.indicators.ExponentialSmoothing(self.data, period=self.params.ema)
		

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
				
		if not self.position:  # not in the market
			
			if self.data.open < self.vwap and self.vwap < self.data.close and self.data.close > self.ema:
				#self.log('BUY CREATE, %.2f' % self.dataclose[0])
				buy_price = self.data.close
				self.order = self.buy(size = self.size, exectype=bt.Order.StopTrail, trailamount = self.params.trail_amt)
				
			
			elif self.data.open > self.vwap and self.vwap > self.data.close and self.data.close > self.ema  and (datetime.time(14, 00, 0) < self.data.datetime.time() and self.data.datetime.time() < datetime.time(15, 15, 0)):
				#self.log('SELL CREATE, %.2f' % self.dataclose[0])
				self.order = self.sell(size = self.size, exectype=bt.Order.StopTrail, trailamount = self.params.trail_amt)
				self.sellprice = self.dataclose[0]
		
		elif self.position.size > 0 and self.dataclose[0] > (self.buyprice + self.params.target_price):	# selling at 2% profit
			
			#self.log('BUY POSITION CLOSE, %.2f' % self.dataclose[0])
			# self.order = self.sell(size = self.size)
			self.order = self.close(size = self.size)
		
		elif self.position.size > 0 and self.dataclose[0] < (self.buyprice - self.params.stoploss):	# selling at 1% loss due to SL
			
			#self.log('BUY POSITION SL HIT, %.2f' % self.dataclose[0])
			self.order = self.close(size = self.size)
			
		elif self.position.size < 0 and self.dataclose[0] < (self.sellprice + self.params.target_price):	# selling at 2% profit
					
			#self.log('SELL POSITION CLOSE, %.2f' % self.dataclose[0])
			self.order = self.close(size = self.size)
			
		elif self.position.size < 0 and self.dataclose[0] > (self.sellprice - self.params.stoploss):	# selling at 1% loss due to SL
			
			#self.log('SELL POSITION SL HIT, %.2f' % self.dataclose[0])
			self.order = self.close(size = self.size)
	
	def stop(self):
		self.log('EMA Period: {} Trailing SL: {} Ending Value: {:.2f}'.format(
			self.params.ema,
			self.params.trail_amt,
			self.broker.getvalue()),
				 doprint=True)

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
	
	ticker = 'BANKNIFTY_F1'
	src_file_path = src + ticker + '.txt'
	temp = pd.read_csv(src_file_path, names=['ticker', 'date','time','open','high','low','close','volume','garbage'])
	temp = temp.drop(['garbage'],axis= 1)
	data = temp
	data['temp'] = data['date'].astype(str) +' '+ data['time']
	data['datetime'] = pd.to_datetime(data['temp'],format = '%Y%m%d %H:%M')
	data = data.drop(['date','time','temp'],axis=1)
	data.set_index('datetime',inplace=True)
	# print(data.head())
	# df_onemin = data
	# ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close': 'last','volume':'sum'}
	# data = data.resample("15min").apply(ohlc_dict).dropna()
	# data['vwap'] = (df_onemin['volume']*(df_onemin['high']+df_onemin['low']+df_onemin['close'])/3).rolling(min_periods=1,window=5).sum() / df_onemin['volume'].rolling(min_periods=1,window=5).sum()
	# print(data)

	print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

	#setup:
	target_price =  20	#percent or point (e.g. 2% or 10 points up)
	stoploss = 10		#percent or point (e.g. 2% or 10 points up)

	timeframe = 5		#3/5/10/15 mins candles
	trail_amt = 5

	# data = bt.feeds.PandasData(dataname=data)
	data = bt.feeds.PandasData(dataname = data , timeframe = bt.TimeFrame.Minutes, compression=1, sessionstart = datetime.time(9,30), sessionend=datetime.time(15,30))
	data_5_min = cerebro.resampledata(data, timeframe = bt.TimeFrame.Minutes, compression = timeframe)
	data_1_day = cerebro.resampledata(data, timeframe = bt.TimeFrame.Days, compression = 1)
	data_1_day.plotinfo.plot = False

	# Add strategy to Cerebro
	# cerebro.addstrategy(TestingStrategy)
	cerebro.optstrategy(TestingStrategy, ema = range(5,40,1), trail_amt = 0)

	# cerebro.addsizer(bt.sizers.FixedSize,stake=1)

	cerebro.broker.setcommission(commission=0)
	cerebro.broker.setcash(100000.0)
	
	# Analyze the trades
	cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
	# cerebro.run()

	# Run Cerebro Engine
	backtests = cerebro.run()
	backtest = backtests[0]

	# print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
	# trades = backtest.analyzers.trades.get_analysis()
	# total_trades = trades.total.closed
	# total_won = trades.won.total
	# perc_won = total_won / total_trades
	# win_streak = trades.streak.won.longest
	# loss_streak = trades.streak.lost.longest
	# total_won_amt = trades.won.pnl.total
	# total_loss_amt = trades.lost.pnl.total
	# print('Test Summary: Trades {} - Won {} - %_Won: {:.2f}'.format(total_trades, total_won, perc_won))
	# print('Lognest win streak: {} - Longest loss streak {} '.format(win_streak, loss_streak))
	# print('Total won amount: {:.2f} - Total loss amount {:.2f} '.format(total_won_amt, total_loss_amt))

	# Plot the result
	# cerebro.plot(style='candlestick', barup='green', bardown='red')