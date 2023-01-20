from time import  sleep
from datetime import datetime, timedelta

from strategy.pair_scanner import refreshCointegratedPairs

from config import session_auth
from config import ws
from config import  signal_tresh
from config import should_refresh
import config

from execution.functions.func_set_leverage import set_leverage
from execution.functions.func_open_new_positions import open_new_positions
from execution.functions.func_get_latest_pair import get_latest_pair_with_hedge_ratio
from execution.functions.func_get_orderbook_mid_prices import  get_orderbook_mid_prices
from execution.functions.func_check_positions import  check_open_positions, check_active_positions
from execution.functions.func_get_latest_zscore import get_latest_zscore
from execution.functions.func_close_all_positions import close_all_positions

ticker_0 = ""
ticker_1 = ""

margin = 0
capital_long = 0
capital_short = 0

# wait for latest stream to perform trade
latest_ticker_0_orderbook_data = {}
latest_ticker_1_orderbook_data = {}

last_refresh_time = datetime.now()
refresh_delta = timedelta(minutes=30)
def handle_orderbook_stream(message):
    global latest_ticker_0_orderbook_data, latest_ticker_1_orderbook_data
    data = message["data"]
    dict = get_orderbook_mid_prices(data)

    if dict["ticker"] == ticker_0:
        latest_ticker_0_orderbook_data = dict
    else:
        latest_ticker_1_orderbook_data = dict

def update_margin():
    global margin
    global capital_long
    global capital_short

    # Margin stuff
    res = session_auth.get_wallet_balance(coin="USDT")

    config.balance = res["result"]["USDT"]["available_balance"]

    margin = config.balance * 0.01

    print(f"Current balance: {config.balance} USDT")
    print(f"Current margin: {margin} USDT")

    capital_long = margin / 2
    capital_short = margin - capital_long

def refresh(fetch):
    global ticker_0
    global ticker_1

    if fetch:
        refreshCointegratedPairs()

    # Get the pair with the most zero crossings
    ticker_0, ticker_1 = get_latest_pair_with_hedge_ratio()  # TODO: Replace with state variables

    sorted_ids = sorted(ticker_0 + ticker_1)
    uid = "".join(sorted_ids)

    if uid in checked_pairs:
        pass
    else:
        checked_pairs.append(uid)
        ws.orderbook_25_stream(handle_orderbook_stream, ticker_0)
        ws.orderbook_25_stream(handle_orderbook_stream, ticker_1)

    # Set the leverage settings
    set_leverage(session_auth, ticker_0, ticker_1)


checked_pairs = []

