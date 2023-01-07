from time import  sleep

import pybit.usdt_perpetual

from config import session_auth, session_public
from config import ws
from config import  signal_tresh, close_tresh
from config import  tradeable_capital_usdt

from func_set_leverage import set_leverage
from func_place_trades import place_buy, place_short
from func_get_latest_pair import get_latest_pair_with_hedge_ratio
from func_get_orderbook_mid_prices import  get_orderbook_mid_prices
from func_evaluate_signal import  evaluate_trade_signal, evaluate_close_signal

# Get the pair with the most zero crossings
ticker_0, ticker_1, hedge_ratio = get_latest_pair_with_hedge_ratio()

# Set the leverage settings
set_leverage(session_auth, ticker_0, ticker_1)

# Get the latest Z-Score
zscore = 2 # Replace with fetching the real value
qty_ratio = 0.1

# Check Z-Score against signal
canTrade, longTicker = evaluate_trade_signal(ticker_0, ticker_1, zscore, signal_tresh)

# wait for latest stream to perform trade
latest_ticker_0_orderbook_data = {}
latest_ticker_1_orderbook_data = {}

def check_open_position(ticker):
    return False

def check_active_position(ticker):
    return False

def get_latest_zscore(ticker_0, ticker_1):
    return 2

def open_positions(ticker_0, ticker_1, zscore, capital):
    order_id = 0
    return order_id

def close_all_positions():
    return True
def handle_orderbook_stream(message):
    global latest_ticker_0_orderbook_data, latest_ticker_1_orderbook_data
    data = message["data"]
    dict = get_orderbook_mid_prices(data)

    if dict["ticker"] == ticker_0:
        latest_ticker_0_orderbook_data = dict
    else:
        latest_ticker_1_orderbook_data = dict

if __name__ == "__main__":
    ws.orderbook_25_stream(handle_orderbook_stream, ticker_0)
    ws.orderbook_25_stream(handle_orderbook_stream, ticker_1)

    print("Bot initiating...")
    while True:
        sleep(3) # Protect API

        print("Checking for any open or positions...")
       # If no active orders and we have capital, get and set latest pair and its latest z-score

        ticker_0_open_position_check = check_open_position(ticker_0)
        ticker_0_active_position_check = check_active_position(ticker_1)

        ticker_1_open_position_check = check_open_position(ticker_0)
        ticker_1_active_position_check = check_active_position(ticker_1)

        position_checks = [ticker_0_open_position_check, ticker_0_active_position_check, ticker_1_open_position_check, ticker_1_active_position_check]

        no_positions = not any(position_checks)

        latest_zscore = get_latest_zscore(ticker_0, ticker_1)
        print(f"latest zscore: {latest_zscore}")

        if no_positions: # if there are no open positions
            print("No open or active positions...")
            print("Checking for capital...")
            if tradeable_capital_usdt > 0:
                print(f"capital OK: {tradeable_capital_usdt}")

                if latest_zscore >= signal_tresh:
                    print(f"latest zscore: {latest_zscore} crossed threshold {signal_tresh}")

                    print(f"opening positions")
                    open_positions(ticker_0, ticker_1, latest_zscore, tradeable_capital_usdt)
                else:
                    print(f"Waiting for z-score {latest_zscore} to cross threshold {signal_tresh}")
            else:
                print(f"Not enough capital: {tradeable_capital_usdt}")
                continue

        else: # if there a open positions
            print("Positions currently open or active...")
            print("Checking for capital...")
            if tradeable_capital_usdt == 0:
                print(f"Not enough capital: {tradeable_capital_usdt}")
                continue

            elif tradeable_capital_usdt > 0:
                print(f"Still got capital: {tradeable_capital_usdt}")
                if latest_zscore >= signal_tresh:
                    print(f"latest zscore: {latest_zscore} crossed threshold {signal_tresh}")

                    print(f"opening new positions with remaining capital")
                    open_positions(ticker_0, ticker_1, latest_zscore, tradeable_capital_usdt)

                elif latest_zscore < signal_tresh:
                    if int(latest_zscore) == 0:
                        print("Zscore reverted to 0, closing all positions!")
                        close_all_positions()
                    else:
                        print("Zscore no longer crossing the treshold and not mean reverted, waiting...")
                        continue

def get_quantity(ticker):
    pass
def monitor_place_trades():
    global trades_placed
    # Place trades
    if trades_placed == False:
        if canTrade:
            if longTicker == ticker_0:
                place_buy(ticker_0, mid_price)
                place_short(ticker_1, mid_price)
            elif longTicker == ticker_1:
                place_buy(ticker_1, mid_price)
                place_short(ticker_0, mid_price)

            trades_placed = True

def monitor_close_trades():
    global trades_placed

    if trades_placed == True:
        evaluate_close_signal(ticker_0, ticker_1, zscore, close_tresh)


get_quantity(ticker_0)

# while True:
#     sleep(1)