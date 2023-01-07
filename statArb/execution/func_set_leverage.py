def set_leverage(session, ticker_0, ticker_1):
    try:
        session.cross_isolated_margin_switch(
            symbol=ticker_0,
            is_isolated=True,
            buy_leverage='1',
            sell_leverage='1')
    except:
        pass

    try:
         session.cross_isolated_margin_switch(
       symbol=ticker_1,
       is_isolated=True,
       buy_leverage='1',
       sell_leverage='1')
    except:
        pass