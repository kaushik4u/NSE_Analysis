import requests
import json
import time
import pandas as pd
from bs4 import BeautifulSoup

proxyDict = {
    "http": 'http://proxy.intra.bt.com:8080',
    "https": 'http://proxy.intra.bt.com:8080',
}

def import_web(ticker,proxy):
    url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=' + \
    	ticker+'&illiquid=0&smeFlag=0&itpFlag=0'
    if proxy:    
        req = requests.get(url, headers={'User-Agent': "Chrome Browser"}, proxies=proxyDict)
    else:
        req = requests.get(url, headers={'User-Agent': "Chrome Browser"})
    print(req.content)


def get_3months(ticker, proxy):
    url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol='+ticker+'&series=EQ&fromDate=undefined&toDate=undefined&datePeriod=3months'
    if proxy:    
        req = requests.get(url, headers={'User-Agent': "Chrome Browser"}, proxies=proxyDict)
    else:
        req = requests.get(url, headers={'User-Agent': "Chrome Browser"})
    soup = BeautifulSoup(req.text, "html.parser")
    # df = pd.read_csv(soup.find("div", {"id": "csvContentDiv"}).getText())
    # print(soup.find("div", {"id": "csvContentDiv"}).getText())
    # print(req.text)
    drawing_list = []
    # temp = []
    for tr in soup.select("table tr"):
        cells = tr.findAll('th')
        temp = []
        if len(cells) > 0:
            for c in cells:
                numbers = c.getText()
                temp.append(numbers)
            drawing_list.append(temp)
        cells = tr.findAll('td')  
        temp = []
        if len(cells)>0:            
            for c in cells:
                numbers = c.getText()
                temp.append(numbers)
            drawing_list.append(temp)  
            # print(drawing_list)
        
        
            # print(temp[0])
        df = pd.DataFrame(drawing_list)
        new_header = df.iloc[0]  # grab the first row for the header
        df = df[1:]  # take the data less the header row
        df.columns = new_header  # set the header row as the df header     
        
    print(df)

# import_web('TCS')

get_3months('INFY',1)
