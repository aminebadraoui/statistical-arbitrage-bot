from config import session_auth
import config

def place_buy(ticker, qty, price, sl, tp):
    success_long = False
    print(f"placed buy on { ticker } for a quantity of {qty} at price { price } for tp at { tp }")
    try:
        order = session_auth.place_active_order(
            symbol=ticker,
            side="Buy",
            order_type="Limit",
            qty=qty,
            price=price,
            time_in_force="PostOnly",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss=sl,
            take_profit = tp
        )

        success_long = True
    except Exception as e:
        print(e)
        pass

    return success_long

def place_short(ticker, qty, price, sl, tp):
    success_short = False

    print(f"placed short on { ticker } for a quantity of {qty} at price { price } for tp at { tp }")
    try:
        order = session_auth.place_active_order(
            symbol=ticker,
            side="Sell",
            order_type="Limit",
            qty=qty,
            price=price,
            time_in_force="PostOnly",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss = sl,
            take_profit = tp
        )

        success_short = True
    except Exception as e:
        print(e)
        pass

    return success_short

def open_new_positions(ticker_0,
                       ticker_1,
                       price_0,
                       price_1,
                       capital_long,
                       capital_short,
                       qty_0_rounding,
                       qty_1_rounding,
                       sl_0,
                       sl_1,
                       tp_0,
                       tp_1,
                       zscore):
    success_long = False
    success_short = False

    try:
        session_auth.position_mode_switch(
            symbol=ticker_0,
            mode="BothSide"
            )
    except Exception as e:
        print(e)
        pass

    try:
        session_auth.position_mode_switch(
            symbol=ticker_1,
            mode="BothSide"
        )
    except Exception as e:
        print(e)
        pass


    if zscore < 0:
        qty_0 = round(capital_long / price_0, qty_0_rounding)
        success_long = place_buy(ticker_0, qty_0, price_0, sl_0, tp_0)

        qty_1 = round(capital_short / price_1, qty_1_rounding)
        success_short = place_short(ticker_1, qty_1, price_1, sl_1, tp_1)

    elif zscore > 0:
        qty_1 = round(capital_long / price_1, qty_1_rounding)
        success_long = place_buy(ticker_1, qty_1, price_1, sl_1, tp_1)

        qty_0 = round(capital_short / price_0, qty_0_rounding)
        success_short = place_short(ticker_0, qty_0, price_0, sl_0, tp_0)

    return success_long, success_short