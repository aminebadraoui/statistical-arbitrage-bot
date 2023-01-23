
def get_orderbook_mid_prices(data):
    bid_prices = []
    ask_prices = []
    qty_rounding = 0
    price_rounding = 0
    ticker = ""

    # Classify data between Bids and Asks
    if len(data) > 0 :
        for level in data:
            price = level["price"]
            symbol = level["symbol"]
            size = level["size"]

            if len(str(size).split(".")) == 1:
                qty_rounding = 0
            else:
                 qty_rounding = len(str(size).split(".")[1])

            price_rounding = len(str(price).split(".")[1])

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

    rounded_mid_price = round(mid_price, price_rounding)

    dict = {
        "symbol": symbol,
        "nearest_ask": nearest_ask,
        "nearest_bid": nearest_bid,
        "mid_price": rounded_mid_price,
        "price_rounding": price_rounding,
        "qty_rounding": qty_rounding
    }
    return dict





