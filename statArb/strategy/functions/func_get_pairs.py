from state import  session_auth

# Get tradeable symbols

def get_tickers():
    sym_list = []
    symbols = session_auth.query_symbol()

    if "ret_msg" in symbols.keys():
        if symbols["ret_msg"] == "OK":
            symbols = symbols["result"]
            for symbol in symbols:
                if symbol["quote_currency"] == "USDT" and symbol["status"] == "Trading" :
                    sym_list.append(symbol)

    return sym_list