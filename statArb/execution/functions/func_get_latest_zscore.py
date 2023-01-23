from strategy.functions.func_get_close_prices import get_close_prices_and_vol
from strategy.functions.func_cointegration import compute_pair_stats
import state

def get_latest_zscore(ticker_0_orderbook_data, ticker_1_orderbook_dadta):
    latest_zscore = 0
    signal = ""
    ticker_0 =  ticker_0_orderbook_data["symbol"]
    ticker_1 =  ticker_1_orderbook_dadta["symbol"]
    latest_orderbook_price_0 =  ticker_0_orderbook_data["mid_price"]
    latest_orderbook_price_1 = ticker_1_orderbook_dadta["mid_price"]

    # get latest prices
    close_prices_0, avg_vol_1 = get_close_prices_and_vol(ticker_0)
    close_prices_1, avg_vol_1 = get_close_prices_and_vol(ticker_1)

    close_prices_0 = close_prices_0[:-1]
    close_prices_1 = close_prices_1[:-1]

    close_prices_0.append(latest_orderbook_price_0)
    close_prices_1.append(latest_orderbook_price_1)

    stats = compute_pair_stats(ticker_0, ticker_1, close_prices_0, close_prices_1)

    if len(stats) > 0:
        if "z_scores" in stats:
            zscores = stats["z_scores"]
            if len(zscores) > 0:
                latest_zscore = zscores[-1]

                if abs(latest_zscore) >= state.signal_tresh:
                    signal = "CROSSED"
                elif abs(latest_zscore) < state.signal_tresh and round(abs(latest_zscore), 2) > 0.1:
                    signal = "WAIT"
                elif round(abs(latest_zscore), 2) < 0.1:
                    signal = "CLOSE"

    return latest_zscore, signal