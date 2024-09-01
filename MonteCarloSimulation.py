import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

from interface import OptionPricingModel

class MonteCarloSimulation(OptionPricingModel):
    """
    Class for Monte Carlo Simulation option pricing model
    """

    def __init__(self, spot_price, strike_price, time_to_maturity, risk_free_rate, volatility, num_simulations):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.time_to_maturity = time_to_maturity / 365
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility

        self.num_simulations = num_simulations
        self.num_of_steps = time_to_maturity 
        self.dt = time_to_maturity / self.num_of_steps

    def simulate_prices(self):
        """
        Simulate the stock prices using Geometric Brownian Motion
        """
        prices = np.zeros((self.num_simulations, self.num_of_steps + 1))
        prices[:, 0] = self.spot_price

        for i in range(1, self.num_of_steps + 1):
            Z = np.random.standard_normal(self.num_simulations)
            prices[:, i] = prices[:, i - 1] * np.exp((self.risk_free_rate - 0.5 * self.volatility ** 2) * self.dt + self.volatility * np.sqrt(self.dt) * Z)

        self.simulate_prices = prices

    def _calculate_call_option_price(self):
        """
        Calculate the price of European Call Option using Monte Carlo Simulation
        :return: Price of the Call Option
        """
        if self.simulate_prices is None:
            return -1
        call_prices = np.maximum(self.simulate_prices[:, -1] - self.strike_price, 0)
        call_price = np.exp(-self.risk_free_rate * self.time_to_maturity) * np.mean(call_prices)
        return call_price
    
    def _calculate_put_option_price(self):
        """
        Calculate the price of European Put Option using Monte Carlo Simulation
        :return: Price of the Put Option
        """
        if self.simulate_prices is None:
            return -1
        put_prices = np.maximum(self.strike_price - self.simulate_prices[:, -1], 0)
        put_price = np.exp(-self.risk_free_rate * self.time_to_maturity) * np.mean(put_prices)
        return put_price
    

    def plot_simulation(self):
        """
        Plot the simulated stock price movements
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.simulate_prices.T)
        plt.title("Monte Carlo Simulation of Stock Prices")
        plt.xlabel("Time Steps")
        plt.ylabel("Stock Price")
        plt.show()

