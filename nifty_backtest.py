import pandas as pd
import os
from os import path

srcFolder = './data/temp/onemin_dump/IntradauData_JUL_DEC2019/IntradayData_JUL_DEC2019/'
# srcFolder = './data/temp/onemin_dump/IntradayData_JAN_JUN2019/IntradayData_JAN_JUN2019/'
srcFolder = './data/temp/onemin_dump/IntradayData_2018/IntradayData_2018/'

desFolder = './data/temp/onemin_consolidated/'
# print(os.listdir(srcFolder))
fileList = os.listdir(srcFolder)
index = 'BANKNIFTY.txt'


def format_ticker(srcPath, index, desFolder):
    df = pd.read_csv(srcPath + index, index_col=False, names=['ticker', 'date', 'time', 'open', 'high', 'low', 'close', 'volume'])
    # Rename all of the columns, keeping them in order
    # df.columns = ['ticker', 'date', 'time', 'open', 'high', 'low','close','volume']
    df['datetime'] = df[['date', 'time']].astype(str).apply(' '.join, axis=1)
    # df['date'] = pd.to_datetime(df['date'], format="%Y%m%d")
    # df['time'] = pd.to_datetime(df['time'], format="%H:%M").dt.time
    # df['time'] = pd.to_timedelta(df['time'], format="%H:%M")
    df['datetime'] = pd.to_datetime(df['datetime'], format="%Y%m%d %H:%M")
    print(df.head())
    # print(df[['date', 'time', 'datetime']].dtypes)
    index = index.replace('.txt','.csv')
    # delete redundant date and time cols
    df = df.drop(['date','time'],axis=1)
    
    if path.exists(desFolder + index):
        df1 = pd.read_csv(desFolder + index)
        df_diff = pd.concat([df, df1]).drop_duplicates()
        cond = df['datetime'].isin(df1['datetime']) == True
        df.drop(df[cond].index, inplace = True)
        # df = pd.concat([df, df1])
        # df = df.reset_index(drop=True)
        # df_gpby = df.groupby(list(df.columns))
        # idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
        # df.reindex(idx)
        # print(df.head())
        # df = df_diff
        df.to_csv(desFolder + index, mode='a', header=False, index=False)
    else:
        df.to_csv(desFolder + index, mode='a', index=False)
    # print("file exist:" + str(path.exists(desFolder + index)))


format_ticker(srcFolder, index, desFolder)

import json
import numpy as np
def get_backtest_data(ticker):
   # print(request.args.to_dict())
   src = './data/temp/onemin_consolidated/' + ticker + '.csv'
   df = pd.read_csv(src)
   df = df.sort_values(by='datetime',ascending=False)
   df['datetime'] = pd.to_datetime(df['datetime'])
   print(df.info())
   # df = df.groupby(pd.Grouper(key='datetime', freq='15min'))
   # df.set_index('datetime', drop=True, append=False, inplace=True, verify_integrity=False)
   df = df.sort_index()
   # df = df.groupby(pd.Grouper(freq='D')).transform(np.cumsum).resample('D', how='ohlc')
   # df = df['close'].resample('15min').ohlc()
   # df = df['close'].resample('D').agg({'close': 'ohlc', 'volume': 'sum'})
   df = df[['datetime','close','volume']]
   df.set_index('datetime', drop=True, append=False, inplace=True, verify_integrity=False)
   df = df.resample('D').agg({'close': 'ohlc', 'volume': 'sum'})
   df.reset_index(level=[0])
   print(df.columns)
   print(df.head())
   json_data = json.JSONDecoder().decode(df.head().to_json(orient="table"))
   # return jsonify({'data': json_data, 'technical': []})
   return json_data

test = get_backtest_data('BANKNIFTY')
print(test)
