# from nsepy import get_history
# from datetime import date
# data = get_history(symbol="SBIN", start=date(2018, 1, 1), end=date(2019, 8, 31))
# data[['Close']].plot()
import requests


# 'https://www.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date=01-01-2014&section=EQ'
datestring = '01-01-2014'
bhavurl = 'http://www.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date=' + datestring + '&section=EQ'
req = requests.get(bhavurl, headers={'User-Agent': "Chrome Browser"})
print(req.text)
