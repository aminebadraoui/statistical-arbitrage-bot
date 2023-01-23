# # Calculate cointegrated pairs
import numpy as np
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm

from strategy.functions.func_get_spread import calculate_spread
from strategy.functions.func_get_zscore import  get_zscores

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint

def calculate_average_volatility(closing_prices, window):
    # Calculate the returns
    returns = np.log(closing_prices) - np.log(closing_prices.shift(1))
    # Calculate the rolling standard deviation of the returns
    average_volatility = (returns.rolling(window=window).std() * np.sqrt(252)).mean()
    return average_volatility

def classify_cointegrated_pairs(data, significance=0.05):
   return data

def get_uid(ticker_0, ticker_1):
    sorted_characters = sorted([ticker_0, ticker_1])
    unique_id = "".join((sorted_characters))

    return unique_id
# Extract cointegrated pairs
def get_cointegrated_tickers(allPairsPrices):
    cointegrated_pairs = []
    unique_pair_combination_list = []

    for elm_0 in allPairsPrices:
        for elm_1 in allPairsPrices:
            ticker_0 = elm_0["symbol"]
            ticker_1 = elm_1["symbol"]

            if ticker_1 != ticker_0:
                # Get unique combination
                unique_id = get_uid(ticker_0, ticker_1)
                if unique_id in unique_pair_combination_list:
                    continue
                else:
                    unique_pair_combination_list.append(unique_id)

                    # Get close prices
                    series_0 = elm_0["prices"] # close prices time series 1
                    series_1 = elm_1["prices"] # close prices time series 2

                    pair_stat = compute_pair_stats(ticker_0, ticker_1, series_0, series_1)

                    if len(pair_stat) > 0:
                        cointegrated_pairs.append(pair_stat)

    classified_cointegrated_pairs = classify_cointegrated_pairs(cointegrated_pairs)

    return classified_cointegrated_pairs

# Compute co-integration between two ararys of close prices
def compute_pair_stats(ticker_0, ticker_1, close_prices_0, close_prices_1):
    is_cointegrated = False
    coint_res = coint(close_prices_0, close_prices_1)

    t_value = coint_res[0]
    p_value = coint_res[1]
    c_value = coint_res[2][1]

    if p_value < 0.05 and t_value < c_value:
        is_cointegrated = True
        model = sm.OLS(close_prices_0, close_prices_1).fit()
        hedge_ratio = model.params[0]  # coeff

        spreads = calculate_spread(close_prices_0, close_prices_1, hedge_ratio)
        z_scores = get_zscores(spreads).tolist()

        zero_crossings = len(np.where(np.diff(np.sign(spreads)))[0])

    if is_cointegrated:
        pair_stat = { "ticker_0": ticker_0,
                      "ticker_1": ticker_1,
                      "t_value": t_value,
                      "p_value": p_value,
                      "c_value": c_value,
                      "hedge_ratio": hedge_ratio,
                      "spread_zero_crossings": zero_crossings,
                      "spreads": spreads,
                      "z_scores": z_scores,
                      "close_prices_0": close_prices_0,
                      "close_prices_1": close_prices_1,
                      }
        return pair_stat
    else:
        return {}
