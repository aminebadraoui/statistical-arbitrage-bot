import pandas as pd

def get_latest_pair_with_hedge_ratio():
    dataframe = pd.read_csv("../generated/cointegrated_tickers.csv")
    firstRow = dataframe.loc[0]

    ticker_0 = firstRow["ticker_0"]
    ticker_1 = firstRow["ticker_1"]

    return (ticker_0, ticker_1)