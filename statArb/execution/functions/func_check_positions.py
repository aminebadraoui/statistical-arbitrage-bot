from config import session_auth

def check_open_positions(ticker):
    try:
        position =  session_auth.my_position(symbol=ticker)

        if position["ret_msg"] == "OK":
            for item in position["result"]:
                if item["size"] > 0:
                    return True
                else:
                    return False
    except Exception as e:
        print(e)
        return False




def check_active_positions(ticker):
    active_order = session_auth.get_active_order(
        symbol=ticker,
        order_status="Created,New,PartiallyFilled,Active"
    )

    if active_order["ret_msg"] == "OK":
        if active_order["result"]["data"] != None:
            return True
        else:
            return False

def get_position_info(ticker):

    # Declare output variables
    side = 0
    size = ""

    # Extract position info
    position = session_auth.my_position(symbol=ticker)
    if "ret_msg" in position.keys():
        if position["ret_msg"] == "OK":
            if len(position["result"]) == 2:
                if position["result"][0]["size"] > 0:
                    size = position["result"][0]["size"]
                    side = "Buy"
                else:
                    size = position["result"][1]["size"]
                    side = "Sell"

    # Return output
    return side, size


