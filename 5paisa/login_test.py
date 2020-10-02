from py5paisa import FivePaisaClient

client = FivePaisaClient(email="srvz39@gmail.com", passwd="202009215P!", dob="19900527")
client.login()

from websocket import create_connection
import json

five_paisa_ws = 'wss://websocket.5paisa.com/TTWebSocket/api/chat?Value1=57096845|2I1hEVxLCJP'
# ws = create_connection(five_paisa_ws)
# print "Sending 'Hello, World'..."
# ws.send("Hello, World")
# print "Sent"
# print "Receiving..."
# result =  ws.recv()
# print "Received '%s'" % result
# ws.close()

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