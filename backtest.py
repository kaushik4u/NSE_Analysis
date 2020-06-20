import backtrader as bt
# import backtrader.indicators as btind
import pandas as pd


class VolumeWeightedAveragePrice(bt.Indicator):

    alias = ('VWAP', 'VolumeWeightedAveragePrice',)
    lines = ('vwap',)
    params = (('period', 5),)

    plotinfo = dict(subplot=False)


    def __init__(self):

        self.addminperiod(self.p.period)
        self.cum_price_by_Volume = list()
        self.cum_volume = list()
        


    def _plotlabel(self):

        # This method returns a list of labels that will be displayed
        # behind the name of the indicator on the plot

        # The period must always be there

        plabels = [self.p.period]

        plabels += [self.lines.vwap]
        return plabels

    def next(self):



        price = (self.data.close + self.data.high + self.data.low) / 3
        price = (self.getdatabyname('df_onemin').close + self.getdatabyname('df_onemin').high + self.getdatabyname('df_onemin').low) / 3

        #check price
        # print(price)

        volume = self.data.volume
        volume = self.getdatabyname('df_onemin').volume
        #check price
        # print(volume)

        price_by_Volume = price * volume


        self.cum_price_by_Volume.append(price_by_Volume)
        self.cum_volume.append(volume)

        if len(self.cum_price_by_Volume) and len(self.cum_volume) >= self.p.period:

            #Check cumulative values for accuracy

            # print(sum(self.cum_price_by_Volume[-1*(self.p.period):]))
            # print(sum(self.cum_volume[-1*(self.p.period):]))

            # get last n'th (period) values in list and perform calculations for VWAP. This is because
            # the latest values go at the end of the list due to the way data is imported (earliest to latest)

            if sum(self.cum_volume[-1*(self.p.period):]) > 0:
            	self.lines.vwap[0] = sum(self.cum_price_by_Volume[-1*(self.p.period):]) / sum(self.cum_volume[-1*(self.p.period):])


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
    def __init__(self):
    	# vwap = self.vwap
    	# self.vwap = bt.indicators.VWAP(period=5)
    	# print(self.getdatabyname('df_onemin').datetime[0])
    	self.vwap = VWAP(period=15)

    def next(self):
    	buy_price = 0
    	if not self.position:  # not in the market
    		if self.data.open < self.vwap and self.vwap < self.data.close:
    			self.buy()
    			buy_price = self.data.close
    			print(buy_price)
    	elif self.data.close > buy_price * 1.02:	# selling at 2% profit
    		self.close()
    		print(self.data.close)
    	elif self.datat.close < buy_price * 0.99:	# selling at 1% loss due to SL
    		self.close()
    		print(self.data.close)




 
if __name__ == '__main__':
	# Instantiate Cerebro engine
	cerebro = bt.Cerebro()

	# Create a Data Feed
	src = './data/temp/onemin_dump/2020/IntradayData_MAY2020/'
	ticker = 'ITC'
	src_file_path = src + ticker + '.txt'
	temp = pd.read_csv(src_file_path, names=['ticker', 'date','time','open','high','low','close','volume','garbage'])
	temp = temp.drop(['garbage'],axis= 1)
	data = temp
	data['temp'] = data['date'].astype(str) +' '+ data['time']
	data['datetime'] = pd.to_datetime(data['temp'],format = '%Y%m%d %H:%M')
	data = data.drop(['date','time','temp'],axis=1)
	data.set_index('datetime',inplace=True)

	df_onemin = data
	ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close': 'last','volume':'sum'}
	data = data.resample("15min").apply(ohlc_dict).dropna()
	data['vwap'] = (df_onemin['volume']*(df_onemin['high']+df_onemin['low']+df_onemin['close'])/3).rolling(min_periods=1,window=5).sum() / df_onemin['volume'].rolling(min_periods=1,window=5).sum()
	print(data)

	print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
	data = bt.feeds.PandasData(dataname=data)
	df_onemin = bt.feeds.PandasData(dataname=df_onemin)
	cerebro.adddata(data)
	cerebro.adddata(df_onemin, name='df_onemin')
	# Add strategy to Cerebro
	cerebro.addstrategy(MyStrategy)

	# Run Cerebro Engine
	cerebro.run()

	print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

	# Plot the result
	cerebro.plot(style='candlestick', barup='green', bardown='red')