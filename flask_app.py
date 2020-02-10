from flask import Flask, render_template, request, redirect, url_for, jsonify
# import sqlite3
import json
from datetime import datetime
import pandas as pd
import numpy as np
import talib
from yahoo_live_feed import fetch_live_feed
from yahoo_historical_fetch import initiate_historical_fetch

# Opens file if exists, else creates file
# connex = sqlite3.connect("./data/nse_data.db")
# This object lets us actually send messages to our DB and receive results
# cur = connex.cursor()
app = Flask(__name__)

@app.route("/")
def index():
   return render_template("highcharts_historical.html")

@app.route("/intra")
def intraday():
   return render_template("highcharts_intra.html")

@app.route("/simulator")
def simulator():
   return render_template("simulator.html")

@app.route("/livedata/<ticker>", methods=['GET'])
def live(ticker):
   fetch_live_feed(ticker,True)
   # fetch_live_feed(ticker, True)
   # return render_template("highcharts_test.html")
   src = './data/temp/yahoo_live/json/'
   tickerFile = ticker+'.json'
   # data = json.loads(src + ticker)
   with open(src + tickerFile) as json_file:
      data = json.load(json_file)
   jsonData = load_data(data)
   tech_data = technical_indicators(data)
   return jsonify({'data':jsonData,'technical':tech_data})

@app.route('/historicaldata/<ticker>', methods=['GET'])
def get_tasks(ticker):
   src = './data/temp/yahoo_data/json/'
   tickerFile = ticker+'.NS.json'
   # data = json.loads(src + ticker)
   with open(src + tickerFile) as json_file:
      data = json.load(json_file)
   jsonData = load_data(data)
   tech_data = technical_indicators(data)
   return jsonify({'data':jsonData,'technical':tech_data})

@app.route('/backtest/<ticker>',methods=['GET'])
def get_backtest_data(ticker):
   # print(request.args.to_dict())
   src = './data/temp/onemin_consolidated/' + ticker + '.csv'
   df = pd.read_csv(src)
   df = df.sort_values(by='datetime', ascending=False)
   df['datetime'] = pd.to_datetime(df['datetime'])
   print(df.info())
   # df = df.groupby(pd.Grouper(key='datetime', freq='15min'))
   # df.set_index('datetime', drop=True, append=False, inplace=True, verify_integrity=False)
   df = df.sort_index()
   # df = df.groupby(pd.Grouper(freq='D')).transform(np.cumsum).resample('D', how='ohlc')
   # df = df['close'].resample('15min').ohlc()
   # df = df['close'].resample('D').agg({'close': 'ohlc', 'volume': 'sum'})
   df = df[['datetime', 'close', 'volume']]
   df.set_index('datetime', drop=True, append=False,
                inplace=True, verify_integrity=False)
   df = df.resample('D').agg({'close': 'ohlc', 'volume': 'sum'})
   # df = droplevel(level=0)
   # df = df.reset_index(level=['datetime','open', 'high', 'low', 'volume'])
   # df.to_flat_index()
   df.columns = df.columns.droplevel()
   # print(df.columns)
   # print(df.head())
   json_data = json.JSONDecoder().decode(df.to_json(orient="table"))
   return jsonify({'data': json_data, 'technical': []})
   # return json_data






# helper functions for flask app
# def backtest_data(df,period):
#    if period = '1D':





def load_data(data):
   jsonData = []
   for i in range(len(data['chart']['result'][0]['timestamp'])):
      # dt_object = datetime.fromtimestamp(data['chart']['result'][0]['timestamp'][i])
      # date.append(dt_object)
      # open.append(data['chart']['result'][0]['indicators']['quote'][0]['open'][i])
      # high.append(data['chart']['result'][0]['indicators']['quote'][0]['high'][i])
      # low.append(data['chart']['result'][0]['indicators']['quote'][0]['low'][i])
      # close.append(data['chart']['result'][0]['indicators']['quote'][0]['close'][i])
      if data['chart']['result'][0]['indicators']['quote'][0]['open'][i] == 'null':
         open_val = 0
      else:
         open_val = data['chart']['result'][0]['indicators']['quote'][0]['open'][i]
      
      if data['chart']['result'][0]['indicators']['quote'][0]['high'][i] == 'null':
         high = 0
      else:
         high = data['chart']['result'][0]['indicators']['quote'][0]['high'][i]
      
      if data['chart']['result'][0]['indicators']['quote'][0]['low'][i] == 'null':
         low = 0
      else:
         low = data['chart']['result'][0]['indicators']['quote'][0]['low'][i]
      
      if data['chart']['result'][0]['indicators']['quote'][0]['close'][i] == 'null':
         close = 0
      else:
         close = data['chart']['result'][0]['indicators']['quote'][0]['close'][i]
      
      if data['chart']['result'][0]['indicators']['quote'][0]['volume'][i] == 'null':
         volume = 0
      else:
         volume = data['chart']['result'][0]['indicators']['quote'][0]['volume'][i]

      jsonData.append({
         'date': data['chart']['result'][0]['timestamp'][i] * 1000,
         'open': open_val,
         'high': high,
         'low': low,
         'close': close,
         'volume' : volume 
      })
   return jsonData

def technical_indicators(data):
   close = []
   for i in range(len(data['chart']['result'][0]['timestamp'])):
      if data['chart']['result'][0]['indicators']['quote'][0]['close'][i] == 'null' or data['chart']['result'][0]['indicators']['quote'][0]['close'][i] == None:
         close.append(0)
      else:
         close.append(round(data['chart']['result'][0]['indicators']['quote'][0]['close'][i],2))
   # float_data = [float(x) for x in real_data]
   close = np.array(close,dtype=float)
   # close = np.random.random(100)
   ema20 = talib.EMA(close,timeperiod=20)
   ema100 = talib.EMA(close,timeperiod=100)
   ema20 = ema20.tolist()
   ema20 = ['Null' if np.isnan(x) else round(x,2) for x in ema20]
   ema100 = ema100.tolist()
   ema100 = ['Null' if np.isnan(x) else round(x,2) for x in ema100]
   jsonData = {'ema20':ema20,'ema100':ema100}

   return jsonData
   # print(close,ema20)



if __name__ == '__main__':
   initiate_historical_fetch()
   app.run(debug=True)
