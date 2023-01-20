import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from strategy.functions.func_get_pairs import get_tickers
from strategy.functions.func_get_prices import get_price_history_for_tickers
from strategy.functions.func_cointegration import get_cointegrated_tickers
from strategy.functions.func_plot_trends import plot_data

import state

def classify_cointegrated_pairs(pairs):
    classified_cointegrated_pairs = []

    return classified_cointegrated_pairs
def refreshCointegratedPairs():
    # # Step 1 - Get the list of symbols
    print("Getting tickers...")
    tickers = get_tickers()

    # Step 2 - Get the price history for every symbol
    print("Getting price history for all tickers....")
    if len(tickers) > 0:
        tickers_with_price = get_price_history_for_tickers(tickers)

        # compute the most cointegrated pairs
        # classify by cointegration, spread mean reversion, correlation, volatility, spread, liquidity.
        # and return only the most performant
        print("Getting the most cointegrated tickers...")
        cointegrated_pairs = get_cointegrated_tickers(tickers_with_price)

        # store them in state variables
        state.latest_cointegrated_pairs = cointegrated_pairs

        # store in csv
        print("Exporting data into csv..")
        df_cointegrated_tickers = pd.DataFrame(state.latest_cointegrated_pairs)
        df_cointegrated_tickers.to_csv("../generated/cointegrated_tickers.csv")

        # Step 5 -Plot pairs data and save it
        print("Plotting trends...")
        figs = []

        for index, pair in enumerate(state.latest_cointegrated_pairs):
            if index < 11:
                ticker_0 = state.latest_cointegrated_pairs[index]["ticker_0"]
                ticker_1 = state.latest_cointegrated_pairs[index]["ticker_1"]

                spreads = state.latest_cointegrated_pairs[index]["spreads"]
                z_scores = state.latest_cointegrated_pairs[index]["z_scores"]
                close_prices_0 = state.latest_cointegrated_pairs[index]["close_prices_0"]
                close_prices_1 = state.latest_cointegrated_pairs[index]["close_prices_1"]

                fig = plot_data(ticker_0, ticker_1, close_prices_0, close_prices_1, spreads, z_scores)

                figs.append(fig)

        print("Generating report...")
        with PdfPages("../report.pdf") as pdf:
            for fig in figs:
                pdf.savefig(fig)

        print("Report generated successfully...")


