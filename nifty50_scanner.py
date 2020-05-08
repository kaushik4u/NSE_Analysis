import asyncio
import aiohttp
import json

url_list = []
tickers = []

with open('./nifty50.txt') as f:
    tickers = f.readlines()

# print(tickers)

for t in tickers:
    yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + t.rstrip() +'.NS?region=IN&lang=en-IN&includePrePost=false&interval=1h&range=6mo'
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
        json.dump(htmls, outfile)
    # print(htmls)

# initiate_fetch()

with open('./data/temp/test_data/nifty50.json') as f:
    data = json.load(f)

print(len(data))
# print(data[0]['chart']['result']['meta']['symbol'])
print(data[0]['chart']['result'][0]['meta']['symbol'])
print(data[0]['chart']['result'][0]['timestamp'])
print(data[0]['chart']['result'][0]['indicators']['quote'][0]['open'])
