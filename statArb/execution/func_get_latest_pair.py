import pandas as pd

def get_latest_pair_with_hedge_ratio():
    global ticker_0
    global ticker_1
    global hedge_ratio

    dataframe = pd.read_csv("../strategy/cointegrated_tickers.csv")
    firstRow = dataframe.loc[0]

    ticker_0 = firstRow["Ticker 1"]
    ticker_1 = firstRow["Ticker 2"]
    hedge_ratio = firstRow["Hedge Ratio"]

    return (ticker_0, ticker_1, hedge_ratio)