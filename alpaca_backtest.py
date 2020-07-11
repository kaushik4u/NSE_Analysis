import alpaca_backtrader_api
import backtrader as bt
from datetime import datetime

ALPACA_API_KEY = 'PKVYQE2ER91N5NH8U3NS'
ALPACA_SECRET_KEY = 'aV4THxtzrNpNKCrysn8cMqW0IJM9INmGMVPOmr8r'
ALPACA_PAPER = True


# class SmaCross(bt.SignalStrategy):
#   def __init__(self):
#     sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
#     crossover = bt.ind.CrossOver(sma1, sma2)
#     self.signal_add(bt.SIGNAL_LONG, crossover)

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
	params = (
        ('ema',10), # Tuple of tuples containing any variable settings required by the strategy.
		('trail_amt',5),
		('target_price',30),
		('stoploss',10)
        # ('printlog',False), # Stop printing the log of the trading strategy        
    )

	def log(self, txt, dt=None):
		dt = dt or self.datas[0].datetime.datetime(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		# vwap = self.vwap
		# self.vwap = bt.indicators.VWAP(period=5)
		# print(self.getdatabyname('df_onemin').datetime[0])
		# self.vwap = VWAP(period=5)
		# self.pp = PivotPoint(self.data1)
		# self.pp = bt.ind.PivotPoint(self.data1)
		# self.pp.plotinfo.plotmaster = self.data1
		self.dataclose = self.datas[1].close
		self.dataopen = self.datas[1].open
		# print(self.data,self.data1)
		self.stoch_rsi = StochRSI(self.data, period = 5)
		# print("RSI "+str(self.rsi))
		self.vwap = VWAP(period=5)
		self.order = None
		self.buyprice = None
		self.sellprice = None
		self.buycomm = None
		self.size = 1 #self.broker.getcash() / self.data.close 
		self.rsi = bt.indicators.RSI(self.data1)
		self.stoch_rsi = StochRSI(self.data1, period = 5)
		self.ema = bt.indicators.ExponentialSmoothing(self.data1, period=self.params.ema)

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
			if self.data1.open < self.vwap and self.vwap < self.data1.close and self.data1.close > self.ema and self.stoch_rsi < 30:
				self.log('BUY CREATE, %.2f' % self.dataclose[0])
				buy_price = self.data1.close
				self.order = self.buy(size = self.size, exectype=bt.Order.StopTrail, trailamount = self.params.trail_amt)
				# self.order = self.buy(size = self.size, exectype=bt.Order.StopTrail, trailpercent =  0.002)
				# self.order = self.buy(size = self.size, exectype=bt.Order.Market, trailamount = trail_amt)
				long_pos = 1
				# print(buy_price)
			# elif self.data.open > self.vwap and self.vwap > self.data.close and self.rsi > 40:
			# elif self.data.open > self.vwap and self.vwap > self.data.close and self.data.close > self.ema  and (datetime.time(14, 00, 0) < self.data.datetime.time() and self.data.datetime.time() < datetime.time(15, 15, 0)):
			elif self.data1.open > self.vwap and self.vwap > self.data1.close and self.data1.close > self.ema and self.stoch_rsi > 70:
				self.log('SELL CREATE, %.2f' % self.dataclose[0])
				self.order = self.sell(size = self.size, exectype=bt.Order.StopTrail, trailamount = self.params.trail_amt)
				# self.order = self.sell(size = self.size, exectype=bt.Order.StopTrail, trailpercent =  0.002)
				# self.order = self.sell(size = self.size, exectype=bt.Order.Market, trailamount = trail_amt)
				self.sellprice = self.dataclose[0]
				short_pos = 1
		# elif self.data.close > (buy_price + 150):	# selling at 2% profit
		elif self.position.size > 0 and self.dataclose[0] >= (self.buyprice + self.params.target_price):	# selling at 2% profit
			# self.close()
			self.log('BUY POSITION CLOSE, %.2f' % self.dataclose[0])
			# self.order = self.sell(size = self.size)
			self.order = self.close(size = self.size)
			long_pos = 0
			# print(self.data.close)
		# elif self.data.close < (buy_price - 100):	# selling at 1% loss due to SL
		elif self.position.size > 0 and self.dataopen[0] <= (self.buyprice - self.params.stoploss):	# selling at 1% loss due to SL
			# self.close()
			self.log('BUY POSITION SL HIT, %.2f' % self.dataopen[0])
			# self.order = self.sell(size = self.size)
			self.order = self.close(size = self.size)
			long_pos = 0
			# print(self.data.close)
		elif self.position.size < 0 and self.dataclose[0] <= (self.sellprice + self.params.target_price):	# selling at 2% profit
			# print(self.dataclose[0], self.sellprice , target_price)
			# self.close()
			self.log('SELL POSITION CLOSE, %.2f' % self.dataclose[0])
			# self.order = self.sell(size = self.size)
			self.order = self.close(size = self.size)
			short_pos = 0
			# print(self.data.close)
		elif self.position.size < 0 and self.dataopen[0] >= (self.sellprice - self.params.stoploss):	# selling at 1% loss due to SL
			# self.close()
			self.log('SELL POSITION SL HIT, %.2f' % self.dataopen[0])
			# self.order = self.sell(size = self.size)
			self.order = self.close(size = self.size)
			short_pos = 0
			# print(self.data







if __name__ == '__main__':
	cerebro = bt.Cerebro()
	cerebro.addstrategy(MyStrategy)

	store = alpaca_backtrader_api.AlpacaStore(
		key_id=ALPACA_API_KEY,
		secret_key=ALPACA_SECRET_KEY,
		paper=ALPACA_PAPER
	)
	if not ALPACA_PAPER:
		broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
		cerebro.setbroker(broker)

	DataFactory = store.getdata  # or use alpaca_backtrader_api.AlpacaData
	data0 = DataFactory(
		dataname='GOOGL', 
		historical=True, 
		fromdate=datetime(2020, 6, 1),
		timeframe=bt.TimeFrame.Minutes
	)

	#setup:
	target_price =  15	#percent or point (e.g. 2% or 10 points up)
	stoploss = 5		#percent or point (e.g. 2% or 10 points up)

	timeframe = 15		#3/5/10/15 mins candles
	trail_amt = 5

	cerebro.adddata(data0)
	cerebro.resampledata(data0,timeframe=bt.TimeFrame.Minutes,compression=timeframe)
	# cerebro.adddata(data0)
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
	
	# Plot the result
	cerebro.plot(style='candlestick', barup='green', bardown='red')

# print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
# cerebro.run()
# print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
# cerebro.plot()