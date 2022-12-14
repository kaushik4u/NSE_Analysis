from sqlalchemy import create_engine
import pymysql
import pandas as pd

 

sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1/test', pool_recycle=3600)
dbConnection = sqlEngine.connect()
ticker = 'ITC'
# for all records
frame = pd.read_sql("select * from nse_nifty50_data", dbConnection)

# selective stock less memory intensive
frame = pd.read_sql("select * from nse_nifty50_data where ticker = '" + ticker + "'", dbConnection)


pd.set_option('display.expand_frame_repr', False)
frame.set_index('datetime',inplace = True)
print(frame)

dbConnection.close()
frame = frame[frame['volume'] !=0]
ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close': 'last','volume':'sum'}
frame = frame.resample("15Min").apply(ohlc_dict).dropna()
# frame = frame[frame['volume'] !=0]
frame['vwap'] = (frame['volume']*(frame['high']+frame['low']+frame['close'])/3).cumsum() / frame['volume'].cumsum()
print(frame)