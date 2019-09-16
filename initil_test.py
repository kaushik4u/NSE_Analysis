from nsepy import get_history
from datetime import date
data = get_history(symbol="SBIN", start=date(2018, 1, 1), end=date(2019, 8, 31))
data[['Close']].plot()
