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
# data = get_history(symbol="SBIN", start=date(2018, 1, 1), end=date(2019, 8, 31))
# data[['Close']].plot()

# Input Start and End Date
start = datetime.datetime(2019,1,1)
end = datetime.datetime(2019,12,31)
stock = web.DataReader('NSE/TCS',"quandl",start,end)
print(stock)