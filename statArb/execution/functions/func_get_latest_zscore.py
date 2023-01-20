from strategy.functions.func_get_close_prices import get_close_prices_and_vol
from strategy.functions.func_cointegration import compute_pair_stats
def get_latest_zscore(ticker_0, ticker_1, latest_orderbook_price_0, latest_orderbook_price_1):
    # get latest prices
    close_prices_0, avg_vol_1 = get_close_prices_and_vol(ticker_0)
    close_prices_1, avg_vol_1 = get_close_prices_and_vol(ticker_1)

    close_prices_0 = close_prices_0[:-1]
    close_prices_1 = close_prices_1[:-1]

    close_prices_0.append(latest_orderbook_price_0)
    close_prices_1.append(latest_orderbook_price_1)

    stats = compute_pair_stats(ticker_0, ticker_1, close_prices_0, close_prices_1)

    print(stats)
    latest_zscore = stats["z_scores"][-1]

    return latest_zscore