from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import json
from datetime import datetime
import pandas as pd
from yahoo_live_feed import fetch_live_feed
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

@app.route("/livedata/<ticker>", methods=['GET'])
def live(ticker):
   fetch_live_feed(ticker)
   # return render_template("highcharts_test.html")
   src = './data/temp/yahoo_live/json/'
   tickerFile = ticker+'.json'
   # data = json.loads(src + ticker)
   with open(src + tickerFile) as json_file:
      data = json.load(json_file)
   jsonData = load_data(data)
   return jsonify({'data':jsonData})

@app.route('/historicaldata/<ticker>', methods=['GET'])
def get_tasks(ticker):
   src = './data/temp/yahoo_data/json/'
   tickerFile = ticker+'.NS.json'
   # data = json.loads(src + ticker)
   with open(src + tickerFile) as json_file:
      data = json.load(json_file)
   
   # date = []
   # open = []
   # close =[]
   # high = []
   # low = []
   # jsonData = []
   # for i in range(len(data['chart']['result'][0]['timestamp'])):
   #    # dt_object = datetime.fromtimestamp(data['chart']['result'][0]['timestamp'][i])
   #    # date.append(dt_object)
   #    # open.append(data['chart']['result'][0]['indicators']['quote'][0]['open'][i])
   #    # high.append(data['chart']['result'][0]['indicators']['quote'][0]['high'][i])
   #    # low.append(data['chart']['result'][0]['indicators']['quote'][0]['low'][i])
   #    # close.append(data['chart']['result'][0]['indicators']['quote'][0]['close'][i])
   #    if data['chart']['result'][0]['indicators']['quote'][0]['open'][i] == 'null':
   #       open_val = 0
   #    else:
   #       open_val = data['chart']['result'][0]['indicators']['quote'][0]['open'][i]
      
   #    if data['chart']['result'][0]['indicators']['quote'][0]['high'][i] == 'null':
   #       high = 0
   #    else:
   #       high = data['chart']['result'][0]['indicators']['quote'][0]['high'][i]
      
   #    if data['chart']['result'][0]['indicators']['quote'][0]['low'][i] == 'null':
   #       low = 0
   #    else:
   #       low = data['chart']['result'][0]['indicators']['quote'][0]['low'][i]
      
   #    if data['chart']['result'][0]['indicators']['quote'][0]['close'][i] == 'null':
   #       close = 0
   #    else:
   #       close = data['chart']['result'][0]['indicators']['quote'][0]['close'][i]
      
   #    if data['chart']['result'][0]['indicators']['quote'][0]['volume'][i] == 'null':
   #       volume = 0
   #    else:
   #       volume = data['chart']['result'][0]['indicators']['quote'][0]['volume'][i]

   #    jsonData.append({
   #       'date': data['chart']['result'][0]['timestamp'][i] * 1000,
   #       'open': open_val,
   #       'high': high,
   #       'low': low,
   #       'close': close,
   #       'volume' : volume 
   #    })
   jsonData = load_data(data)
   return jsonify({'data': jsonData})

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


if __name__ == '__main__':
    app.run(debug=True)