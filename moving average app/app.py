from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime
import requests
import pandas as pd
import numpy as np

proxyDict = {
   
}

app = Flask(__name__, template_folder='./')

@app.route("/")
def index():
   return render_template("test.html")

@app.route("/data/<ticker>", methods=['GET'])
def live(ticker):
   jsonData = fetch_data(ticker)
   return jsonify({'data':jsonData})

def fetch_data(ticker):
    yurl = 'https://query1.finance.yahoo.com/v8/finance/chart/'+ ticker +'.NS?region=IN&lang=en-IN&includePrePost=false&interval=1d&range=5y'
    res = requests.get(yurl, proxies=proxyDict)
    print(res)
    fileName = 'temp.json'
    with open('./'+fileName, 'w', encoding='utf-8') as outfile:
        json.dump(json.JSONDecoder().decode(res.text), outfile)
    return json.JSONDecoder().decode(res.text)

if __name__ == '__main__':
#    initiate_historical_fetch()
   app.run(debug=True)
