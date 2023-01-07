import pandas as pd

# Calculate spread between two price histories
def calculate_spread(series_0, series_1, hedge_ratio):
    spread = pd.Series(series_0)-pd.Series(series_1)*hedge_ratio

    return spread