def evaluate_trade_signal(ticker_0, ticker_1, zscore, tresh):
    can_trade = False
    long_ticker= ""

    if abs(zscore) >= tresh:
        can_trade = True

        if zscore > 0:
            long_ticker = ticker_1
        else:
            long_ticker = ticker_0

    return can_trade, long_ticker

def evaluate_close_signal(ticker_0, ticker_1, zscore, tresh):
    can_trade = False
    long_ticker= ""

    if abs(zscore) >= tresh:
        can_trade = True
        print(can_trade)

        if zscore > 0:
            long_ticker = ticker_1
        else:
            long_ticker = ticker_0

    return can_trade, long_ticker
