from strategy.func_price_klines import get_price_klines
import json


def get_price_history_for_tickers(symbols):

  # Get prices and store in Dataframe
  price_history_dict = {}

  # Get prices and store
  for sym in symbols:
    symbol_name = sym["name"]
    price_history = get_price_klines(symbol_name)

    if len(price_history) > 0:
      price_history_dict[symbol_name] = price_history

  return price_history_dict




