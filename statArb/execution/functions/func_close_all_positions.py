from state import session_auth
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


def close_position(ticker, qty):
    # Get position information
    side, size = get_position_info(ticker)

    if size > 0:
        new_side = ""

        if side == "Buy":
            new_side = "Sell"
        else:
            new_side = "Buy"

        place_market_close_order(ticker, new_side, min(qty,size))