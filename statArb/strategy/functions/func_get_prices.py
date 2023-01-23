from strategy.functions.func_get_close_prices import get_close_prices_and_vol
from state import  kline_limit


def get_price_history_for_tickers(symbols):

  # Get prices and store in Dataframe
  price_data_list = []

  # Get prices and store
  for count, sym in enumerate(symbols):
    print(f"{count+1}/{len(symbols)}")
    symbol_name = sym["name"]
    price_history, avg_vol = get_close_prices_and_vol(symbol_name)


    if len(price_history) == kline_limit:
      price_data_list.append(
        {
          "symbol": symbol_name,
          "prices": price_history,
          "avg_vol": avg_vol
        }
      )

  sorted_dict = sorted(price_data_list, key=lambda x: x["avg_vol"], reverse=True)
  filtered_list = sorted_dict[:20]


  return filtered_list




