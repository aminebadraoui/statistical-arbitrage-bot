from state import session_auth
import state

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

        print(order)

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

        print(order)

        success_short = True
    except Exception as e:
        print(e)
        pass

    return success_short

def open_new_positions(ticker_0_data,
                       ticker_1_data,
                       zscore):
    success_long = False
    success_short = False

    ticker_0 = ticker_0_data["symbol"]
    ticker_1 = ticker_1_data["symbol"]

    price_0 = ticker_0_data["mid_price"]
    price_1 = ticker_1_data["mid_price"]

    qty_0_rounding = ticker_0_data["qty_rounding"]
    qty_1_rounding = ticker_1_data["qty_rounding"]

    price_rounding_0 = ticker_0_data["price_rounding"]
    price_rounding_1 = ticker_1_data["price_rounding"]

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

    order_long = {
        "symbol": "",
        "success": False,
        "qty": 0
    }

    order_short = {
        "symbol": "",
        "success": False,
        "qty": 0
    }

    if zscore < 0:
        print("zscore negative: We go long on ticker 0, short on ticker 1")
        order_long["symbol"] = ticker_0
        order_short["symbol"] = ticker_1

        qty_0 = state.risk_long / price_0
        order_long["qty"] = qty_0

        qty_1 = state.risk_short / price_1
        order_short["qty"] = qty_1

        sl_0 = round(price_0 - (price_0*state.sl), price_rounding_0)
        tp_0 = round(price_0 + (price_0*state.tp), price_rounding_0)

        sl_1 = round(price_1 + (price_1*state.sl), price_rounding_1)
        tp_1 = round(price_1 - (price_1*state.tp), price_rounding_1)

        # TODO perform liquidity check and pick the min
        success_long = place_buy(ticker_0, round(qty_0, qty_0_rounding), price_0, sl_0, tp_0)

        if success_long:
            order_long["success"] = True
        if success_short:
            order_short["success"] = True


        # TODO perform liquidity check and pick the min
        success_short = place_short(ticker_1, round(qty_1, qty_1_rounding), price_1, sl_1, tp_1)

    else:
        print("zscore positive: We go long on ticker 1, short on ticker 0")
        order_long["symbol"] = ticker_1
        order_short["symbol"] = ticker_0

        sl_0 = round(price_0 + (price_0 * state.sl), price_rounding_0)
        tp_0 = round(price_0 - (price_0 * state.tp), price_rounding_0)

        sl_1 = round(price_1 - (price_1 * state.sl), price_rounding_1)
        tp_1 = round(price_1 + (price_1 * state.tp), price_rounding_1)


        qty_1 = round(state.risk_long / price_1, qty_1_rounding)
        order_long["qty"] = qty_1

        # TODO perform liquidity check and pick the min
        success_long = place_buy(ticker_1, qty_1, price_1, sl_1, tp_1)

        qty_0 = round(state.risk_short / price_0, qty_0_rounding)
        order_short["qty"] = qty_0

        # TODO perform liquidity check and pick the min
        success_short = place_short(ticker_0, qty_0, price_0, sl_0, tp_0)


    if success_long:
        order_long["success"] = True
    if success_short:
        order_short["success"] = True

    return order_long, order_short