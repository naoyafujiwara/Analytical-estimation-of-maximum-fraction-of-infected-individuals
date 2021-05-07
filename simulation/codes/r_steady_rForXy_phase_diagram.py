import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import pandas as pd

from default_params import ts_for_r, mu, beta0, beta1s, mesh, t_ons,\
    durations, cmap, names, starts_dict, cases_duration, scatter_options,\
    r_steady_levels, fig1_grid, figS1_grid, r_steady_levels_theory, data_dir
from model import simulate, normalize, r_on_and_delta_r
from theory_r_steady import plot_theory

y0 = [1 - 1 / 1000, 1 / 1000]


def plot_r_steady_for_r(beta1, fig_name=None, save_fig=True, theory=False,
                        data_name=None):
    xs = np.zeros(shape=(mesh, mesh))
    ys = np.zeros_like(xs)

    r_steady_s = np.zeros((t_ons.size, durations.size))
    for i, t_on in enumerate(tqdm(t_ons)):
        for j, duration in enumerate(durations):
            ss, i_s, rs = simulate(ts_for_r, y0, mu, beta0, beta1, start=t_on,
                                   end=t_on + duration)
            r_steady_s[i, j] = rs[-1]
            t_length = rs.size
            mask_on = (ts_for_r >= t_on)[:t_length]
            xs[i, j] = rs[mask_on][0]
            mask_off = (ts_for_r >= t_on+duration)[:t_length]
            ys[i, j] = rs[mask_off][0]
    ys = ys - xs

    if theory:
        plt.subplot(figS1_grid[1, 0])
        levels = r_steady_levels_theory
        plt.contourf(xs, ys, r_steady_s, levels=levels, cmap=cmap)
        plot_theory(beta1, levels[1:-1])
    else:
        plt.subplot(fig1_grid[6:, :4])
        levels = r_steady_levels
        plt.contourf(xs, ys, normalize(r_steady_s), levels=levels, cmap=cmap)
        r_on_scatters, delta_r_scatters = r_on_and_delta_r(starts_dict[beta1], cases_duration, ts_for_r, y0, mu, beta0, beta1)
        plt.scatter(r_on_scatters, delta_r_scatters, **scatter_options)

    if theory:
        plt.title("r(∞)")
        plt.xlabel("r_on")
        plt.ylabel("Δr")
        plt.colorbar()
        
    plt.xlim([0, 0.8])
    if beta1 < mu:
        plt.ylim([0, 0.3])
    else:
        plt.ylim([0, 0.6])

    if save_fig:
        plt.tight_layout()
        plt.savefig(f"phase_diagram_r_steady_rForXy_{fig_name}.pdf")
        plt.show()

    if data_name is not None:
        df = pd.DataFrame()
        df['x'] = xs.flatten()
        df['y'] = ys.flatten()
        df['r_steady'] = r_steady_s.flatten()
        df.to_csv(f'{data_dir}{data_name}_r_steady.csv', index=False)


def main():
    for beta1, name in zip(beta1s, names):
        plot_r_steady_for_r(beta1, name)


if __name__ == '__main__':
    main()
