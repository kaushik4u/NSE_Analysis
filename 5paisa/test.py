import requests

url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/LoginRequestMobileNewbyEmail"

payload = "{\n    \"head\": {\n        \"appName\": \"5P57096845\",\n        \"appVer\": \"1.0\",\n        \"key\": \"5DlbyuEfaCZFnJ7fabIkqLqT5LJoGDXV\",\n        \"osName\": \"WEB\",\n        \"requestCode\": \"5PLoginV2\",\n        \"userId\": \"2I1hEVxLCJP\",\n        \"password\": \"m7QAt8H8cpm\"\n    },\n    \"body\": {\n        \"Email_id\": \"i1P2KqXk0ckrR2j4OLmRcGOi/T5ksoUfPeSFtWaFGSY=\",\n        \"Password\": \"5A52Cs/Ezgj3JRFRAmSKtw==\",\n        \"LocalIP\": \"\",\n        \"PublicIP\": \"\",\n        \"HDSerailNumber\": \"\",\n        \"MACAddress\": \"\",\n        \"MachineID\": \"BM4653-D-039377.local.indiainfoline.com\",\n        \"VersionNo\": \"1.7\",\n        \"RequestNo\": \"1\",\n        \"My2PIN\": \"RZytAuACqtMyjsyVJf8UPg==\",\n        \"ConnectionType\": \"1\"\n    }\n}"
headers = {
  'Content-Type': 'application/json',
#   'Cookie': '5paisacookie=sgyr05bsfzevuh01rbwm0avk'
}

s = requests.Session()
response = s.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
print(s.cookies)

# data = {"Exch":"N","ExchType":"C","ScripCode":"317","LastRequestTime":"1TODAY"}
payload = "{\"Exch\":\"N\",\"ExchType\":\"C\",\"ScripCode\":\"317\",\"LastRequestTime\":\"1TODAY\"}"
payload = {
    "Exch":"N",
    "ExchType":"C",
    "ScripCode":"317",
    "LastRequestTime":"1TODAY"
}

response = s.post('https://trade.5paisa.com/Trade/Chart/FetchQuoteData', headers=headers, data = payload)

print(response.text)


from websocket import create_connection
import websocket
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

ws_cookie = '.ASPXAUTH=C25C3197D6D34AB39207C56B5AF91E309878FE60E95435E4C533DD51A802CDB6BDB3375F2C9D0AF9F24E48A644B5DBAA3FE1F258618F6D927112BF1F1824ABD419951AD6B51869135D6F3189777341160BA7FDCE3F58C4BA4B66CB82C2C8E88A791086ECC9B674628908A130A927F3C65B180B49BBF15D17CAFCBD8676B6013DFAA41C082A73EBB1ED6AC4A71EE3171C3B3E3AD16A719EC231BCDAB1E255891A8CFCD00B00DCA0A02EAF7824C470C1D25CF39CE22A7AB896C74982957D16C5E94F712F9E649021B17F1C28348903C244D4D61AB37FAC33D0DB0F23185631AFAC31FF26742924BBC706F8DD72F9C4E584140D3F4C; Path=/; Domain=.5paisa.com; Secure; HttpOnly;'

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
headers = {
    'Pragma': 'no-cache',
    'Origin': 'chrome-extension://fgponpodhbmadfljofbimhhlengambbn',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-WebSocket-Key': '8O6o8YiAVHK2BsSoOGmcvg==',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Upgrade': 'websocket',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    'Sec-WebSocket-Version': '13',
}

# ws = websocket.WebSocketApp(five_paisa_ws,
#                         header=headers,
#                         cookie=ws_cookie)

# # ws = create_connection(five_paisa_ws)
# print('Sending ws payload...')
# ws.send(ws_request)
# print('Receiving...')
# result =  ws.recv()
# print(result)
# ws.close()

# import requests



params = (
    ('Value1', '57096845|2I1hEVxLCJP'),
)

# response = s.get('http://wss://websocket.5paisa.com/TTWebSocket/api/chat', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = s.get('http://wss://websocket.5paisa.com/TTWebSocket/api/chat?Value1=57096845|2I1hEVxLCJP', headers=headers)

# print(response.text)