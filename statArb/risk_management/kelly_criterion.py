def get_kelly_size(win_prob, avg_win,avg_loss):
    size = win_prob * (avg_win-avg_loss)/(avg_win+avg_loss)

    return  size