import pandas as pd
import nsepy as nse
import json
from datetime import datetime, timedelta
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect

nifty500list = pd.read_csv('./ind_nifty500list.csv')
# print(nifty500list.head(5))

with open('./conf.json') as f:
    conf_keys = json.load(f)

login_payload = {
    "clientcode": conf_keys['clientcode'],
    "password": conf_keys['password']
}

def angelapi_login():
    angelapi = SmartConnect(api_key=conf_keys['apikey'])
    data = angelapi.generateSession(conf_keys['clientcode'],conf_keys['password'])
    refreshToken = data['data']['refreshToken']
    token_data = angelapi.generateToken(refreshToken)
    feedToken = token_data['data']['feedToken']

    return angelapi

def checkLTP(ticker,api):
    df = pd.read_json('../angelapi/OpenAPIScripMaster.json')

    print(df[df['symbol']==ticker])
    token = df[df['symbol']==ticker]['token'].values[0]
    exchange = df[df['symbol']==ticker]['exch_seg'].values[0]
    ltpRes = api.ltpData(exchange,ticker,token)
    # print(ltpRes)
    priceStr = datetime.now().strftime('%d/%m/%Y %H:%M:%S') +' > '+ ltpRes['data']['tradingsymbol'] +' = '+ str(ltpRes['data']['ltp']) +'\n'
    print(priceStr)
    with open('signals.txt',mode='a+' ) as f:
        f.write(priceStr)
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S') , ltpRes['data']['tradingsymbol'] , ltpRes['data']['ltp']

tickers = ['KRBL']

angelConnect = angelapi_login()

ts, ticker, ltp = checkLTP(tickers[0], angelConnect)
# df = pd.read_json('../angelapi/OpenAPIScripMaster.json')
# print(df[df['symbol']==tickers[0]])