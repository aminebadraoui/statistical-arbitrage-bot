from config import session_auth
from execution.functions.func_check_positions import get_position_info

#  Place market close order
def place_market_close_order(ticker, side, size):

    # Close position
    session_auth.place_active_order(
        symbol=ticker,
        side=side,
        order_type="Market",
        qty=size,
        time_in_force="GoodTillCancel",
        reduce_only=True,
        close_on_trigger=False
    )

    # Return
    return


def close_all_positions(ticker_0, ticker_1):
    # Get position information
    side_1, size_1 = get_position_info(ticker_0)
    side_2, size_2 = get_position_info(ticker_1)

    if size_1 > 0:
        place_market_close_order(ticker_0, side_2, size_1)  # use side 2

    if size_2 > 0:
        place_market_close_order(ticker_1, side_1, size_2)  # use side 1