from datetime import datetime, timedelta
import pandas as pd
from plotly_approach import fetch_yahoo_feed, process_yahoo_feed, calc_fib_levels
import json
import pandas as pd
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
# from smartapi import SmartSocket #or from smartapi.smartSocket import SmartSocket
# from smartapi import WebSocket
import time
import math
import pytz

# with open ('./live_ticks.txt', mode='r') as f:
#     temp = f.readlines()

# ts = []
# opts = []
# ltp = []
# for t in temp:
#     if "31DEC" in t:
#         ts.append(t.split('>')[0])
#         opts.append(t.split('>')[0].split('=')[0])
#         ltp.append(t.split('>')[0].split('=')[1])
# cols = ['Datetime', 'ticker', 'ltp']
# df = pd.read_csv('./live_ticks.txt', sep=" > | = ", header=None, names=cols, engine='python')
# df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d/%m/%Y %H:%M:%S')
# print(datetime.today().date())
# df = df[df['datetime'] > "2021-01-05 09:00:00"]
# df = df[df['Datetime'] > pd.Timestamp(datetime.today().date())]
# df['Datetime'] = df['datetime']
# df.columns = ['Datetime','Ticker']
# df_5_min = df.set_index('Datetime')
# df_5_min = df_5_min['ltp'].resample('5min').ohlc()
# df_5_min.columns = ['Open','High','Low','Close']
# df_5_min.reset_index(level=0, inplace=True)
df_yahoo = process_yahoo_feed('5m')
# print(df)
# print(df_yahoo)
# print(df_5_min)

# target = 32100
# side = "CE"
# searchStr = 'BANKNIFTY31DEC20' + str(target) + side
# print(searchStr)
# dt_match_str = datetime.now().strftime('%Y-%m-%d') +' 9:30:00'
dt_match_str = datetime.now().strftime('%Y-%m-%d') +' 09:15:00'
# dt_match_str = "2021-01-22 9:15:00"
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


def find_nearest_level(ltp,option):
    if option == "PE":
        return int(math.floor(ltp / 100.0)) * 100
    elif option == "CE":
        return int(math.ceil(ltp / 100.0)) * 100


def prev_weekday(adate):
    _offsets = (3, 1, 1, 1, 1, 1, 2)
    return adate - timedelta(days=_offsets[adate.weekday()])

def find_pd_extremes(df,dt):
    pday = prev_weekday(datetime.strptime(dt,'%Y-%m-%d'))
    pday = pytz.timezone('Asia/Kolkata').localize(pday)
    curr_day = pytz.timezone('Asia/Kolkata').localize(datetime.strptime(dt,'%Y-%m-%d'))
    # print(pday)
    df = df[(df['Datetime'] >= pday) & (df['Datetime'] < curr_day)]
    # print(df)
    pdh = df['High'].max()
    pdl = df['Low'].min()
    pdch = df['Close'].max()
    pdol = df['Open'].min()
    return pdol, pdh, pdl, pdch

entry_price = 0
exit_price = 0
bn_entry_lvl = None
bn_exit_lvl = None
lotsize = 25
ongoing_trade = False
option_ticker = ""