if __name__ == "__main__":
    refresh(should_refresh)

    print("Bot initiating...")
    while True:
        # check refresh
        if  datetime.now() >= last_refresh_time + refresh_delta:
            print("Time to refresh....")
            refresh(should_refresh)
            last_refresh_time = datetime.now()

        print("Bot running...")
        print(f"Current balance: {config.balance} USDT")
        print(f"Current margin: {margin} USDT")

        print(f"Checking for any open or positions for { ticker_0 } and { ticker_1 }")
       # If no active orders and we have capital, get and set latest pair and its latest z-score
        ticker_0_open_position_check = check_open_positions(ticker_0)
        ticker_0_active_position_check = check_active_positions(ticker_1)

        ticker_1_open_position_check = check_open_positions(ticker_0)
        ticker_1_active_position_check = check_active_positions(ticker_1)

        position_checks = [ticker_0_open_position_check, ticker_0_active_position_check, ticker_1_open_position_check, ticker_1_active_position_check]

        no_positions = not any(position_checks)

        mid_price_0 = latest_ticker_0_orderbook_data["mid_price"]
        mid_price_1 = latest_ticker_1_orderbook_data["mid_price"]
        qty_rounding_0 = latest_ticker_0_orderbook_data["qty_rounding"]
        qty_rounding_1 = latest_ticker_1_orderbook_data["qty_rounding"]
        price_rounding_0 = latest_ticker_0_orderbook_data["price_rounding"]
        price_rounding_1 = latest_ticker_1_orderbook_data["price_rounding"]

        latest_zscore = get_latest_zscore(ticker_0,
                                          ticker_1,
                                          mid_price_0,
                                          mid_price_1
                                          )

        print(f"latest zscore: {latest_zscore}")

        if latest_zscore < 0:
            print("zscore negative: We go long on ticker 0, short on ticker 1")
            sl_0 = round(mid_price_0 - (mid_price_0 * 0.15), price_rounding_0)
            tp_0 = round(mid_price_0 + (mid_price_0 * 0.30), price_rounding_0)

            sl_1 = round(mid_price_1 + (mid_price_1 * 0.15), price_rounding_1)
            tp_1 = round(mid_price_1 - (mid_price_1 * 0.30), price_rounding_1)

            print(f"price ticker_0 {mid_price_0}")
            print(f"TP ticker_0 {tp_0}")

            print(f"price ticker_1 {mid_price_1}")
            print(f"TP ticker_1 {tp_1}")


        else:
            print("zscore positive: We go long on ticker 1, short on ticker 0")
            sl_0 = round(mid_price_0 + (mid_price_0 * 0.15), price_rounding_0)
            tp_0 = round(mid_price_0 - (mid_price_0 * 0.30), price_rounding_0)

            sl_1 = round(mid_price_1 - (mid_price_1 * 0.15), price_rounding_1)
            tp_1 = round(mid_price_1 + (mid_price_1 * 0.30), price_rounding_1)

            print(f"price ticker_0 {mid_price_0}")
            print(f"TP ticker_0 {tp_0}")

            print(f"price ticker_1 {mid_price_1}")
            print(f"TP ticker_1 {tp_1}")




        if no_positions: # if there are no open positions
            print("No open or active positions...")
            update_margin()
            if margin >= capital_long + capital_short:
                if abs(latest_zscore) >= signal_tresh:
                    print(f"latest zscore: {latest_zscore} crossed threshold {signal_tresh}")

                    print(f"opening positions")
                    print(f"capital_long: {capital_long}")
                    print(f"capital_short: {capital_short}")

                    success_long, success_short = open_new_positions(ticker_0,
                                                                     ticker_1,
                                                                     mid_price_0,
                                                                     mid_price_1,
                                                                     capital_long,
                                                                     capital_long,
                                                                     qty_rounding_0,
                                                                     qty_rounding_1,
                                                                     sl_0,
                                                                     sl_1,
                                                                     tp_0,
                                                                     tp_1,
                                                                     latest_zscore)

                    if success_long:
                        margin -= capital_long
                    if success_short:
                        margin -= capital_short

                    capital_long = margin / 2
                    capital_short = margin - capital_long

                else:
                    print(f"Waiting for z-score {latest_zscore} to cross threshold {signal_tresh}")
            else:
                print(f"Not enough margin: {margin}")
                continue

        else: # if there a open positions
            print("Positions currently open or active...")
            print("Checking for capital...")
            if margin <= capital_long+capital_short:
                print(f"Not enough capital: {margin}")
                print(f"capital_long: {capital_long}")
                print(f"capital_short: {capital_short}")
                continue

            elif  margin >= capital_long+capital_short:
                print(f"margin: {margin}")
                print(f"capital_long: {capital_long}")
                print(f"capital_short: {capital_short}")
                if abs(latest_zscore) >= signal_tresh:
                    print(f"latest zscore: {latest_zscore} crossed threshold {signal_tresh}")
                    print(f"opening new positions with remaining capital")

                    success_long, success_short = open_new_positions(ticker_0,
                                                                     ticker_1,
                                                                     mid_price_0,
                                                                     mid_price_1,
                                                                     capital_long,
                                                                     capital_long,
                                                                     qty_rounding_0,
                                                                     qty_rounding_1,
                                                                     sl_0,
                                                                     sl_1,
                                                                     tp_0,
                                                                     tp_1,
                                                                     latest_zscore)

                    if success_long:
                        margin -= capital_long
                    if success_short:
                        margin -= capital_short

                    capital_long = margin / 2
                    capital_short = margin - capital_long

                    continue

                elif abs(latest_zscore) < signal_tresh:
                    if round(latest_zscore, 3) < 0.009:
                        print("Zscore reverted to 0, closing all positions!")
                        session_auth.cancel_all_active_orders(symbol=ticker_0)
                        session_auth.cancel_all_active_orders(symbol=ticker_1)

                        close_all_positions(ticker_0, ticker_1)
                        continue
                    else:
                        print("Zscore no longer crossing the threshold and not mean reverted, waiting...")
                        continue
        print("Pausing for 30 secs...")
        sleep(30)