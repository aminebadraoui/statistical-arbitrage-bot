import pandas as pd
import matplotlib.pyplot as plt

# Plot prices
def plot_data(sym_0, sym_1, prices_close_0, prices_close_1, spread, zscore):
    fig, axs = plt.subplots(3,1,constrained_layout=True, figsize=(16,8))

    plt.suptitle = print(f"{sym_0} / { sym_1}")

    df = pd.DataFrame(columns=[sym_0, sym_1])
    df[sym_0] = prices_close_0
    df[sym_1] = prices_close_1
    df[f"{sym_0} delta"] = df[sym_0] / prices_close_0[0]
    df[f"{sym_1} delta"] = df[sym_1] / prices_close_1[1]

    delta_0 =  df[f"{sym_0} delta"].astype(float).values
    delta_1 = df[f"{sym_1} delta"].astype(float).values

    axs[0].plot(delta_0, color="BLUE")
    axs[0].plot(delta_1, color="ORANGE")
    axs[0].set_title(f"Prices for {sym_0} & { sym_1}")

    axs[1].plot(spread)
    axs[1].set_title("Spread")

    axs[2].plot(zscore)
    axs[2].set_title("Z-Score")

    plt.close()

    return fig


