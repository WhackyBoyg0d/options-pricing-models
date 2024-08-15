import datetime

import requests_cache
import matplotlib.pyplot as plt
import yfinance as yf


class Ticker:
    """ Fetch stock data from Yahoo Finance. """

    @staticmethod
    def get_historical_data(ticker, start_date = None, end_date = None, cache_date = None, cache_days = 1):
        """
        Fetch historical stock data from Yahoo Finance. Request is by default cached for 1 day.

        :param ticker: Stock symbol
        :param start_date: Start date of the historical data
        :param end_date: End date of the historical data
        :param cache_date: Date of the cache
        :param cache_days: Number of days to cache the data
        :return: Historical stock data
        """

        try:
            # initilaize sqlite for caching yahoo finance requests
            expire_after = datetime.timedelta(days=cache_days)
            session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)

            # Adding headers to session
            session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Accept': 'application/json;charset=utf-8'}

            # Fetch historical stock data
            if start_date is not None and end_date is not None:
                data = yf.Ticker(ticker).history(start=start_date, end=end_date)
            else:
                data = yf.Ticker(ticker).history()
            if data is None:
                return None
            return data
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return None
        
    @staticmethod
    def get_columns(data):
        """
        Get dataframe columns for previously fetched stock data.

        :param data: Stock data
        :return: Columns of the stock data
        """

        if data is None:
            return None
        return [column for column in data.columns]
    
    @staticmethod
    def get_last_price(data, column_name):
        """
        Get the last price of the stock.

        :param data: Stock data
        :param column_name: Column name for the stock data
        :return: Last price of the stock
        """

        if data is None or column_name is None:
            return None
        if column_name not in Ticker.get_columns(data):
            return None
        return data[column_name][-1]
    
    @staticmethod
    def plot_data(data, ticker, column_name):
        """
        Plot the stock data.

        :param data: Stock data
        :param ticker: Stock symbol
        :param column_name: Column name for the stock data
        """

        try:
            if data is None:
                return
            data[column_name].plot(figsize=(10, 7), title=f" Historical data for {ticker} - {column_name}")
            plt.ylabel(column_name)
            plt.xlabel("Date")
            plt.legend(loc = "best")
            plt.show()
        except Exception as e:
            print(f"Error plotting data for {ticker}: {e}")
            return 