def trade_tracker(df,ltp):
    # if bn_entry_lvl is None:
    #     return 0
    global entry_price
    global exit_price
    global bn_entry_lvl
    global bn_exit_lvl
    global lotsize
    global ongoing_trade
    # print(option_ticker)
    if bn_entry_lvl is None:
        return 0
    else:       
        # print("BN Level: ", bn_entry_lvl)
        # if ongoing_trade:
        #     exit_price = ltp
        #     ongoing_trade = False
        #     print('{} [Trade Status] Ticker: {} Entry : {} Exit : {} '.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), option_ticker,entry_price,exit_price))
        # else:
        #     entry_price = ltp
        #     ongoing_trade = True
        #     print('{} [Trade Status] Ticker: {} Entry : {} Exit : {} '.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), option_ticker,entry_price,exit_price))
        
        if ongoing_trade == False:
            if decision !=0 or decision is not None:
                entry_price = ltp
                ongoing_trade = True            
                print('{} [Trade Status] Ticker: {} Entry : {} Exit : {} '.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), option_ticker,entry_price,exit_price))

        else:
            if "CE" in decision:
                #book profits
                if df.iloc[-1]['Close'] > bn_entry_lvl['Close'] + 100 and ongoing_trade:    
                    bn_exit_lvl = df.iloc[-1]
                    exit_price = ltp
                    pnl = (exit_price - entry_price) * lotsize
                    ongoing_trade = False
                    trade_status = '{} [Trade Status] Profit made: {} Ticker: {} Entry : {} Exit : {} Lotsize {} BN Entry: {} BN Exit: {} \n'.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'),pnl,option_ticker,entry_price,exit_price,lotsize,bn_entry_lvl['Close'],bn_exit_lvl['Close'])    
                    print(trade_status)
                    with open('tradebook.txt',mode='a+' ) as f:
                        f.write(trade_status)
                # SL hit
                if df.iloc[-1]['Close'] < bn_entry_lvl['Close'] - 50 and ongoing_trade:
                    bn_exit_lvl = df.iloc[-1]
                    exit_price = ltp
                    pnl = (exit_price - entry_price) * lotsize
                    ongoing_trade = False
                    trade_status = '{} [Trade Status] SL Hit: {} Ticker: {} Entry : {} Exit : {} Lotsize {} BN Entry Level {} BN Exit Level: {} \n'.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), pnl,option_ticker,entry_price,exit_price,lotsize,bn_entry_lvl['Close'],bn_exit_lvl['Close'])
                    print(trade_status)
                    with open('tradebook.txt',mode='a+' ) as f:
                        f.write(trade_status)
            if "PE" in decision:
                #book profits
                if df.iloc[-1]['Close'] < bn_entry_lvl['Close'] - 100 and ongoing_trade:
                    bn_exit_lvl = df.iloc[-1]
                    exit_price = ltp
                    pnl = (exit_price - entry_price) * lotsize
                    ongoing_trade = False
                    trade_status = '{} [Trade Status] Profit made: {} Ticker: {} Entry : {} Exit : {} Lotsize {} BN Entry: {} BN Exit: {} \n'.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'),pnl,option_ticker,entry_price,exit_price,lotsize,bn_entry_lvl['Close'],bn_exit_lvl['Close'])    
                    print(trade_status)
                    with open('tradebook.txt',mode='a+' ) as f:
                        f.write(trade_status)
                # SL hit
                if df.iloc[-1]['Close'] > bn_entry_lvl['Close'] + 50 and ongoing_trade:
                    bn_exit_lvl = df.iloc[-1]
                    exit_price = ltp
                    pnl = (exit_price - entry_price) * lotsize
                    ongoing_trade = False
                    trade_status = '{} [Trade Status] SL Hit: {} Ticker: {} Entry : {} Exit : {} Lotsize {} BN Entry Level {} BN Exit Level: {} \n'.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), pnl,option_ticker,entry_price,exit_price,lotsize,bn_entry_lvl['Close'],bn_exit_lvl['Close'])
                    print(trade_status)
                    with open('tradebook.txt',mode='a+' ) as f:
                        f.write(trade_status)

        #book profits
        # if df.iloc[-1]['Close'] > bn_entry_lvl['Close'] + 100 and ongoing_trade:
        #     bn_exit_lvl = df.iloc[-1]
        #     exit_price = ltp
        #     pnl = (exit_price - entry_price) * lotsize
        #     ongoing_trade = False
        #     trade_status = '{} [Trade Status] Profit made: {} Ticker: {} Entry : {} Exit : {} Lotsize {} BN Entry: {} BN Exit: {} \n'.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'),pnl,option_ticker,entry_price,exit_price,lotsize,bn_entry_lvl['Close'],bn_exit_lvl['Close'])
        #     print(trade_status)
        #     with open('tradebook.txt',mode='a+' ) as f:
        #         f.write(trade_status)
            
        # # SL hit
        # if df.iloc[-1]['Close'] < bn_entry_lvl['Close'] - 50 and ongoing_trade:
        #     bn_exit_lvl = df.iloc[-1]
        #     exit_price = ltp
        #     pnl = (exit_price - entry_price) * lotsize
        #     ongoing_trade = False
        #     trade_status = '{} [Trade Status] SL Hit: {} Ticker: {} Entry : {} Exit : {} Lotsize {} BN Entry Level {} BN Exit Level: {} \n'.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), pnl,option_ticker,entry_price,exit_price,lotsize,bn_entry_lvl['Close'],bn_exit_lvl['Close'])
        #     print(trade_status)
        #     with open('tradebook.txt',mode='a+' ) as f:
        #         f.write(trade_status)


