import requests_cache
from datetime import datetime as dt
import yfinance as yf
from ticker import Ticker

session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=1)

# Adding headers to session
session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Accept': 'application/json;charset=utf-8'}

ticker = "AMZN"
tickerObj = yf.Ticker(ticker)
hist = tickerObj.history()
print(Ticker.get_last_price(hist, "Close"))
print(Ticker.get_columns(hist))
Ticker.plot_data(hist, ticker, "Close")

