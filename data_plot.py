import pandas as pd
import json
from datetime import datetime
import plotly.graph_objects as go

src = './data/temp/yahoo_data/json/'
ticker = 'INFY.NS.json'
# data = json.loads(src + ticker)
# with open(src + ticker) as json_file:
#     data = json.load(json_file)
data = [json.loads(line) for line in open(src + ticker, 'r')]
# print(len(data['chart']['result'][0]['timestamp']))

date = []
open = []
close =[]
high = []
low = []
for i in range(len(data['chart']['result'][0]['timestamp'])):
    dt_object = datetime.fromtimestamp(data['chart']['result'][0]['timestamp'][i])
    date.append(dt_object)
    open.append(data['chart']['result'][0]['indicators']['quote'][0]['open'][i])
    high.append(data['chart']['result'][0]['indicators']['quote'][0]['high'][i])
    low.append(data['chart']['result'][0]['indicators']['quote'][0]['low'][i])
    close.append(data['chart']['result'][0]['indicators']['quote'][0]['close'][i])
    # print(dt_object)

print(len(data['chart']['result'][0]['indicators']['quote'][0]['open']))
# fig = go.Figure(data=[go.Candlestick(x=date,
#                                      open=open,
#                                      high=high,
#                                      low=low,
#                                      close=close)])

# fig.show()
