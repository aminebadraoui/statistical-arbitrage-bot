# # Calculate cointegrated pairs
import math
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm

# Extract cointegrated pairs
def get_cointegrated_tickers(allPairsPrices):
    cointegrated_pairs = []
    unique_pair_combination_list = []

    for pair_0 in allPairsPrices.keys():
        for pair_1 in allPairsPrices.keys():
            if pair_1 != pair_0:
                # Get unique combination
                sorted_characters = sorted([pair_0,pair_1])
                unique_id = "".join((sorted_characters))

                if unique_id in unique_pair_combination_list:
                    continue
                else:
                    unique_pair_combination_list.append(unique_id)

                    # Get close prices
                    series_0 = allPairsPrices[pair_0] # close prices time series 1
                    series_1 = allPairsPrices[pair_1] # close prices time series 2

                    is_cointegreated, t_value, p_value, c_value, hedge_ratio, zero_crossings = compute_cointegration(series_0, series_1)

                    if is_cointegreated:
                        cointegrated_pairs.append({
                            "Ticker 1": pair_0,
                            "Ticker 2": pair_1,
                            "t value": t_value,
                            "p value": p_value,
                            "c value": c_value,
                            "Hedge Ratio": hedge_ratio,
                            "Zero Crossings": zero_crossings
                        })


    df_cointegration = pd.DataFrame(cointegrated_pairs)

    return df_cointegration

# Compute co-integration between two ararys of close prices
def compute_cointegration(series_0, series_1):
    is_cointegrated = False
    coint_res = coint(series_0, series_1)

    t_value = coint_res[0]
    p_value = coint_res[1]
    c_value = coint_res[2][1]

    model = sm.OLS(series_0, series_1).fit()
    hedge_ratio = model.params[0] # coeff

    spread_series = calculate_spread(series_0, series_1, hedge_ratio)
    zero_crossings = len( np.where( np.diff(np.sign(spread_series)))[0])

    if p_value < 0.05 and t_value < c_value:
        is_cointegrated = True

    return (is_cointegrated,
            round(t_value, 2),
            round(p_value, 2),
            round(c_value, 2),
            round(hedge_ratio, 2),
            zero_crossings)
