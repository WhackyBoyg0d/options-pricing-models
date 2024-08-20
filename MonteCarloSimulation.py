import numpy as np
from scipy.stats import norm

from interface import OptionPricingModel

class MonteCarloSimulation(OptionPricingModel):
    """
    Class for Monte Carlo Simulation option pricing model
    """

    def __init__(self, spot_price, strike_price, time_to_maturity, risk_free_rate, volatility, num_simulations):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.time_to_maturity = time_to_maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility

        self.num_simulations = num_simulations
        self.num_of_steps = time_to_maturity * 365
        self.dt = time_to_maturity / self.num_of_steps
    

