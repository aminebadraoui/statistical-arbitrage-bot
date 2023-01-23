from state import  session_auth
from risk_management.kelly_criterion import  get_kelly_size
import state


win_stat = 0.2
avg_win = 100
avg_loss = 50


def get_balance():
    res = session_auth.get_wallet_balance(coin="USDT")

    balance = res["result"]["USDT"]["available_balance"]

    return balance

def set_risk_margins(number_of_pairs):
    balance = get_balance()
    RR = avg_win / avg_loss
    kelly_size =  get_kelly_size(win_stat,avg_win,avg_loss)
    risk_margin = balance * kelly_size
    margin_pair = risk_margin
    risk_long = margin_pair / 2
    risk_short =  margin_pair - risk_long
    sl = RR * kelly_size
    tp = RR * sl
    leverage_multiplier = 1 / kelly_size

    state.balance = balance
    state.kelly_size =  kelly_size
    state.risk_margin = risk_margin
    state.margin_pair = margin_pair
    state.risk_long = risk_long
    state.risk_short = risk_short
    state.sl = sl
    state.tp = tp
    state.leverage_multiplier = leverage_multiplier

    return kelly_size, risk_margin, risk_long, risk_short, sl, tp
