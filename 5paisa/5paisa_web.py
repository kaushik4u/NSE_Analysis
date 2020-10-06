import requests

headers = {
    'authority': 'www.5paisa.com',
    'accept': '*/*',
    'dnt': '1',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.5paisa.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.5paisa.com/',
    'accept-language': 'en-US,en;q=0.9',
}

data = {
  'Email': 'srvz39@gmail.com'   
}

s = requests.Session()
response = s.post('https://www.5paisa.com/Home/VerifyEmailStatus', headers=headers, data=data)
print(response.text.encode('utf8'))
print(s.cookies)


headers = {
    'authority': 'www.5paisa.com',
    'accept': '*/*',
    'dnt': '1',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.5paisa.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.5paisa.com/',
    'accept-language': 'en-US,en;q=0.9',
}

headers = {
    'authority': 'www.5paisa.com',
    'accept': '*/*',
    'dnt': '1',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.5paisa.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.5paisa.com/',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_gcl_au=1.1.1694663341.1600523099; utm_campaign_cookie_eaccount=; _fbp=fb.1.1600523099995.498828509; utm_campaign_cookie=; PIData=U09VUkFW; WZRK_G=92feefdd4fa24231a498161f481a5600; _gid=GA1.2.1985002571.1601579442; source=www.google.com|mail.google.com|mail.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|github.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com; LandingPage=/landing/algo-trading; 5paisacookie=1tdsinkispti5xleuh3elrob; ASP.NET_SessionId=akwi3zsz2vljsrxgr3tp0c5u; _ga_0ZW7K75KJP=GS1.1.1601651063.30.1.1601651986.0; AF_BANNERS_SESSION_ID=1601651986522; _ga=GA1.2.1280417679.1600523099',
}

data = {
  'login.UserName': 'srvz39@gmail.com',
  'login.ClientCode': '',
  'login.Password': '290920205P!',
  'login.DOB': '27051990'
}

response = s.post('https://www.5paisa.com/Home/Login', data=data)
print(response.text.encode('utf8'))
print(s.cookies)


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



# ws_request={ 
#     "Method":"MarketFeedV3",
#     "Operation":"Subscribe",
#     "ClientCode":"2I1hEVxLCJP",
#     "MarketFeedData":[ 
#     { 
#     "Exch":"N",
#     "ExchType":"C",
#     "ScripCode":scrip_code
#     }
#     ]
# }

# ws = create_connection(five_paisa_ws)
# print('Sending ws payload...')
# ws.send(ws_request)
# print('Receiving...')
# result =  ws.recv()
# print(result)
# ws.close()

