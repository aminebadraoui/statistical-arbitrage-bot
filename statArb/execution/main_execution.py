from time import  sleep
from datetime import datetime, timedelta

from strategy.pair_scanner import refreshCointegratedPairs

from state import session_auth
from state import ws
from state import  signal_tresh
from state import should_refresh
import state

from risk_management.risk_config import set_risk_margins

from execution.functions.func_set_leverage import set_leverage
from execution.functions.func_open_new_positions import open_new_positions
from execution.functions.func_get_latest_pair import get_latest_pair_with_hedge_ratio
from execution.functions.func_get_orderbook_mid_prices import  get_orderbook_mid_prices
from execution.functions.func_check_positions import is_position_active_or_open, get_position_info
from execution.functions.func_get_latest_zscore import get_latest_zscore
from execution.functions.func_close_all_positions import close_position
from strategy.functions.func_cointegration import get_uid


orderbook_data = {}
open_tickers = {}

last_refresh_time = datetime.now()
refresh_delta = timedelta(minutes=30)

def handle_orderbook_stream(message):
    data = message["data"]
    symbol_orderbook = get_orderbook_mid_prices(data)
    symbol = symbol_orderbook["symbol"]

    orderbook_data[symbol] = symbol_orderbook

def update_tickers(fetch):
    if fetch:
        refreshCointegratedPairs()

def log_balance_state():
    print(
        f"Capital: {state.balance} "
        f"Kelly Size: {state.kelly_size} "
        f"// optimal leverage multiplier: {state.leverage_multiplier} "
        f"// stop loss: {state.sl} "
        f"// take profit: {state.tp}"
        f"Available risk margin: {state.risk_margin} "
    )

def updateMarginIfAllowed():
    if len(state.latest_cointegrated_pairs) > 0:
        number_of_pairs = len(state.latest_cointegrated_pairs)
        set_risk_margins(number_of_pairs)
        print("risk_margins reset")
    else:
        print("No cointegrated pairs")

    log_balance_state()

if __name__ == "__main__":
    update_tickers(should_refresh)
    while True:
        print(f"open tickers: { open_tickers}")
        # check if any position or order open (array in json)

        # if no position => reset margin

        # check refresh
        if  datetime.now() >= last_refresh_time + refresh_delta:
            print("Refresh...")
            update_tickers(should_refresh)
            last_refresh_time = datetime.now()

        for pair in state.latest_cointegrated_pairs:
            ticker_0 = pair["ticker_0"]
            ticker_1 = pair["ticker_1"]
            uid = get_uid(ticker_0, ticker_1)

            # check if symbol exist in orderbook, if not subscribe
            if ticker_0 in orderbook_data:
                pass
            else:
                orderbook_data[ticker_0] = {}
                ws.orderbook_25_stream(handle_orderbook_stream, ticker_0)

            if ticker_1 in orderbook_data:
                pass
            else:
                orderbook_data[ticker_1] = {}
                ws.orderbook_25_stream(handle_orderbook_stream, ticker_1)

            # if no data for ticker, continue to next ticker
            if len(orderbook_data[ticker_0]) == 0:
                continue
            if len(orderbook_data[ticker_1]) == 0:
                continue

            orderbook_data_0 = orderbook_data[ticker_0]
            orderbook_data_1 = orderbook_data[ticker_1]

            # check latest zscore
            zscore, signal = get_latest_zscore(orderbook_data_0, orderbook_data_1)

            if signal == "CROSSED":
                print(f"{ticker_0} / {ticker_1}:  z-score {zscore} crossed threshold {signal_tresh}")

                log_balance_state()

                # check margin + place trades + update margin
                positions_open = False
                for ticker in open_tickers.keys():
                    side, size = get_position_info(ticker)
                    if size > 0:
                        print("positions already open")
                        positions_open = True
                        break

                if positions_open == False:
                    updateMarginIfAllowed()

                if state.risk_margin/state.margin_pair >= 1 and state.risk_margin > 0:
                    print(f"{ticker_0} / {ticker_1}: Setting Leverage")
                    set_leverage(session_auth, ticker_0, ticker_1)

                    print(f"{ticker_0} / {ticker_1}: Opening Positions")

                    order_long, order_short = open_new_positions(orderbook_data_0,
                                                                     orderbook_data_1,
                                                                     zscore)
                    ticker_orders = []
                    qty_0 = 0
                    qty_1 = 0
                    if order_long["success"] == True:
                        ticker_orders.append(order_long)
                        if order_long["symbol"] == ticker_0:
                            qty_0 = order_long["qty"]
                        else:
                            qty_1 = order_long["qty"]

                        state.risk_margin -= state.risk_long
                        state.risk_long = state.margin_pair / 2

                        if ticker_0 in open_tickers.keys():
                            if uid in open_tickers[ticker_0].keys():
                                existing_qty = open_tickers[ticker_0][uid]["qty"]
                                open_tickers[ticker_0][uid]["qty"] = existing_qty + qty_0

                            else:
                                open_tickers[ticker_0][uid] = qty_0
                        else:
                            open_tickers[ticker_0] = {
                                uid: {
                                    "qty": qty_0
                                }
                            }

                    if order_short["success"]== True:
                        ticker_orders.append(order_short)
                        if order_long["symbol"] == ticker_1:
                            qty_0 = order_long["qty"]
                        else:
                            qty_1 = order_long["qty"]

                        state.risk_margin -= state.risk_short
                        state.risk_short = state.margin_pair - state.risk_long

                        if ticker_1 in open_tickers.keys():
                            if uid in open_tickers[ticker_1].keys():
                                existing_qty = open_tickers[ticker_1][uid]["qty"]
                                open_tickers[ticker_1][uid]["qty"] = existing_qty + qty_1

                            else:
                                open_tickers[ticker_1][uid] = qty_1
                        else:
                            open_tickers[ticker_1] = {
                                uid: {
                                    "qty": qty_1
                                }
                            }

                    else:
                        print("Not enough margin")
                        log_balance_state()

            elif signal == "WAIT":
                # continue to next pair
                print(f"{ticker_0} / {ticker_1}: Waiting for z-score {zscore} to cross threshold {signal_tresh}")
                continue

            elif signal == "CLOSE":
                print(f"{ticker_0} / {ticker_1}:  Zscore reverted to 0, closing all get_positions.py!")

                if ticker_0 in open_tickers.keys():
                    ticker_0_orders = open_tickers[ticker_0]
                    if uid in ticker_0_orders.keys():
                        qty_0 = ticker_0_orders[uid]["qty"]
                        close_position(ticker_0, qty_0)
                        session_auth.cancel_all_active_orders(symbol=ticker_0)
                        del ticker_0_orders[uid]

                if ticker_1 in open_tickers.keys():
                    ticker_1_orders = open_tickers[ticker_1]
                    if uid in ticker_1_orders.keys():
                        qty_0 = ticker_1_orders[uid]["qty"]
                        close_position(ticker_1, qty_0)
                        session_auth.cancel_all_active_orders(symbol=ticker_1)
                        del ticker_1_orders[uid]

                sleep(5)
                continue

        print("Pausing for 30 secs...")
        sleep(30)