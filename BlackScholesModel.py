import numpy as np
from scipy.stats import norm

from interface import OptionPricingModel

class BlackScholesModel(OptionPricingModel):
    """
    Class for Black-Scholes option pricing model

    Call/Put option price is calculated with following assumptions:
    - European option can be exercised only on maturity date.
    - Underlying stock does not pay divident during option's lifetime.  
    - The risk free rate and volatility are constant.
    - Efficient Market Hypothesis - market movements cannot be predicted.
    - Lognormal distribution of underlying returns.
    """

    def __init__(self, spot_price, strike_price, time_to_maturity, risk_free_rate, volatility):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.time_to_maturity = time_to_maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
    
    def _calculate_call_option_price(self):
        """
        Calculate the price of European Call Option using Black-Scholes Model
        :return: Price of the Call Option
        """
        d1 = (np.log(self.spot_price / self.strike_price) + (self.risk_free_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / (self.volatility * np.sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity)
        call_price = self.spot_price * norm.cdf(d1) - self.strike_price * np.exp(-self.risk_free_rate * self.time_to_maturity) * norm.cdf(d2)
        return call_price
    
    def _calculate_put_option_price(self):
        """
        Calculate the price of European Put Option using Black-Scholes Model
        :return: Price of the Put Option
        """

        d1 = (np.log(self.spot_price / self.strike_price) + (self.risk_free_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / (self.volatility * np.sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity)
        put_price = self.strike_price * np.exp(-self.risk_free_rate * self.time_to_maturity) * norm.cdf(-d2) - self.spot_price * norm.cdf(-d1)
        return put_price