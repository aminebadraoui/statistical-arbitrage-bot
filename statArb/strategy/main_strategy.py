import pandas as pd
import json
from matplotlib.backends.backend_pdf import PdfPages

from strategy.func_get_pairs import get_tickers
from strategy.func_get_prices import get_price_history_for_tickers
from strategy.func_cointegration import get_cointegrated_tickers
from strategy.func_cointegration import calculate_spread
from strategy.func_plot_trends import plot_data
from strategy.func_get_zscore import get_zscores

""" Strategy code """

if __name__ == "__main__":
    # Step 1 - Get the list of symbols
    print("Getting tickers...")
    tickers = get_tickers()

    # Step 2 - Get the price history for every symbol and store it
    print("Getting price history for all tickers....")
    if len(tickers) > 0:
        tickers_with_price = get_price_history_for_tickers(tickers)

        if len(tickers_with_price) > 0:
            with open("../price_list.json", "w") as jsonfile:
                json.dump(tickers_with_price, jsonfile, indent=4)

    # Step 3 - Compute the cointegrated pairs and save it
    print("Computing co-integration among every ticker...")
    with open("../price_list.json") as price_json:
        tickers_with_price_from_json = json.load(price_json)

        df_cointegrated_tickers = get_cointegrated_tickers(tickers_with_price_from_json)
        df_cointegrated_tickers = df_cointegrated_tickers.sort_values("Zero Crossings", ascending=False)
        df_cointegrated_tickers.to_csv("cointegrated_tickers.csv")

    # Step 4 -Plot trends and save it
    print("Plotting trends...")
    df_cointegrated_tickers_from_csv = pd.read_csv("cointegrated_tickers.csv")
    df_data = df_cointegrated_tickers_from_csv[["Ticker 1", "Ticker 2", "Hedge Ratio"]].head(15)

    print(df_data)

    with open("../price_list.json") as price_json:
        prices_data_from_json = json.load(price_json)

        if len(prices_data_from_json) > 0:
            figs = []
            for i in range(len(df_data)):
                ticker_0 = df_data.loc[i, "Ticker 1"]
                ticker_1 = df_data.loc[i, "Ticker 2"]
                hedge_ratio = df_data.loc[i, "Hedge Ratio"]

                price_history_0 = prices_data_from_json[ticker_0]
                price_history_1 = prices_data_from_json[ticker_1]

                spread = calculate_spread(price_history_0, price_history_1, hedge_ratio)
                zscore = get_zscores(spread)

                fig = plot_data(ticker_0, ticker_1, price_history_0, price_history_1, spread, zscore)

                figs.append(fig)

            print("Generating report...")
            with PdfPages("../report.pdf") as pdf:
                for fig in figs:
                    pdf.savefig(fig)

    """ Execution code """


