import strategy.pair_scanner as pair_scanner
import state


if __name__ == "__main__":
    print("Bot initiating")

    """ Pair Scanner to be ran every 60min """

    if state.cointegrated_pairs == [] || state.hasRefreshPassed:
    pair_scanner.refreshCointegratedPairs()

    """ Bot to be ran every 5min """
    # Every 5min:
    #     first check balance
    #     set the criteria
    #     if active order:
    #         check if zscore back to zero => close all
    #         check if total pnl < loss limit => close all
    #     if no order:
    #         for pair in pairs:
    #             if hot => place get_positions.py + check next pair
    #             if cold => check next pair
