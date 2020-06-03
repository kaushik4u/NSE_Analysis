import asyncio
import aiohttp
import json

url_list = []
tickers = []

with open('./nifty200.txt') as f:
# with open('./nifty200.txt') as f:
    tickers = f.readlines()

# print(tickers)

"""
yahoo finance limits:

1 min till 7 days
5/10/15 min till 60 days
1 hour till 2 years
1 day till 5 years

"""

for t in tickers:
    yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + t.rstrip() +'.NS?region=IN&lang=en-IN&includePrePost=false&interval=1d&range=6mo'
    yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + t.rstrip() +'.NS?region=IN&lang=en-IN&includePrePost=false&interval=1m&range=7d'
    url_list.append(yahoo_url)

# print(url_list)

async def fetch(session, url):
    async with session.get(url) as response:
        # temp = url.replace('https://query1.finance.yahoo.com/v8/finance/chart/')
        # ticker = temp.split('.')[0]
        # res = await response.json()
        # print(res)
        # with open('./data/temp/test_data/'+ ticker +'.json', 'w', encoding='utf-8') as outfile:
        #     json.dump(res, outfile)
        return await response.json()
        # return res


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results


# if __name__ == '__main__':
def initiate_fetch():
    loop = asyncio.get_event_loop()
    urls = url_list
    htmls = loop.run_until_complete(fetch_all(urls, loop))
    with open('./data/temp/test_data/nifty50.json', 'w', encoding='utf-8') as outfile:
    # with open('./data/temp/test_data/nifty200.json', 'w', encoding='utf-8') as outfile:
        json.dump(htmls, outfile)
    # print(htmls)

initiate_fetch()

with open('./data/temp/test_data/nifty50.json') as f:
# with open('./data/temp/test_data/nifty200.json') as f:
    data = json.load(f)

print(len(data))
# print(data[0]['chart']['result']['meta']['symbol'])
print(data[0]['chart']['result'][0]['meta']['symbol'])
print(data[0]['chart']['result'][0]['timestamp'])
print(data[0]['chart']['result'][0]['indicators']['quote'][0]['open'])

print(tickers[5],data[5]['chart']['result'][0]['meta']['symbol'])

idx = 0
for d in data:
    print(str(idx) + ' : ' +d['chart']['result'][0]['meta']['symbol'])
    idx = idx + 1