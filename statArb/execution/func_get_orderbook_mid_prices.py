
def get_orderbook_mid_prices(data):
    bid_prices = []
    ask_prices = []
    ticker = ""

    # Classify data between Bids and Asks
    if len(data) > 0 :
        for level in data:
            price = level["price"]
            ticker = level["symbol"]
            if(level["side"] == "Buy"):
                bid_prices.append(price)
            if (level["side"] == "Sell"):
                ask_prices.append(price)

    # Sort bids and asks
    if len(bid_prices) > 0:
        bid_prices.sort(reverse=True) # Descending order so the first bid is the highest price

    if len(bid_prices) > 0:
        ask_prices.sort(reverse=False) # Ascending order so the first ask is the lowest price

    # Get mid-price
    nearest_bid = float(bid_prices[0])
    nearest_ask = float(ask_prices[0])

    mid_price = (float(nearest_ask) + float(nearest_bid)) / 2

    dict = {
        "ticker": ticker,
        "nearest_ask": nearest_ask,
        "nearest_bid": nearest_bid,
        "mid_price": mid_price
    }
    return dict





