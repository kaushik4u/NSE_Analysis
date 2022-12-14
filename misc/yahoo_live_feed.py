from datetime import datetime, timedelta

# import time
import json
import requests

proxyDict = {}

yahoo_url = "https://query1.finance.yahoo.com/v8/finance/chart/ACC.NS?symbol=ACC.NS&period1=1577766180&period2=1578284580&interval=1m"


def fetch_live_feed(ticker, proxy):
    # print(int(datetime.now().timestamp()))
    prevDay = datetime.now() + timedelta(days=-1)
    # print(int(prevDay.timestamp()))
    yahoo_url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        + ticker
        + ".NS?symbol="
        + ticker
        + ".NS&period1="
        + str(int(prevDay.timestamp()))
        + "&period2="
        + str(int(datetime.now().timestamp()))
        + "&interval=1m"
    )
    print(yahoo_url)
    if proxy:
        res = requests.get(yahoo_url, proxies=proxyDict)
    else:
        res = requests.get(yahoo_url)
    # print(res.text)
    fileName = ticker + ".json"
    with open(
        "./data/temp/yahoo_live/json/" + fileName, "w", encoding="utf-8"
    ) as outfile:
        json.dump(json.JSONDecoder().decode(res.text), outfile)
    print("Data fetched : ", datetime.now().strftime("%d-%m-%Y %HH:%MM"))


# fetch_live_feed('TCS',True)
