from datetime import datetime
import pandas as pd
import requests
import smartapi
scrip_codes_url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

df = pd.read_json('./OpenAPIScripMaster.json')
currentBankNifty = 31800
rangeLimit = 200
upperLimit = (currentBankNifty + rangeLimit) * 100
lowerLimit = (currentBankNifty - rangeLimit) * 100
# df1 = df[(df['name']=='BANKNIFTY') & (df['expiry'].str.contains('31DEC')) & (df['strike'] > 3050000) & (df['strike'] < 3150000)]
df1 = df[(df['name']=='BANKNIFTY') & (df['expiry'].str.contains('7JAN')) & (df['strike'] >= lowerLimit) & (df['strike'] <= upperLimit)]
print(df[df['symbol']=='BANKNIFTY14JAN2132300CE']['token'].values[0])
print(df1)
print(df1['token'])
print(len(df1['token']))
print(df[df['token'] == '26009']['symbol'].values[0])
token_string = "nse_cm|26009" #banknifty
for t in df1['token']:
    # print(t)
    token_string = token_string + '&nse_fo|' + t

print(token_string)

import requests
import json
import pandas as pd
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
# from smartapi import SmartSocket #or from smartapi.smartSocket import SmartSocket
from smartapi import WebSocket

with open('./conf.json') as f:
    conf_keys = json.load(f)
    # print(d)

# conf_keys = json.load("./conf.json")
print(conf_keys['clientcode'])
s = requests.Session()

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
print("\nRefresh token: ", refreshToken)

token_data = obj.generateToken(refreshToken)

feedToken = token_data['data']['feedToken']
print("\nFeed token: ", feedToken)

ltpRes = obj.ltpData('NFO','BANKNIFTY07JAN2131600PE','43108')
print(datetime.now().strftime('%d/%m/%Y %H:%M:%S') +' '+ ltpRes['data']['tradingsymbol'] +' '+ str(ltpRes['data']['ltp']))

# 06/01/2021 14:25:17 BANKNIFTY07JAN2131800CE 190.0
# 06/01/2021 14:34:54 BANKNIFTY07JAN2131600PE 159.1
# 06/01/2021 14:59:05 BANKNIFTY07JAN2131600PE 83.75