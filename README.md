# Option Pricing Models

## Introduction  
This repository represents simple web app for calculating option prices (European Options). It uses three different methods for option pricing:  
1. Black-Scholes model    
2. Monte Carlo simulation    
3. Binomial model    

Each model has various parameters that user needs to import:  

- Ticker  
- Strike price  
- Expiry date  
- Risk-free rate  
- Volatility  

Option pricing models are implemented in [Python 3.7](https://www.python.org/downloads/release/python-377/). Latest spot price, for specified ticker, is fetched from Yahoo Finance API using [yfinace](https://github.com/ranaroussi/yfinance/tree/main). Visualization of the models through simple web app is implemented using [Panel](https://panel.holoviz.org/) library.

## Start the app
To start the app, you need to install all required libraries. You can do that by running the following command:  
```python
pip install -r requirements.txt
```
After that, you can start the app by running the following command:  
```python
panel serve panel.py
```
