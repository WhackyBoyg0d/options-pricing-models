import numpy as np
from scipy.stats import norm

from interface import OptionPricingModel

class BinomialTreeModel(OptionPricingModel):
    """
    Class implementing Binomial Option Pricing Model to calculate price of European Call and Put Options.
    Calculates option price in discrete time steps, in specified number of time points between date of vsluation and exercise date.
    The pricing models has three steps:
    1. Price tree generation
    2. Calculate the option price at each final node
    3. Sequential calculation of option price at each preceding node
    """

    def __init__(self, spot_price, strike_price, risk_free_rate, sigma, days_to_maturity, num_steps):
        """
        Initialize the BinomialTreeModel with the following parameters:
        :param spot_price: Current price of the underlying asset
        :param strike_price: Strike price of the option
        :param risk_free_rate: Risk free rate of return
        :param volatility: Volatility of the underlying asset
        :param time_to_maturity: Time to maturity of the option
        :param num_steps: Number of time steps to be considered in the model
        """
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.risk_free_rate = risk_free_rate 
        self.sigma = sigma 
        self.days_to_maturity = days_to_maturity / 365
        self.num_steps = num_steps
        

    def _calculate_call_option_price(self):
        """
        Calculate the price of European Call Option using Binomial Tree Model
        :return: Price of the Call Option
        """

        print("Spot Price: ", self.spot_price) # Debugging
        # Delta t, up and down factors
        delta_T = self.days_to_maturity / self.num_steps
        u = np.exp(self.sigma * np.sqrt(delta_T))
        d = 1 / u

        # Price vector initialization
        V = np.zeros(self.num_steps + 1)

        # Calculate the price of the underlying asset at each node
        S_T = np.array([self.spot_price * (u ** j) * (d ** (self.num_steps - j)) for j in range(self.num_steps + 1)])
        print("u: ", u)
        print("d: ", d)
        print("V: ", V)
        print("S_T: ", S_T) # Debugging

        a = np.exp(self.risk_free_rate * delta_T) # Risk free compound return
        print("a: ", a) # Debugging
        p = (a - d) / (u - d) # Risk neutral up probability
        q = 1 - p # Risk neutral down probability

        # Calculate the option price at each final node
        V[:] = np.maximum(0, S_T - self.strike_price)

        # Sequential calculation of option price at each preceding node
        for i in range(self.num_steps - 1, -1, -1):
            V[:-1] = np.exp(-self.risk_free_rate * delta_T) * (p * V[1:] + q * V[:-1])
        
        return V[0]
    
    def _calculate_put_option_price(self):
        """
        Calculate the price of European Put Option using Binomial Tree Model
        :return: Price of the Put Option
        """

        # Delta t, up and down factors
        delta_T = self.days_to_maturity / self.num_steps
        u = np.exp(self.sigma * np.sqrt(delta_T))
        d = 1 / u

        # Price vector initialization
        V = np.zeros(self.num_steps + 1)

        # Calculate the price of the underlying asset at each node
        S_T = np.array([self.spot_price * (u ** j) * (d ** (self.num_steps - j)) for j in range(self.num_steps + 1)])

        a = np.exp(self.risk_free_rate * delta_T)
        p = (a - d) / (u - d)
        q = 1 - p

        # Calculate the option price at each final node
        V[:] = np.maximum(0, self.strike_price - S_T)

        # Sequential calculation of option price at each preceding node
        for i in range(self.num_steps - 1, -1, -1):
            V[:-1] = np.exp(-self.risk_free_rate * delta_T) * (p * V[1:] + q * V[:-1])

        return V[0]
