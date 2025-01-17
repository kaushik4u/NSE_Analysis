import requests

url = 'https://openfeed.5paisa.com/Feeds/api/UserActivity/LoginCheck'
# url = 'https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/LoginRequestMobileNewbyEmail'

myobj = {
"head": {
    "appName": "5P57096845",
    "appVer": "1.0",
    "key": "jSyWtc8LngGhP7J3445IRCUVY0OmQVBXxb0oKSHAkCvcSXwaQcOLaOPzVfC8m5BI",
    "osName": "Web",
    "requestCode":"5PLoginCheck"
},
"body": {
    "userId" : "2I1hEVxLCJP",
    "password": "m7QAt8H8cpm"
}
}

myobj2 = {
    "head": {
        "appName": "5P57096845",
        "appVer": "1.0",
        "key": "jSyWtc8LngGhP7J3445IRCUVY0OmQVBXxb0oKSHAkCvcSXwaQcOLaOPzVfC8m5BI",
        "osName": "WEB",
        "requestCode": "5PLoginV2",
        "userId": "2I1hEVxLCJP",
        "password": "m7QAt8H8cpm"
    },
    "body": {
        "Email_id": "i1P2KqXk0ckrR2j4OLmRcGOi/T5ksoUfPeSFtWaFGSY=",
        "Password": "5A52Cs/Ezgj3JRFRAmSKtw==",
        "LocalIP": "",
        "PublicIP": "",
        "HDSerailNumber": "",
        "MACAddress": "",
        "MachineID": "",
        "VersionNo": "1.7",
        "RequestNo": "1",
        "My2PIN": "RZytAuACqtMyjsyVJf8UPg==",
        "ConnectionType": "1"
    }
}

header ={
    "appName": "5P57096845",
    "appVer": "1.0",
    "key": "jSyWtc8LngGhP7J3445IRCUVY0OmQVBXxb0oKSHAkCvcSXwaQcOLaOPzVfC8m5BI",
    "osName": "Web",
    "requestCode":"5PLoginCheck"
}

data ={
    "userId" : "2I1hEVxLCJP",
    "password": "m7QAt8H8cpm"
}
s = requests.Session()
x = s.post(url, headers= header, data = data)

print(x.text)

# wss://websocket.5paisa.com/TTWebSocket/api/chat?Value1=<<Pass ClientCode>>|<<Pass RegistrationID>>
# wss://websocket.5paisa.com/TTWebSocket/api/chat?Value1=|<<Pass RegistrationID>>


#!/usr/bin/python

from websocket import create_connection
import json

five_paisa_ws = 'wss://websocket.5paisa.com/TTWebSocket/api/chat?Value1=57096845|2I1hEVxLCJP'

def get_scripcode(symbol):
    with open('5paisa_scripcodes.json') as f:
        scrip_codes = json.load(f)
    for i in range(len(scrip_codes['data'])):
        if scrip_codes['data'][i]['SYMBOL'] == symbol:
            return scrip_codes['data'][i]['SCRIP_CODE']
     
    # print(scrip_codes['data'][0]['SYMBOL'])

# print(scrip_code)

scrip_code = get_scripcode('TATAMOTORS')

ws_request={ 
    "Method":"MarketFeedV3",
    "Operation":"Subscribe",
    "ClientCode":"2I1hEVxLCJP",
    "MarketFeedData":[ 
    { 
    "Exch":"N",
    "ExchType":"C",
    "ScripCode":scrip_code
    }
    ]
}

ws = create_connection(five_paisa_ws)
print('Sending ws payload...')
ws.send(ws_request)
print('Receiving...')
result =  ws.recv()
print(result)
ws.close()