def trade_decision(df,flvl,dt):
    global bn_entry_lvl
    # df = df.set_index('Datetime')
    # df_15 = df['Close'].resample('15min').ohlc()
    df_15 = process_yahoo_feed('15m')
    df_15 = df_15.reset_index()
    idx = df_15[df_15['Datetime'] == dt].index.values[0]
    curr_dt = dt.split(' ')[0]
    # curr_day = pytz.timezone('Asia/Kolkata').localize(datetime.strptime(dt,'%Y-%m-%d'))
    pdol, pdh, pdl, pdch = find_pd_extremes(df,curr_dt)
    # print('Previous day Lowest Open: {} Highest High: {} Lowest Low: {} and Highest Close: {}'.format(pdol, pdh, pdl, pdch))
    df = df[df['Datetime'] >= curr_dt]
    # print(df_15)
    # print(df_15.iloc[idx])
    price_diff = df_15.iloc[idx]['Close'] - df_15.iloc[idx]['Open']
    print("Opening Price diff [close - open]: " + str(price_diff))
    # check if there is 50 point diff in 1st candle
    level1382 = flvl['138.2%']
    level1618 = flvl['161.8%']
    leveln382 = flvl['-38.2%']
    leveln618 = flvl['-61.8%']
    
    bn_entry_lvl = df.iloc[-1]
    if (abs(price_diff) > 50):        
        if df.iloc[-1]['Close'] > df.iloc[-1]['sma26']:
            #close is higher than sma26 
            if df.iloc[-1]['Close'] > level1382 or df.iloc[-1]['Close'] > level1618:
                print(datetime.now(),' Buy CE option for: ',find_nearest_level(df.iloc[-1]['Close'],"CE"))
                # break
                return str(find_nearest_level(df.iloc[-1]['Close'],"CE")) + 'CE'
        else:
            # close is lower than sma26
            if df.iloc[-1]['Close'] < leveln382 or df.iloc[-1]['Close'] < leveln618:
                print(datetime.now(),' Buy PE option for: ',find_nearest_level(df.iloc[-1]['Close'],"PE"))
                # break
                return str(find_nearest_level(df.iloc[-1]['Close'],"PE")) + 'PE'
    else:
        # buy side prev day highs broken
        if df.iloc[-1]['Close'] > pdch or df.iloc[-1]['Close'] > pdh:
            print(datetime.now(),' Buy CE option for: ',find_nearest_level(df.iloc[-1]['Close'],"CE"))
            return str(find_nearest_level(df.iloc[-1]['Close'],"CE")) + 'CE'
        # sell side prev day lows broken
        elif df.iloc[-1]['Close'] < pdol or df.iloc[-1]['Close'] < pdl:
            print(datetime.now(),' Buy PE option for: ',find_nearest_level(df.iloc[-1]['Close'],"PE"))
            return str(find_nearest_level(df.iloc[-1]['Close'],"PE")) + 'PE'
        else:
            print(datetime.now(), ' No decisive trade signal!')
            bn_entry_lvl  = None
            return 0
    

decision = trade_decision(df_yahoo,fiblvl,dt_match_str)
option_ticker = decision
print(decision)
# trade_tracker(df_yahoo,bn_entry_lvl)

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
# obj = SmartConnect(api_key=conf_keys['apikey'])

# #login api call

# data = obj.generateSession(conf_keys['clientcode'],conf_keys['password'])
# refreshToken = data['data']['refreshToken']
# # print("\nRefresh token: ", refreshToken)

# token_data = obj.generateToken(refreshToken)

# feedToken = token_data['data']['feedToken']
# print("\nFeed token: ", feedToken)

# ltpRes = obj.ltpData('NFO','BANKNIFTY14JAN2131900CE','50699')
# print(ltpRes)

# BANKNIFTY07JAN2131900CE 10:41 189.0 BN 31843
# 06/01/2021 14:05:48 BANKNIFTY07JAN2131900CE 153.75

# entry_price = 189

def angelapi_login():
    angelapi = SmartConnect(api_key=conf_keys['apikey'])
    data = angelapi.generateSession(conf_keys['clientcode'],conf_keys['password'])
    refreshToken = data['data']['refreshToken']
    token_data = angelapi.generateToken(refreshToken)
    feedToken = token_data['data']['feedToken']

    return angelapi



def checkLTP(ticker,api):
    df = pd.read_json('./OpenAPIScripMaster.json')
    token = df[df['symbol']==ticker]['token'].values[0]
    exchange = df[df['symbol']==ticker]['exch_seg'].values[0]
    ltpRes = api.ltpData(exchange,ticker,token)
    # print(ltpRes)
    priceStr = datetime.now().strftime('%d/%m/%Y %H:%M:%S') +' > '+ ltpRes['data']['tradingsymbol'] +' = '+ str(ltpRes['data']['ltp']) +'\n'
    print(priceStr)
    with open('signals.txt',mode='a+' ) as f:
        f.write(priceStr)
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S') , ltpRes['data']['tradingsymbol'] , ltpRes['data']['ltp']

starttime = time.time()
time_interval = 5 * 60.0 # 5 minutes


# while True:
#     checkLTP('BANKNIFTY14JAN2132000PE',angelConnect)
#     time.sleep(time_interval - ((time.time() - starttime) % time_interval))

# angelConnect = angelapi_login()
if decision != 0 or decision is not None:
    angelConnect = angelapi_login()
    symbol = 'BANKNIFTY04FEB21'
    while True:
        decision = trade_decision(df_yahoo,fiblvl,dt_match_str)
        print(decision)
        if decision is not None:
            ts, ticker, ltp = checkLTP(symbol + decision, angelConnect)
            trade_tracker(process_yahoo_feed('5m'),ltp)
        time.sleep(time_interval - ((time.time() - starttime) % time_interval))
        # if datetime.now().time() > time(15,30):
        #     break
