import requests
import json
import pandas as pd
url = 'https://www.bloombergquint.com/feapi/markets/options?option-type=call&security-type=index&sort-by=contract&limit=200'

proxies = {"http": "http://proxy.intra.bt.com:8080",
           "https": "http://proxy.intra.bt.com:8080",
           }
# r = requests.get(url, proxies=proxies)
# # print(r.text)
# data = dict(json.loads(r.text))
# print(data['options'][0].keys())

# with open('temp.json', 'w') as fp:
#     json.dump(data, fp)

