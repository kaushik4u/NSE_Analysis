# Import modules
from datetime import datetime, timedelta
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like #For solving import pandas_datareader issue
import numpy as np
import datetime
import csv
import requests
import pandas_datareader.data as web
import pandas_datareader as pdr
from pandas_datareader import data, wb


# Input Start and End Date
start = datetime.datetime(2019,1,1)
end = datetime.datetime(2019,12,31)

Today = datetime.datetime.now().strftime ("%Y-%m-%d")

# Import list of stock names from NSE website
# with requests.Session() as s:
#     download = s.get('https://www.nseindia.com/products/content/sec_bhavdata_full.csv')
#     decoded_content = download.content.decode('utf-8')
#     cr = csv.reader(decoded_content.splitlines(), delimiter=',')
#     my_list = pd.DataFrame(list(cr))

stock_list = pd.read_csv('./sec_bhavdata_full.csv')
# print(stock_list['SYMBOL'])
# decoded_content = download.content.decode('utf-8')
# cr = csv.reader('./sec_bhavdata_full.csv', delimiter=',')
# my_list = pd.DataFrame(list(cr))
# my_list = pd.DataFrame(list(stock_list['SYMBOL']))
my_list = stock_list

#View the top rows
print(my_list.head())

# Clean the downloaded data
# Rename the headers
new_header = my_list.iloc[0] #grab the first row for the header
my_list = my_list[1:] #take the data less the header row
my_list = my_list.rename(columns = new_header)

# Get only the list of stock names - remove everything else
my_list['stock_name'] = "NSE/"+ my_list['SYMBOL']
stock_list = my_list['stock_name'].tolist()
stock_list = list(set(stock_list))

#View the top few stock names
stock_list[1:10]


# Create Empty Dataframe
stock_final = pd.DataFrame()

# Scrape the stock prices from quandl
# for i in range(len(stock_list))#Use this to scrape all the stocks
for i in range(10):  
    print(i)    
    try:
        stock=[]
        stock = web.DataReader(stock_list[i],"quandl",start,end)
        stock['Name']=stock_list[i]
        
        stock_final = pd.DataFrame.append(stock_final,stock)
    except Exception: # Replace Exception with something more specific.
        i = i+1

#View the top 10 rows of the downloaded data 
stock_final.head()

#Plot trend for a particular stock

#Subset for a particular stock
stock_final = stock_final[stock_final['Name']=='NSE/SUTLEJTEX']

#Generate a line plot
stock_final.plot(y='High')
plt.show()