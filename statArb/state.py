"""
API Documentation
https://bybit-exchange.github.io/docs/futuresV2/linear/#t-introduction
"""
# API Imports
from pybit import usdt_perpetual

""" General Configuration """
mode = "test"

# Live API
api_key_mainnet = ""
api_secret_mainnet = ""

# Testnet API
api_key_testnet = "AOUjMeK81Ij1vuWwLw"
api_secret_testnet = "8tPcaFbC4jjh1qfdgy424Gv0WMegqlKiiulu"

# Selected API
api_key = api_key_mainnet if mode == "prod" else api_key_testnet
api_secret = api_secret_mainnet if mode == "prod" else api_secret_testnet

# Selected URL
api_url = "https://api.bybit.com" if mode == "prod" else "https://api-testnet.bybit.com"

# Websocket (Public)
ws = usdt_perpetual.WebSocket(test= (mode == "test"))

# Session activation
session_public = usdt_perpetual.HTTP(endpoint=api_url)
session_auth = usdt_perpetual.HTTP(endpoint=api_url,
                                   api_key=api_key,
                                   api_secret=api_secret)

""" Strategy specific configuration"""
# CONFIG
timeframe = 60
kline_limit = 200
z_score_window = 21

""" Execution specific configuration """
should_refresh = True
limit_order = True # Ensures all get_positions.py (except close) are limit orders, switch to False for maket orders

""" RISK """
risk_long = 0
risk_short = 0
risk_margin = 0
margin_pair = 0

balance = 0
kelly_size = 0
sl = 0
tp = 0
leverage_multiplier = 0

""" Signal """
signal_tresh = 1.1 # Z-Score tresh (absolute value)

latest_cointegrated_pairs = []

