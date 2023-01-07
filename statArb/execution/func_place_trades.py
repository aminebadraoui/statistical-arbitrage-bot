from config import session_auth
def place_buy(ticker, qty, price, sl):
    print(f"placed buy on { ticker } at price { price }")

    session_auth.place_active_order(
    symbol=ticker,
    side="Buy",
    order_type="Limit",
    qty=qty,
    price=price,
    time_in_force="GoodTillCancel",
    reduce_only=False,
    close_on_trigger=False)

def place_short(ticker, qty, price, sl):
    print(f"placed short on { ticker } at price { price }")

    session_auth.place_active_order(
    symbol=ticker,
    side="Sell",
    order_type="Limit",
    qty=qty,
    price=price,
    time_in_force="GoodTillCancel",
    reduce_only=False,
    close_on_trigger=False)