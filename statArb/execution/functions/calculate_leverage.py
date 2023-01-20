
import numpy as np


def calculate_optimal_leverage(coin_value, profit, position_size, fee_rate, volatility, liquidation_price):
    # Determine the value of the position in USDT
    position_value = coin_value * position_size
    # Determine the required price increase to achieve the desired profit
    price_increase = (profit + (position_value * fee_rate)) / position_value
    # Calculate the required leverage
    leverage = (price_increase / (1 - price_increase)) * (1 / volatility)
    # Adjust leverage to ensure it is within a safe range
    leverage = min(leverage, liquidation_price / (coin_value * (1 - fee_rate)))
    return leverage