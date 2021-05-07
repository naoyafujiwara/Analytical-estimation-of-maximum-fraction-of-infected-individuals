import matplotlib.pyplot as plt
import pandas as pd

from model import simulate
from default_params import ts, mu, beta0, beta1s, starts_dict, cases_duration,\
    panel_width, names, fig1_grid, y0, data_dir

optimal = 44


def plot_cases(beta1, fig_name=None, save_fig=True, data_name=None):
    if save_fig:
        plt.figure(figsize=(panel_width * 5, panel_width * 5))
    df = pd.DataFrame()
    
    starts = starts_dict[beta1]
    for i, start in enumerate(starts):
        end = start + cases_duration if start is not None else None
        ss, i_s, rs = simulate(ts, y0, mu, beta0, beta1, start=start, end=end)

        ax1 = plt.subplot(fig1_grid[0:2, 2*i:2*i+2])
        color = 'tab:orange'
        ax1.plot(ts, rs, label='r(t)', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        plt.ylim([0, 0.85])
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.plot(ts, i_s, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        plt.ylim([0, 0.17])
        if i == 0:
            ax1.set_ylabel('r(t)', color=color)
        elif i == 4:
            ax2.set_ylabel('i(t)', color=color)
        plt.axvspan(start, end, color="gray", alpha=0.3)
        if i == 0:
            df['t'] = ts
        df[f'start={start}'] = i_s
        
    if save_fig:
        plt.tight_layout()
        plt.savefig(f"cases_{fig_name}.pdf")
        plt.show()

    if data_name is not None:
        df.to_csv(f"{data_dir}{data_name}_cases.csv", index=False)


def main():
    for beta1, name in zip(beta1s[:], names):
        plot_cases(beta1, name)


if __name__ == '__main__':
    main()
