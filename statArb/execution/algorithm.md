compute the most cointegrated pairs

classify by cointegration, spread mean reversion, 
correlation, volatility, spread, liquidity. 

select the 10 first pairs

store them in csv 

write report

Every 5min:
    first check balance
    set the criteria
    if active order:
        check if zscore back to zero => close all
        check if total pnl < loss limit => close all
    if no order:
        for pair in pairs:
            if hot => place positions + check next pair
            if cold => check next pair
            
        
    


check if zcore is 0:
 check latest z-score for pair 1 if pass threshold 
    if yes, open new position
    if not move to next pair
    repeat same for next pair
    
    