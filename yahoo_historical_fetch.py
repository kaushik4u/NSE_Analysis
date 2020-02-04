# import requests
import requests_async as requests
from datetime import datetime
import asyncio
import json
import pandas as pd
import os

url = 'https://www.bloombergquint.com/feapi/markets/options?option-type=call&security-type=index&sort-by=contract&limit=200'

proxies = {"http": "http://proxy.intra.bt.com:8080",
        #    "https": "http://proxy.intra.bt.com:8080/",
           "https": "xmu1.intra.bt.com:8080"
           }
# r = requests.get(url, proxies=proxies)
# # print(r.text)
# data = dict(json.loads(r.text))
# print(data['options'][0].keys())

# with open('temp.json', 'w') as fp:
#     json.dump(data, fp)

test_url = 'http://query1.finance.yahoo.com/v8/finance/chart/TCS.NS?symbol=TCS.NS&period1=-668159390&period2=1529865000&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-IN&region=IN'

# r = requests.get(test_url)
# print(r.text)



async def main(index):
    tasks = []
    sema = asyncio.BoundedSemaphore(value=2)
    for idx in index:
        with open('./data/temp/yahoo_historical_tracker.txt', 'r') as f:
            lines = f.readlines()
        for l in lines:
            if idx == l.split(' ')[1] and datetime.now().strftime('%d-%m-%Y') == l.split(' ')[0]:
                tasks.append(fetch_EOD_historical_data(idx,sema))
        # tasks.append(fetch_EOD_historical_data(idx,browser,csv,sema))
    await asyncio.gather(*tasks)


async def fetch_EOD_historical_data(index, sema):
    await sema.acquire()
    # yahoo_url = 'https://finance.yahoo.com/quote/'+index+'/history?p='+index
    yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/'+ index +'?symbol='+ index +'&period1=-668159390&period2='+ str(int(datetime.now().timestamp()))+ '&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-IN&region=IN'   
    print('fetching... ', yahoo_url)
    # res = await requests.get(yahoo_url, proxies=proxies)
    res = await requests.get(yahoo_url)
    print('Closing Session...!')
    
    fileName = index + '.json'
    with open('./data/temp/yahoo_data/json/'+fileName, 'w', encoding='utf-8') as outfile:
        json.dump(json.JSONDecoder().decode(res.text), outfile)
    print(datetime.now().strftime('%d-%m-%Y %HH:%MM')+' Writing file... ' + index)    
    with open('./data/temp/yahoo_historical_tracker.txt','a',encoding='utf-8') as trackerfile:
        trackerfile.writelines(datetime.now().strftime('%d-%m-%Y') +' '+ index +'\n')
    # downloadPath = 'C:\\Users\\608619925\\Downloads\\' + fileName
    # destinationPath = 'C:\\Users\\608619925\\Desktop\\Misc Projects\\python\\nse_test\\NSE_Data\\data\\temp\\'+fileName
    # os.replace(downloadPath, destinationPath)
    sema.release()

# csvInput = pd.read_csv('./ind_nifty100list.csv')
# # print(list(csvInput['Yahoo Ticker']))
# ticker_list = list(csvInput['Symbol'])
# # print(ticker_list)
# files = os.listdir('./data/temp/yahoo_data/json/')
# files = [f.replace('.csv','') for f in files]
# ticker_list = [t+'.NS' for t in ticker_list]
# # print(ticker_list)
# # print(files)
# fetch_list = []
# for ticker in ticker_list:
#     # print(file[:-4])
#     if ticker not in files:
#         # print(ticker)
#         fetch_list.append(ticker)
        
# # print(fetch_list)
# asyncio.get_event_loop().run_until_complete(main(fetch_list))
# # asyncio.get_event_loop().run_until_complete(main(ticker_list))

def initiate_historical_fetch():
    csvInput = pd.read_csv('./ind_nifty100list.csv')
    # print(list(csvInput['Yahoo Ticker']))
    ticker_list = list(csvInput['Symbol'])
    # print(ticker_list)
    files = os.listdir('./data/temp/yahoo_data/json/')
    files = [f.replace('.csv','') for f in files]
    ticker_list = [t+'.NS' for t in ticker_list]
    # print(ticker_list)
    # print(files)
    fetch_list = []
    for ticker in ticker_list:
        # print(file[:-4])
        if ticker not in files:
            # print(ticker)
            fetch_list.append(ticker)
            
    # print(fetch_list)
    asyncio.get_event_loop().run_until_complete(main(fetch_list))
    # asyncio.get_event_loop().run_until_complete(main(ticker_list))

# initiate_historical_fetch()
