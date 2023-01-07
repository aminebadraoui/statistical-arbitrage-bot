import datetime
import time

from config import session_auth
from config import timeframe
from config import kline_limit

"""
    interval: 60, "D"
    from: integer from timestamp in seconds
    limit: max size of 200
"""

# GET start times

time_start_date = 0

if timeframe == 60:
    time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
if timeframe == "D":
    time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)

time_start_seconds = int(time_start_date.timestamp())

def get_price_klines(symbol):
    prices = []

    prices_res = session_auth.query_mark_price_kline(
        symbol = symbol,
        interval = timeframe,
        limit=kline_limit,
        from_time = time_start_seconds
    )
    time.sleep(0.1)

    if prices_res["ret_msg"] == "OK":
        prices_result = prices_res["result"]

        if len(prices_result) == kline_limit:
            for res in prices_result:
                price_close = res["close"]
                prices.append(price_close)

    return prices

