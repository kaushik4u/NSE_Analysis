import requests
import json
from datetime import datetime as dt

with open('5paisa_api_config.json') as f:
    keys = json.load(f)

api_session = requests.Session()

def get_scripcode(symbol):
    with open('5paisa_scripcodes.json') as f:
        scrip_codes = json.load(f)
    for i in range(len(scrip_codes['data'])):
        if scrip_codes['data'][i]['SYMBOL'] == symbol:
            return scrip_codes['data'][i]['SCRIP_CODE']


def api_login(session):
    headers = {
        'authority': 'www.5paisa.com',
        'accept': '*/*',
        'dnt': '1',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.5paisa.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.5paisa.com/',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': '_gcl_au=1.1.1694663341.1600523099; utm_campaign_cookie_eaccount=; _fbp=fb.1.1600523099995.498828509; utm_campaign_cookie=; PIData=U09VUkFW; WZRK_G=92feefdd4fa24231a498161f481a5600; source=www.google.com|mail.google.com|mail.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|github.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com; _ga_0ZW7K75KJP=GS1.1.1603524384.36.0.1603524384.0; gclid=undefined; _ga=GA1.2.1280417679.1600523099; _gid=GA1.2.575694897.1606587289; __RequestVerificationToken=HiYhpm6ej1orEweQHTGJHK6eQicw-xNHxfIIclBbmsMltcXzGPiup5In3AcYvSBuidbf0G9buqYG4bKFzAqm7d0qzxA1; RClient=; 5paisacookie=yoo1vf4kavgmedlzyot4zrtz; WZRK_S_675-RZ7-6Z5Z=%7B%22p%22%3A2%2C%22s%22%3A1606717821%2C%22t%22%3A1606718904%7D; ASP.NET_SessionId=j40ph2dnycbx2kghyev3gvnd; WZRK_S_R74-5R4-6W5Z=%7B%22p%22%3A11%2C%22s%22%3A1606717796%2C%22t%22%3A1606719087%7D',
    }

    data = {
    'Email': keys['email']   
    }

    s = session
    response = s.get('https://www.5paisa.com/Home/')
    # print(response.text.encode('utf8'))
    print(s.cookies.get_dict())

    # header is not required here to capture the verification cookie
    # response = s.post('https://www.5paisa.com/Home/VerifyEmailStatus', headers=headers, data=data)
    response = s.post('https://www.5paisa.com/home/checkclient', data=data)    
    print(response.text.encode('utf8'))
    print(s.cookies.get_dict())

    data = {
    'login.UserName': keys['UserName'],
    'login.ClientCode': '',
    'login.Password': keys['Password'],
    'login.DOB': keys['DOB']
    }

    # data = {
    # 'login.UserName': 'srvz39@gmail.com',
    # 'login.ClientCode': '',
    # 'login.Password': '091220205p!',
    # 'login.DOB': '27051990'
    # }
    
    # header is required here
    response = s.post('https://www.5paisa.com/Home/Login', headers=headers, data=data)
    print(response.text.encode('utf8'))
    print(s.cookies.get_dict())
    if response.ok:
        print('Logged in successfully!')
    else:
        print('Couldn\'t log in, something is wrong.')
    return s

def fetch_data(session,symbol,date):
    s = session
    # headers = {
    #     'authority': 'www.5paisa.com',
    #     'accept': '*/*',
    #     'dnt': '1',
    #     'x-requested-with': 'XMLHttpRequest',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    #     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #     'origin': 'https://www.5paisa.com',
    #     'sec-fetch-site': 'same-origin',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-dest': 'empty',
    #     'referer': 'https://www.5paisa.com/',
    #     'accept-language': 'en-US,en;q=0.9',
    # }

    # data = {
    # 'Email': keys['email']   
    # }

    # s = requests.Session()
    # response = s.post('https://www.5paisa.com/Home/VerifyEmailStatus', headers=headers, data=data)
    # print(response.text.encode('utf8'))
    # print(s.cookies)

    # data = {
    # 'login.UserName': keys['UserName'],
    # 'login.ClientCode': '',
    # 'login.Password': keys['Password'],
    # 'login.DOB': keys['DOB']
    # }

    # response = s.post('https://www.5paisa.com/Home/Login', data=data)
    # print(response.text.encode('utf8'))
    # print(s.cookies)

    # symbol = symbol
    scrip_code = get_scripcode(symbol)



    response = s.get('https://trade.5paisa.com/trade/home')
    print(response)

    quote_headers = {
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
    if date == None:
        quote_payload = '{"Exch":"N","ExchType":"C","ScripCode":"'+ scrip_code +'","LastRequestTime":"1TODAY"}'
        quote_url = 'https://trade.5paisa.com/Trade/Chart/FetchQuoteData'
        save_loc='temp.txt'
    else:
        quote_payload = '{"Exch":"N","ExchType":"C","ScripCode":"'+ scrip_code +'","LastRequestTime":"'+ date +'"}'
        quote_url = 'https://trade.5paisa.com/Trade/Chart/FetchHistoricalDayDataforIntra'
        save_loc='prev_day_temp.txt'
    # response = s.post('https://trade.5paisa.com/Trade/Chart/FetchQuoteData', headers=headers, cookies=cookies, data=data)
    # response = s.post('https://trade.5paisa.com/Trade/Chart/FetchQuoteData', headers=quote_headers, data=quote_payload)
    response = s.post(quote_url, headers=quote_headers, data=quote_payload)
    # print(response)
    if response.ok:
        print(symbol + ' data fetched successfully!')
    else:
        print(symbol + ' data couldn\'t be fetched, something is wrong.')
    json_data = response.json()
    # print(json_data)

    # with open("temp.txt", "w") as outfile:
    #     outfile.write(json_data)
    with open(save_loc, 'w') as f:
        # for item in json_data:
        #     f.write("%s\n" % item)
        json.dump(json_data, f, ensure_ascii=False, separators=(',', ':'))

def dateserialnumber(datestring):
    d = dt.strptime(datestring,"%Y%m%d")
    temp = dt(1970, 1, 1)    # Note, not 31st Dec but 30th!
    delta = d - temp
    print(int(delta.days))
    return int(delta.days)

def fetch_banknifty_option_data(session,expiry):
    
    date_serial = dateserialnumber(expiry)
    quote_headers = {
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
        'referer': 'https://trade.5paisa.com/trade/home',
        'accept-language': 'en-US,en;q=0.9',
    }
    
    # payload example
    # quote_payload = "{ 'Exch': 'N','Symbol': 'BANKNIFTY','Expiry':'18620','ExchType':'D' }"
    quote_payload = '{"Exch": "N","Symbol": "BANKNIFTY","Expiry":'+ str(date_serial) +',"ExchType":"D"}'
    quote_url = 'https://trade.5paisa.com/Trade/Home/FetchStrikeRate'
    response = session.post(quote_url, headers=quote_headers, data=quote_payload)

    if response.ok:
        print('BANKNIFTY option data fetched successfully!')
    else:
        print('BANKNIFTY option data couldn\'t be fetched, something is wrong.')
    json_data = response.json()
    print(response)
    with open('bankniftyoption.txt', 'w') as f:
        # for item in json_data:
        #     f.write("%s\n" % item)
        json.dump(json_data, f, ensure_ascii=False, separators=(',', ':'))


s = api_login(api_session)

# fetch_data(s,'BANK NIFTY','20201101')
fetch_data(s,'BANK NIFTY',None)


fetch_banknifty_option_data(s,'20201231')







