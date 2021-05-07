import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import pandas as pd

from default_params import ts, mu, beta0, beta1s, mesh, peak_levels, starts_dict,\
    cases_duration, names, scatter_options, fig1_grid, t_on_max, \
    delta_t_max, data_dir
from model import simulate, normalize

y0 = [1 - 1 / 1000, 1 / 1000]

t_ons = np.linspace(0, 80, mesh)
durations = np.linspace(0, 80, mesh)


def plot_peak_for_t(beta1, fig_name=None, save_fig=True, data_name=None):
    i_maxs = np.zeros((t_ons.size, durations.size))
    for i, t_on in enumerate(tqdm(t_ons)):
        for j, duration in enumerate(durations):
            ss, i_s, rs = simulate(ts, y0, mu, beta0, beta1, start=t_on,
                                   end=t_on + duration)
            i_maxs[i, j] = i_s.max()

    plt.subplot(fig1_grid[2:6, 4:])
    plt.contourf(t_ons, durations, normalize(i_maxs.T), levels=peak_levels)
    plt.colorbar()
    starts = starts_dict[beta1]
    delta_ts = [cases_duration for _ in starts]
    plt.scatter([0] + starts, [0] + delta_ts, **scatter_options)
    plt.xlim([-2, t_on_max])
    plt.ylim([-2, delta_t_max])

    if save_fig:
        plt.tight_layout()
        plt.savefig(f"i_max_phase_diagram_{fig_name}.pdf")
        plt.show()

    if data_name is not None:
        df = pd.DataFrame()
        df['t_on'] = t_ons.reshape((-1, 1)).repeat(durations.size, 1).flatten()
        df['duration'] = durations.reshape((1, -1)).repeat(t_ons.size, 0).flatten()
        df['i_max'] = i_maxs.flatten()
        df.to_csv(f'{data_dir}{data_name}_i_max_for_t.csv', index=False)


def main():
    for beta1, name in zip(beta1s, names):
        plot_peak_for_t(beta1, name)


if __name__ == '__main__':
    main()
