"""
API Documentation
https://bybit-exchange.github.io/docs/futuresV2/linear/#t-introduction
"""

# API Imports
from pybit import usdt_perpetual



# CONFIG
mode = "test"
timeframe = 60
kline_limit = 200
z_score_window = 21

# Live API
api_key_mainnet = ""
api_secret_mainnet = ""

# Testnet API
api_key_testnet = "BnSPERz520rL7BykyW"
api_secret_testnet = "K76SWz5fpuizU0wleR3MlrZfPk07ttbtvJM3"

# Selected API
api_key = api_key_mainnet if mode == "prod" else api_key_testnet
api_secret = api_secret_mainnet if mode == "test" else api_secret_testnet

# Selected URL
api_url = "https://api.bybit.com" if mode == "prod" else "https://api-testnet.bybit.com"

# Session activation
session = usdt_perpetual.HTTP(endpoint=api_url,
                              api_key=api_key,
                              api_secret=api_secret)


