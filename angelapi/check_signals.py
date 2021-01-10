from datetime import datetime
import pandas as pd
from plotly_approach import fetch_yahoo_feed, process_yahoo_feed, calc_fib_levels
import json
import pandas as pd
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
# from smartapi import SmartSocket #or from smartapi.smartSocket import SmartSocket
# from smartapi import WebSocket
import time
with open ('./live_ticks.txt', mode='r') as f:
    temp = f.readlines()

ts = []
opts = []
ltp = []
# for t in temp:
#     if "31DEC" in t:
#         ts.append(t.split('>')[0])
#         opts.append(t.split('>')[0].split('=')[0])
#         ltp.append(t.split('>')[0].split('=')[1])
cols = ['Datetime', 'ticker', 'ltp']
df = pd.read_csv('./live_ticks.txt', sep=" > | = ", header=None, names=cols, engine='python')
df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d/%m/%Y %H:%M:%S')
print(datetime.today().date())
# df = df[df['datetime'] > "2021-01-05 09:00:00"]
df = df[df['Datetime'] > pd.Timestamp(datetime.today().date())]
# df['Datetime'] = df['datetime']
# df.columns = ['Datetime','Ticker']
# df_5_min = df.set_index('Datetime')
# df_5_min = df_5_min['ltp'].resample('5min').ohlc()
# df_5_min.columns = ['Open','High','Low','Close']
# df_5_min.reset_index(level=0, inplace=True)
df_yahoo = process_yahoo_feed('5m')
# print(df)
print(df_yahoo)
# print(df_5_min)

target = 32100
side = "CE"
searchStr = 'BANKNIFTY31DEC20' + str(target) + side
print(searchStr)
# dt_match_str = datetime.now().strftime('%Y-%m-%d') +' 9:30:00'
# dt_match_str = datetime.now().strftime('%Y-%m-%d') +' 09:15:00'
dt_match_str = "2021-01-08 9:15:00"
# fiblvl = calc_fib_levels(df_5_min,dt_match_str)
fiblvl = calc_fib_levels(df_yahoo,dt_match_str)
print(fiblvl)
# print(df['ticker'].unique())
# print(df[df['ticker'] == searchStr])

# entry_price = df[df['ticker'] == searchStr]['ltp'].values[0]
# # print(entry_price)
# print('Initial entry price: ' + searchStr + ' @ ' + str(entry_price))
# for price in df[df['ticker'] == searchStr]['ltp']:
#     if price > entry_price * 1.10:
#         print('Exit price ' + searchStr + ' @ '+ str(price) + ' (profit)  = ' + str(price - entry_price))
#         # break
#     elif price < entry_price * 0.90:
#         print('Exit price ' + searchStr + ' @ '+ str(price) + ' (loss)  = ' + str(price - entry_price))
#         # break

def trade_decision(df,flvl,dt):
    df = df.set_index('Datetime')
    # df_15 = df['Close'].resample('15min').ohlc()
    df_15 = process_yahoo_feed('15m')
    df_15 = df_15.reset_index()
    idx = df_15[df_15['Datetime'] == dt].index.values[0]
    print(df_15.iloc[idx])
    price_diff = df_15.iloc[idx]['Close'] - df_15.iloc[idx]['Open']
    print("Price diff [close - open]: " + str(price_diff))
    # check if there is 50 point diff in 1st candle
    leveln618 = flvl[0]
    leveln382 = flvl[1]
    level0 = flvl[2]
    level382 = flvl[3]
    level618 = flvl[4]
    level1 = flvl[5]
    level1382 = flvl[6]
    level1618 = flvl[7]
    if (abs(price_diff) > 50):
        pass

        
    
        

trade_decision(df_yahoo,fiblvl,dt_match_str)

""" 
with open('./conf.json') as f:
    conf_keys = json.load(f)
    # print(d)

# conf_keys = json.load("./conf.json")
print(conf_keys['clientcode'])
# s = requests.Session()

login_url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"

login_payload = {
    "clientcode": conf_keys['clientcode'],
    "password": conf_keys['password']
}

# ip_info = requests.get('http://ipinfo.io/json').json()
# print(ip_info)

#create object of call
obj = SmartConnect(api_key=conf_keys['apikey'])

#login api call

data = obj.generateSession(conf_keys['clientcode'],conf_keys['password'])
refreshToken = data['data']['refreshToken']
# print("\nRefresh token: ", refreshToken)

token_data = obj.generateToken(refreshToken)

feedToken = token_data['data']['feedToken']
# print("\nFeed token: ", feedToken)
 """
# ltpRes = obj.ltpData('NFO','BANKNIFTY14JAN2131900CE','50699')
# print(ltpRes)

# BANKNIFTY07JAN2131900CE 10:41 189.0 BN 31843
# 06/01/2021 14:05:48 BANKNIFTY07JAN2131900CE 153.75

# entry_price = 189

def checkLTP(ticker):
    df = pd.read_json('./OpenAPIScripMaster.json')
    token = df[df['symbol']==ticker]['token'].values[0]
    exchange = df[df['symbol']==ticker]['exch_seg'].values[0]
    ltpRes = obj.ltpData(exchange,ticker,token)
    # print(ltpRes)
    priceStr = datetime.now().strftime('%d/%m/%Y %H:%M:%S') +' > '+ ltpRes['data']['tradingsymbol'] +' = '+ str(ltpRes['data']['ltp']) +'\n'
    print(priceStr)
    with open('signals.txt',mode='a+' ) as f:
        f.write(priceStr)

starttime = time.time()
time_interval = 5 * 60.0 # 5 minutes
# while True:
#     checkLTP('BANKNIFTY14JAN2132300CE')
#     time.sleep(time_interval - ((time.time() - starttime) % time_interval))

