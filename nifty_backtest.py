import pandas as pd
import os


srcFolder = './data/temp/onemin_dump/IntradauData_JUL_DEC2019/IntradayData_JUL_DEC2019/'

# print(os.listdir(srcFolder))
fileList = os.listdir(srcFolder)
index = 'BANKNIFTY.txt'

df = pd.read_csv(srcFolder + index, index_col=False, names=['ticker', 'date', 'time', 'open', 'high', 'low', 'close', 'volume'])
# Rename all of the columns, keeping them in order
# df.columns = ['ticker', 'date', 'time', 'open', 'high', 'low','close','volume']
print(df.head())
