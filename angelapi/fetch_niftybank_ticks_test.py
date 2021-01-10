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

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
    'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
    'X-MACAddress': 'MAC_ADDRESS',
    'X-PrivateKey': 'API_KEY'
  }


#create object of call
obj = SmartConnect(api_key=conf_keys['apikey'])

#login api call

data = obj.generateSession(conf_keys['clientcode'],conf_keys['password'])
refreshToken = data['data']['refreshToken']
print("\nRefresh token: ", refreshToken)

token_data = obj.generateToken(refreshToken)

feedToken = token_data['data']['feedToken']
print("\nFeed token: ", feedToken)
# print("\nObject: ",tokens)

# print(data['feedToken'])
#fetch User Profile
# userProfile = obj.getProfile(refreshToken)
# print("\nUser : ", userProfile)s


FEED_TOKEN = feedToken #56825435
CLIENT_CODE = conf_keys['clientcode']
token = "channel you want the information of" #"nse_cm|2885&nse_cm|1594&nse_cm|11536"
token = "nse_cm|26009&nse_cm|48072" #banknifty
token = "nse_cm|26009&nse_fo|43010&nse_fo|43032&nse_fo|43038&nse_fo|43030&nse_fo|43031&nse_fo|43026&nse_fo|43025&nse_fo|43046&nse_fo|43035&nse_fo|43045&nse_fo|43040&nse_fo|43009&nse_fo|43039&nse_fo|43029&nse_fo|43008&nse_fo|43027&nse_fo|43028&nse_fo|43011"
# token = "nse_cm|2885&nse_cm|1594&nse_cm|11536"


df = pd.read_json('./OpenAPIScripMaster.json')
currentBankNifty = 31500
rangeLimit = 200
upperLimit = (currentBankNifty + rangeLimit) * 100
lowerLimit = (currentBankNifty - rangeLimit) * 100
# df1 = df[(df['name']=='BANKNIFTY') & (df['expiry'].str.contains('31DEC')) & (df['strike'] > 3050000) & (df['strike'] < 3150000)]
df1 = df[(df['name']=='BANKNIFTY') & (df['expiry'].str.contains('7JAN')) & (df['strike'] >= lowerLimit) & (df['strike'] <= upperLimit)]
print(df1)

token_string = "nse_cm|26009" #banknifty
# for t in df1['token']:
#     # print(t)
#     token_string = token_string + '&nse_fo|' + t

print(token_string)
token = token_string

ss = WebSocket(FEED_TOKEN, CLIENT_CODE)

# with open('ticks.json', mode='w', encoding='utf-8') as f:
#     # json.dump([],f)
#     pass
# with open('live_ticks.txt', mode='w') as f:
#     f.write("")

def on_tick(ws, tick):
    # with open('ticks1.json', mode='r', encoding='utf-8') as f:
    #     prevticks = json.load(f)
    # with open('ticks.json', mode='w', encoding='utf-8') as f:
    #     prevticks.append(tick)
    #     json.dump(prevticks, f)
    # # with open('ticks.json', mode='a+', encoding='utf-8') as f:
    # #     json.dump(tick, f)

    with open('live_ticks.txt',mode='a+',encoding='utf-8') as f:
        try:
            print(tick[0]['tvalue'],tick[1]['ltp'])
            f.write(tick[0]['tvalue'] +" > "+df[df['token'] == tick[1]['tk']]['symbol'].values[0]+" = "+ tick[1]['ltp'] + "\n")
        except:
            pass
    # with open('test_dump.txt',mode='a+',encoding='utf-8') as f:
    #     json.dump(tick, f)
    print(tick)
        
    # print("Ticks: {}".format(tick))

def on_connect(ws, response):
    ws.send_request(token)
    # a = ws.send_request(token)
    # print("Back to Function", a)

def on_close(ws, code, reason):
    # with open('live_ticks.txt',mode='r',encoding='utf-8') as f:
    #     live_ticks = f.readlines()
    # with open('historical_ticks', mode='w') as f:
    #     f.writelines(live_ticks)
    ws.stop()

# Assign the callbacks.
ss.on_ticks = on_tick
ss.on_connect = on_connect
ss.on_close = on_close
ss.connect()

# ltp_data = obj.ltpData('NSE','SBIN-EQ',"3045")``
# print(ltp_data)