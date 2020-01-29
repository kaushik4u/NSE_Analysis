import pandas as pd
import os


srcFolder = './data/temp/onemin_dump/IntradauData_JUL_DEC2019/IntradayData_JUL_DEC2019/'

# print(os.listdir(srcFolder))
fileList = os.listdir(srcFolder)
index = 'BANKNIFTY.txt'

df = pd.read_csv(srcFolder + index, index_col=False, names=['ticker', 'date', 'time', 'open', 'high', 'low', 'close', 'volume'])
# Rename all of the columns, keeping them in order
# df.columns = ['ticker', 'date', 'time', 'open', 'high', 'low','close','volume']
df['datetime'] = df[['date', 'time']].astype(str).apply(' '.join, axis=1)
# df['date'] = pd.to_datetime(df['date'], format="%Y%m%d")
# df['time'] = pd.to_datetime(df['time'], format="%H:%M").dt.time
# df['time'] = pd.to_timedelta(df['time'], format="%H:%M")
df['datetime'] = pd.to_datetime(df['datetime'], format="%Y%m%d %H:%M")
print(df.head())
print(df[['date', 'time', 'datetime']].dtypes)
