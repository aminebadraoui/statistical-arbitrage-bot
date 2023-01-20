import pandas as pd

# Calculate spread between two price histories
def calculate_spread(close_prices_0, close_prices_1, hedge_ratio):
    spread = pd.Series(close_prices_0)-pd.Series(close_prices_1)*hedge_ratio

    return spread.tolist()