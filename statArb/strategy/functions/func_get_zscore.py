import pandas as pd
from config import z_score_window

# Compute zscore
def get_zscores(spread):
   df = pd.DataFrame(spread)

   x = df.rolling(window=1).mean()
   mean = df.rolling(window=z_score_window).mean()
   std = df.rolling(window=z_score_window).std()

   df["Z-Score"] = (x-mean)/std

   z_score_list = df["Z-Score"].astype(float).values

   return (z_score_list)

