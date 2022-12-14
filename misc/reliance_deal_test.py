import pandas as pd
import os
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from finta import TA

april_src = '../NSE_Data/data/temp/onemin_dump/2020/APR-20200425T192750Z-001/APR'

filename = 'RELIANCE.txt'
filename = 'IBULHSGFIN.txt'

fu = [f.path.replace('\\','/') for f in os.scandir(april_src) if f.is_dir()]

# print(fu)
data = pd.DataFrame()
for f in fu:
    # print(f + '/' + filename)
    file_src = f + '/' + filename
    print('Opening...'+file_src)
    # with open(file_src, 'r') as f:
    #     data = f.readlines()
    temp = pd.read_csv(file_src,names=['ticker', 'date','time','open','high','low','close','volume','garbage'])
    temp = temp.drop(['garbage'],axis=1)
    data = data.append(temp,ignore_index=True)

data['temp'] = data['date'].astype(str) +' '+ data['time']
data['datetime'] = pd.to_datetime(data['temp'],format = '%Y%m%d %H:%M')
data = data.drop(['date','time','temp'],axis=1)

print(data.dtypes)
print(data)

def HA(df):
    df['HA_Close']=(df['open']+ df['high']+ df['low']+df['close'])/4

    idx = df.index.name
    df.reset_index(inplace=True)

    for i in range(0, len(df)):
        if i == 0:
            df.set_value(i, 'HA_Open', ((df.get_value(i, 'open') + df.get_value(i, 'close')) / 2))
        else:
            df.set_value(i, 'HA_Open', ((df.get_value(i - 1, 'HA_Open') + df.get_value(i - 1, 'HA_Close')) / 2))

    if idx:
        df.set_index(idx, inplace=True)

    df['HA_High']=df[['HA_Open','HA_Close','high']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','low']].min(axis=1)
    return df

ha_data = HA(data)


def vwap(df):
    q = df.Volume.values
    p = df.Close.values
    return df.assign(vwap=(p * q).cumsum() / q.cumsum())

print(ha_data)
mpf_data = data
mpf_data.set_index('datetime',inplace=True)
mpf_data = mpf_data.drop(['index','ticker','HA_Open','HA_Close','HA_High','HA_Low'], axis=1)
mpf_data.columns = ['Open','High','Low','Close','Volume']
ohlc_dict = {'Open':'first', 'High':'max', 'Low':'min', 'Close': 'last','Volume':'sum'}
mpf_data = mpf_data.resample("1H").apply(ohlc_dict).dropna()
print(mpf_data)
mpf.plot(mpf_data,type='candle',volume=True,show_nontrading=False,style='yahoo')
mpf_data['price_diff'] = mpf_data['Close'] - mpf_data['Open']
mpf_data['normalized_vol'] = (mpf_data['price_diff'].abs()/mpf_data['price_diff']) * mpf_data['Volume']
mpf_data['vol_momentum'] = mpf_data['price_diff'] * mpf_data['Volume']
# mpf_data = mpf_data.apply(vwap)
print(mpf_data[['Volume','Open','Close','price_diff','normalized_vol','vol_momentum']])

print(mpf_data['normalized_vol'].groupby(pd.Grouper(freq='4H')).sum())

mpf_data['vol_momentum'].groupby(pd.Grouper(freq='4H')).sum() .plot.bar()
# print(TA.SMA(mpf_data, 20))
plt.show()