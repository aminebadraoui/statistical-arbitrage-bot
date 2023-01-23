import state


def set_leverage(session, ticker_0, ticker_1):
    try:
        session.cross_isolated_margin_switch(
            symbol=ticker_0,
            is_isolated=True,
            buy_leverage=state.leverage_multiplier,
            sell_leverage=state.leverage_multiplier)
    except Exception as e:
        print(e)
        pass

    try:
         session.cross_isolated_margin_switch(
       symbol=ticker_1,
       is_isolated=True,
       buy_leverage=state.leverage_multiplier,
       sell_leverage=state.leverage_multiplier)
    except Exception as e:
        print(e)
        pass

    try:
        session.set_leverage(
        symbol=ticker_0,
        buy_leverage=state.leverage_multiplier,
        sell_leverage=state.leverage_multiplier
        )
    except Exception as e:
        print(e)
        pass

    try:
        session.set_leverage(
         symbol=ticker_1,
            buy_leverage=state.leverage_multiplier,
            sell_leverage=state.leverage_multiplier
     )
    except Exception as e:
        print(e)
        pass