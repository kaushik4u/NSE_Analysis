import requests
import schedule
import time


nse_url = 'https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxFOGetQuoteJSON.jsp?underlying=BANKNIFTY&instrument=FUTIDX&expiry=30JUL2020&type=SELECT&strike=SELECT'

def fetch_nse(url):
    print(time.ctime(time.time()) +' :fetching data...')
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referer': 'https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying=BANKNIFTY&instrument=FUTIDX&expiry=30JUL2020&type=-&strike=-',
        
    }
    response = requests.get(url, headers=headers)
    print(response.text)



fetch_nse(nse_url)