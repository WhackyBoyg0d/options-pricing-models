import enum as en
import datetime as dt 

import hvplot.pandas 
import panel as pn
from panel.template import DarkTheme
from BinomialTreeModel import BinomialTreeModel
from BlackScholesModel import BlackScholesModel
from MonteCarloSimulation import MonteCarloSimulation
from ticker import Ticker


class OPTION_PRICING_MODEL(en.Enum):
    BINOMIAL_TREE = "Binomial Tree Model"
    MONTE_CARLO = "Monte Carlo Simulation"
    BLACK_SCHOLES = "Black-Scholes Model"

pn.extension('tabulator')

@pn.cache
def get_historical_data(ticker):
    """Fetch historical stock data for the specified ticker and caching it with panel app."""
    return Ticker.get_historical_data(ticker)

pricing_method = pn.widgets.Select(name="Pricing Model", options=[model.value for model in OPTION_PRICING_MODEL])

def get_options_pricing(pricing_model):
    """Return the option pricing model according to the specified pricing model."""
    # Initialize the input widgets
    ticker = pn.widgets.TextInput(name="Ticker", value="AAPL")
    strike_price = pn.widgets.FloatInput(name="Strike Price", value=300)
    risk_free_rate = pn.widgets.FloatSlider(name="Risk Free Rate (%)", start=0, end=100, value= 20)
    sigma = pn.widgets.FloatSlider(name="Sigma (%)", start=0, end=100, value= 30)
    exercise_date = pn.widgets.DatePicker(name="Exercise Date", value=dt.datetime.now())

    if pricing_model == OPTION_PRICING_MODEL.BINOMIAL_TREE.value:
        number_of_time_steps = pn.widgets.IntSlider(name="Number of Time Steps", start=5000, end=100000, value=15000)
        button = pn.widgets.Button(name="Calculate Option Price")

        def calculate_option_price(event):
            """Calculate the option price using Binomial Tree Model."""
            if event:
                print(ticker.value)
                historical_data = get_historical_data(ticker.value)
                spot_price = Ticker.get_last_price(historical_data, "Close")
                binomial_tree_model = BinomialTreeModel(spot_price, strike_price.value, risk_free_rate.value, sigma.value, (exercise_date.value - dt.date.today()).days, number_of_time_steps.value)
                tabulator = pn.widgets.Tabulator(historical_data, pagination="remote", page_size=10, disabled = True, width=800)
                plot = historical_data.hvplot.line(x='Date', y='Close', title=f'{ticker.value} Stock Price', width=800, height=400)
                call_option_price = binomial_tree_model.calculate_option_price("Call")
                put_option_price = binomial_tree_model.calculate_option_price("Put")
                return pn.Column(tabulator, plot, pn.pane.Markdown(f"Call Option Price: {call_option_price}"), pn.pane.Markdown(f"Put Option Price: {put_option_price}"))
            else:
                return pn.pane.Markdown("Click the button to calculate the option price.")
        
        gspec = pn.GridSpec(sizing_mode='stretch_both', max_height=500)
        gspec[0, 0] = pn.Column(ticker, strike_price, risk_free_rate, sigma, exercise_date, number_of_time_steps, button)
        gspec[0, 1:3] = pn.bind(calculate_option_price, button)
        return gspec
    
    elif pricing_model == OPTION_PRICING_MODEL.BLACK_SCHOLES.value:
        button = pn.widgets.Button(name="Calculate Option Price")
        
        def calculate_option_price2(event):
            """Calculate the option price using Black-Scholes Model."""
            if event:
                historical_data = get_historical_data(ticker.value)
                spot_price = Ticker.get_last_price(historical_data, "Close")
                black_scholes_model = BlackScholesModel(spot_price, strike_price.value, (exercise_date.value - dt.date.today()).days, risk_free_rate.value, sigma.value)
                tabulator = pn.widgets.Tabulator(historical_data, pagination="remote", page_size=10, disabled = True, width=800)
                plot = historical_data.hvplot.line(x='Date', y='Close', title=f'{ticker.value} Stock Price', width=800, height=400)
                call_option_price = black_scholes_model.calculate_option_price("Call")
                put_option_price = black_scholes_model.calculate_option_price("Put")
                markdown_content = f"""
                <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;">
                <strong>Call Option Price:</strong> {call_option_price}<br>
                <strong>Put Option Price:</strong> {put_option_price}
                </div>
                """
                return pn.Column(pn.Row(tabulator, plot), markdown_content)
            else:
                return pn.pane.Markdown("Click the button to calculate the option price.")
        
        gspec = pn.GridSpec(sizing_mode='stretch_both', max_height=500)
        gspec[0, 0] = pn.Column(ticker, strike_price, risk_free_rate, sigma, exercise_date, button)
        gspec[0, 1:3] = pn.bind(calculate_option_price2, button)
        return gspec
    
    elif pricing_model == OPTION_PRICING_MODEL.MONTE_CARLO.value:
        number_of_simulations = pn.widgets.IntSlider(name="Number of Simulations", start=5000, end=100000, value=15000)
        button = pn.widgets.Button(name="Calculate Option Price")
        
        def calculate_option_price3(event):
            """Calculate the option price using Monte Carlo Simulation."""
            if event:
                historical_data = get_historical_data(ticker.value)
                spot_price = Ticker.get_last_price(historical_data, "Close")
                monte_carlo_simulation = MonteCarloSimulation(spot_price, strike_price.value, (exercise_date.value - dt.date.today()).days, risk_free_rate.value, sigma.value, number_of_simulations.value)
                monte_carlo_simulation.simulate_prices()
                tabulator = pn.widgets.Tabulator(historical_data, pagination="remote", page_size=10, disabled = True, width=800)
                plot = monte_carlo_simulation.plot_simulation()
                call_option_price = monte_carlo_simulation.calculate_option_price("Call")
                put_option_price = monte_carlo_simulation.calculate_option_price("Put")
                markdown_content = f"""
                <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">
                <strong>Call Option Price:</strong> {call_option_price}<br>
                <strong>Put Option Price:</strong> {put_option_price}
                </div>
                """
                return pn.Column(tabulator, plot, pn.pane.Markdown(f"Call Option Price: {call_option_price}"), pn.pane.Markdown(f"Put Option Price: {put_option_price}"))
            else:
                return pn.pane.Markdown("Click the button to calculate the option price.")
        
        gspec = pn.GridSpec(sizing_mode='stretch_both', max_height=500)
        gspec[0, 0] = pn.Column(ticker, strike_price, risk_free_rate, sigma, exercise_date, number_of_simulations, button)
        gspec[0, 1:3] = pn.bind(calculate_option_price3, button)
        return gspec
        


    

pn.template.MaterialTemplate(
    site="Panel",
    title="Option Pricing",
    main=[pn.bind(get_options_pricing, pricing_method)],
    sidebar=[pricing_method],
    theme = DarkTheme
).servable()
