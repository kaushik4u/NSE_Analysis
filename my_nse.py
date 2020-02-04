import requests
import json
import time
import pandas as pd
from bs4 import BeautifulSoup
import zipfile
import sqlite3
import glob
import os
import random

proxyDict = {
    "http": 'http://proxy.intra.bt.com:8080',
    "https": 'http://proxy.intra.bt.com:8080',
}

user_agent_list = [
    #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

# Opens file if exists, else creates file
connex = sqlite3.connect("./data/nse_data.db")
# This object lets us actually send messages to our DB and receive results
cur = connex.cursor()

def import_web(ticker,proxy):
    url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=' + \
    	ticker+'&illiquid=0&smeFlag=0&itpFlag=0'
    user_agent = random.choice(user_agent_list)
    if proxy:
        req = requests.get(url, headers={'User-Agent': user_agent}, proxies=proxyDict)
    else:
        req = requests.get(url, headers={'User-Agent': user_agent})
    print(req.content)


years2 = 'https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=SBIN&segmentLink=3&symbolCount=1&series=EQ&dateRange=24month&fromDate=&toDate=&dataType=PRICEVOLUME'
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
    
    # df = df.set_index([1])    
    print(df)
    
    df.to_json('temp.json', orient='records')
    return df

# import_web('TCS')

def fetch_bhavcopy(datestring,proxy):
    bhavurl = 'http://www.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date=' + datestring + '&section=EQ'
    baseurl = 'http://www.nseindia.com'
    if proxy:    
        req = requests.get(bhavurl, headers={'User-Agent': "Chrome Browser"}, proxies=proxyDict)
    else:
        req = requests.get(bhavurl, headers={'User-Agent': "Chrome Browser"})
    print(bhavurl)
    soup = BeautifulSoup(req.text, 'html.parser')
    print(soup)
    link = soup.find('a')
    if link != None:
        print('fetching...'+baseurl+link.get('href'))
        fileurl = baseurl + link.get('href')
        if proxy:    
            req = requests.get(fileurl, headers={'User-Agent': "Chrome Browser"}, proxies=proxyDict)
        else:
            req = requests.get(fileurl, headers={'User-Agent': "Chrome Browser"})
        with open('./data/temp/temp.zip', 'wb') as f:
            f.write(req.content)
            with zipfile.ZipFile('./data/temp/temp.zip', 'r') as zip_ref:
                zip_ref.extractall('./data/temp/')
        
    else:
        print('No data found!')


def merge_csv():
    pass

def load_to_db(connection):
    csvDir = './data/temp'
    for file in os.listdir(csvDir):
        if file.endswith(".csv"):
            # print(os.Dir.join(csvDir, file))
            # print(csvDir +'/'+ file)
            csvFile = csvDir + '/' + file
            print('loading...' + file)
            for chunk in pd.read_csv(csvFile, chunksize=4):
                chunk['TIMESTAMP'] = pd.to_datetime(chunk['TIMESTAMP']).dt.date
                chunk = chunk.loc[:, ~chunk.columns.str.contains('^Unnamed')]
                chunk.to_sql(name="EOD_data", con=connection, if_exists="append", index=False)  #"name" is name of table 
                print(chunk.iloc[0])

data = get_3months('SBIN',1)
startDate = '01-01-2015' # mm-dd-yyyy
endDate = '01-02-2015'  # mm-dd-yyyy
dateRange = [d.strftime('%d-%m-%Y') for d in pd.date_range(startDate, endDate)]
# print(dateRange)
# for d in dateRange:
#     fetch_bhavcopy(d,0)

# load_to_db(connex)
