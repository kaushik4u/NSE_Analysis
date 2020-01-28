from datetime import datetime, timedelta
# import time
import json
import requests
import asyncio

yahoo_url= 'https://query1.finance.yahoo.com/v8/finance/chart/ACC.NS?symbol=ACC.NS&period1=1577766180&period2=1578284580&interval=1m'

def fetch_live_feed(ticker):
    # print(int(datetime.now().timestamp()))
    prevDay = datetime.now() + timedelta(days=-5)
    # print(int(prevDay.timestamp()))
    yahoo_url= 'https://query1.finance.yahoo.com/v8/finance/chart/'+ ticker +'.NS?symbol='+ ticker +'.NS&period1='+ str(int(prevDay.timestamp())) +'&period2=' + str(int(datetime.now().timestamp())) +'&interval=1m'
    print(yahoo_url)
    res = requests.get(yahoo_url)
    # print(res.text)
    fileName = ticker + '.json'
    with open('./data/temp/yahoo_live/json/'+fileName, 'w', encoding='utf-8') as outfile:
        json.dump(json.JSONDecoder().decode(res.text), outfile)
    print('Data fetched : ', datetime.now().strftime('%d-%m-%Y %HH:%MM'))
# fetch_live_feed('ACC')

async def fetch_1min_feed(ticker,date,sema):
    await sema.acquire()
    # print(int(datetime.now().timestamp()))

    # prevDay = datetime.now() + timedelta(days=-5)
    prevDay = date + timedelta(days=-5)
    # print(int(prevDay.timestamp()))
    yahoo_url= 'https://query1.finance.yahoo.com/v8/finance/chart/'+ ticker +'?symbol='+ ticker +'&period1='+ str(int(prevDay.timestamp())) +'&period2=' + str(int(date.timestamp())) +'&interval=1m'
    print(yahoo_url)
    res = requests.get(yahoo_url)
    # print(res.text)
    fileName = ticker +'_'+ date.strftime('%d-%m-%Y') +'_'+ prevDay.strftime('%d-%m-%Y') +'.json'
    with open('./data/temp/nifty_data/'+fileName, 'w', encoding='utf-8') as outfile:
        json.dump(json.JSONDecoder().decode(res.text), outfile)
    print('Data fetched : ', datetime.now().strftime('%d-%m-%Y %HH:%MM'))
    sema.release()


# sdate = date(2008, 8, 15)   # start date
edate = datetime.now()
sdate = datetime(2007, 9, 17,9,15)   # end date

delta = edate - sdate       # as timedelta
# print(delta.days)
listofDates = []
day = sdate
for i in range(delta.days,0,-5):
    listofDates.append(day)
    day = sdate + timedelta(days=i)
    print(day)

async def main(dates):
    tasks = []
    sema = asyncio.BoundedSemaphore(value=2)
    for d in dates:
        tasks.append(fetch_1min_feed('%5ENSEI',d,sema))
        # tasks.append(fetch_EOD_historical_data(idx,browser,csv,sema))
    await asyncio.gather(*tasks)

asyncio.get_event_loop().run_until_complete(main(listofDates))