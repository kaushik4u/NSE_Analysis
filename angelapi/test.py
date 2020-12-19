import requests
import json
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
token = "nse_cm|26009" #banknifty
# token = "nse_cm|2885&nse_cm|1594&nse_cm|11536"
ss = WebSocket(FEED_TOKEN, CLIENT_CODE)

with open('ticks.json', mode='w', encoding='utf-8') as f:
    json.dump([],f)

def on_tick(ws, tick):
    with open('ticks.json', mode='r', encoding='utf-8') as f:
        prevticks = json.load(f)
    with open('ticks.json', mode='w', encoding='utf-8') as f:
        prevticks.append(tick)
        json.dump(prevticks, f)
    # with open('ticks.json', mode='a+', encoding='utf-8') as f:
    #     json.dump(tick, f)
    print("Ticks: {}".format(tick))

def on_connect(ws, response):
    ws.send_request(token)
    # a = ws.send_request(token)
    # print("Back to Function", a)

def on_close(ws, code, reason):
    ws.stop()

# Assign the callbacks.
ss.on_ticks = on_tick
ss.on_connect = on_connect
ss.on_close = on_close
ss.connect()

# ltp_data = obj.ltpData('NSE','SBIN-EQ',"3045")
# print(ltp_data)