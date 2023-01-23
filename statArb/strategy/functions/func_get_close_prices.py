import datetime
import time

from state import session_public
from state import timeframe
from state import kline_limit

"""
    interval: 60, "D"
    from: integer from timestamp in seconds
    limit: max size of 200
"""

# GET start times



def get_close_prices_and_vol(symbol):
    time_start_date = 0

    if timeframe == 60:
        time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
    if timeframe == "D":
        time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)

    time_start_seconds = int(time_start_date.timestamp())

    prices = []
    volumes = [1]
    average_volume = 0

    prices_res = session_public.query_kline(
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
                # print(res)
                price_close = res["close"]
                price_volume = res["volume"]

                prices.append(price_close)
                volumes.append(price_volume)

                average_volume = sum(volumes)/len(volumes)

    return prices, average_volume