""" 
cookies = {
    '_gcl_au': '1.1.1694663341.1600523099',
    '_fbp': 'fb.1.1600523099995.498828509',
    'PIData': 'U09VUkFW',
    'WZRK_G': '92feefdd4fa24231a498161f481a5600',
    '_gid': 'GA1.2.740914364.1601270863',
    'utm_campaign_cookie_eaccount': '',
    'ASP.NET_SessionId': 'zgofzolzswb401wjbgs3aokd',
    '__RequestVerificationToken_L1RyYWRl0': 'yX1njCtoIKgI9YHqvkBPleI1jsC9naA2LyDCUxyZzWomgofeJuwO1R65rnPenymG8eGeZySB83sZWpbjLOYpg5aNTkM1',
    'NSC_usbef.5qbjtb.dpn_443': 'ffffffffaf103e4045525d5f4f58455e445a4a423660',
    'RMSMargin': '',
    'OrderDataForRMS': '',
    'SmartOrderType': '',
    'haptik-sdk-user-info-bebc46427b51a56e62d60b843c62742c6a7e82a5': 'XIFCMfdFJGQdvvaJDMiaHvGG99DMDb10tbnFO6QmeaU=|78075694dd90bce9c1a619612c15e24a9dfd3b4d|ssl://mqtt.haptik.me|GMATvgDr|mqtt|443',
    'WZRK_S_675-RZ7-6Z5Z': '%7B%22p%22%3A1%2C%22s%22%3A1601366137%2C%22t%22%3A1601366258%7D',
    '5paisacookie': 'vzbl0glbnipa2fxlr3tgbbd3',
    '.ASPXAUTH': 'FB5C1B8EB8ADCE4793CC4A07B5D61D01B1C57B89FCCBAB1C836DCAF16C039E755C28DE3AA5B252DBBBF728D221B709A25912806FCE30D4C6C0DC1C02C30639C4E4AB192C4FACB560A3C2561679958F1E57B3624FA1E038D2687263DB2E9C73E26F1536A9A97CF55340416DC891D87E823F0E402BD5F10C59E17DE0BB25F601EDEE2EE816C939EC481663970BE1C6EED0994D9FE679F2004A128E573E68B5BEE7F030BAA928074D5B94393C3AD999223EF2D722B75A8D7737109030EC74EA0502B9E0309F69EF617490483B641B18F9D167A1EE3E201C9ABEFE5BD011AA12C49F4D04A8DA0BDCC6E6D2CEFA32CD021EEF19BD510E',
    '_ga_0ZW7K75KJP': 'GS1.1.1601363670.23.1.1601367088.0',
    '_ga': 'GA1.2.1280417679.1600523099',
}


headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'DNT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://trade.5paisa.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://trade.5paisa.com/trade/home',
    'Accept-Language': 'en-US,en;q=0.9',
}

cookies = {
    '_gcl_au': '1.1.1694663341.1600523099',
    '_fbp': 'fb.1.1600523099995.498828509',
    'PIData': 'U09VUkFW',
    'WZRK_G': '92feefdd4fa24231a498161f481a5600',
    'utm_campaign_cookie_eaccount': '',
    '_gid': 'GA1.2.1985002571.1601579442',
    '5paisacookie': 'mu4rgivergytgzuanvw53u55',
    'ASP.NET_SessionId': 'dpuadp3hvtxvn0y5h2ljnkoc',
    '.ASPXAUTH': '7791D07E1F7567258F57C3FD719EFA8599DE45A13643B01B612CCB507C8A6187741AF3DFFD6C481E410895AE7137CE7DC09FF0A3645E7CD44B896C85F8D12950F51F22883E88A22968132129B693B31A4C59246A',
    '__RequestVerificationToken_L1RyYWRl0': 'xW4EyKYXEmJRZ6_mnxOyBmOC12etyxfLDYibovUL6F7h0FTiJHE99wPLPPSEMmyPcoxvBMs3Z8WPZWXogVliz1UN31M1',
    'NSC_usbef.5qbjtb.dpn_443': 'ffffffffaf103e0545525d5f4f58455e445a4a423660',
    'RMSMargin': '',
    'OrderDataForRMS': '',
    'SmartOrderType': '',
    'haptik-sdk-user-info-bebc46427b51a56e62d60b843c62742c6a7e82a5': 'I6DkX84crpvjkjRFzc7PyAtzDXer_aGjU6s-rZap_cI=|78075694dd90bce9c1a619612c15e24a9dfd3b4d|ssl://mqtt.haptik.me|GMATvgDr|mqtt|443',
    'WZRK_S_675-RZ7-6Z5Z': '%7B%22p%22%3A1%2C%22s%22%3A1601652261%2C%22t%22%3A1601652261%7D',
    '_ga': 'GA1.1.1280417679.1600523099',
    '_ga_0ZW7K75KJP': 'GS1.1.1601651063.30.1.1601652278.0',
}
 """
symbol = 'SBIN'
scrip_code = get_scripcode(symbol)

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'DNT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Origin': 'https://trade.5paisa.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    # 'Referer': 'https://trade.5paisa.com/Trade/chart/GetChart1?Exch=N&ExchType=C&ScripCode=8828&ScripName=GAEL&Period=1TODAY&Display=false',
    'Referer': 'https://trade.5paisa.com/Trade/chart/GetChart1?Exch=N&ExchType=C&ScripCode='+ scrip_code +'&ScripName='+ symbol +'&Period=1TODAY&Display=false',
    'Accept-Language': 'en-US,en;q=0.9',
}


data = '{"Exch":"N","ExchType":"C","ScripCode":"8828","LastRequestTime":"1TODAY"}'

data = '{"Exch":"N","ExchType":"C","ScripCode":"'+ scrip_code +'","LastRequestTime":"1TODAY"}'

response = s.get('https://trade.5paisa.com/trade/home')
print(response)

# response = s.post('https://trade.5paisa.com/Trade/Chart/FetchQuoteData', headers=headers, cookies=cookies, data=data)
response = s.post('https://trade.5paisa.com/Trade/Chart/FetchQuoteData', headers=headers, data=data)
print(response)
json_data = response.json()
# print(json_data)

# with open("temp.txt", "w") as outfile:
#     outfile.write(json_data)

with open('temp.txt', 'w') as f:
    # for item in json_data:
    #     f.write("%s\n" % item)
    json.dump(json_data, f, ensure_ascii=False, separators=(',', ':'))
    # f.write(json_data)

