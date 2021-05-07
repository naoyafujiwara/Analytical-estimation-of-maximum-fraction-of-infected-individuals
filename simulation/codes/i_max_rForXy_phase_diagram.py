import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import pandas as pd

from model import simulate, normalize, r_on_and_delta_r
from default_params import mesh, t_ons, beta0, beta1s, mu, durations, cmap, \
    peak_levels, starts_dict, cases_duration, panel_width, scatter_options,\
    names, fig1_grid, ts_for_r, peak_levels_theory_figS1,\
    peak_levels_theory_figS2, figS1_grid, data_dir
from i_max_theory import plot_theory

y0 = [1 - 1 / 1000, 1 / 1000]


def plot_peak_for_r(beta1, fig_name=None, save_fig=True, theory=False,
                    data_name=None):
    if save_fig:
        plt.figure(figsize=(panel_width * 5, panel_width * 5))
    xs = np.zeros(shape=(mesh, mesh))
    ys = np.zeros_like(xs)
    
    i_maxs = np.zeros((t_ons.size, durations.size))
    for i, t_on in enumerate(tqdm(t_ons)):
        for j, duration in enumerate(durations):
            ss, i_s, rs = simulate(ts_for_r, y0, mu, beta0, beta1, start=t_on,
                                   end=t_on + duration)
            i_maxs[i, j] = i_s.max()
            t_length = rs.size
            mask_on = (ts_for_r >= t_on)[:t_length]
            xs[i, j] = rs[mask_on][0]
            mask_off = (ts_for_r >= t_on + duration)[:t_length]
            ys[i, j] = rs[mask_off][0]
    
    ys = ys - xs
    if theory:
        # figS1
        plt.subplot(figS1_grid[0, 0])
        levels = peak_levels_theory_figS1 if beta1 > mu else \
            peak_levels_theory_figS2
        plt.contourf(xs, ys, i_maxs, levels=levels, cmap=cmap)
        plot_theory(beta1, levels[1:-1], phase_boundary=False)
    else:
        # fig1
        plt.subplot(fig1_grid[2:6, :4])
        levels = peak_levels
        plt.contourf(xs, ys, normalize(i_maxs), levels=levels, cmap=cmap)
        r_on_scatters, delta_r_scatters = r_on_and_delta_r(starts_dict[beta1],
                                                           cases_duration, ts_for_r, y0,
                                                           mu, beta0, beta1)
        plt.scatter(r_on_scatters, delta_r_scatters, **scatter_options)
        plot_theory(beta1, [])
    
    y_lim = 0.3 if beta1 < mu else 0.6
    plt.ylim([0, y_lim])
    plt.xlim([0, 0.8])
    plt.tight_layout()
    if theory:
        plt.title("i_max")
        plt.xlabel("r_on")
        plt.ylabel("Δr")
        plt.colorbar()
    
    if save_fig:
        plt.colorbar()
        plt.savefig(f"i_max_rForXy_phase_diagram_{fig_name}.pdf")
        plt.show()
        
    if data_name is not None:
        df = pd.DataFrame()
        df['x'] = xs.flatten()
        df['y'] = ys.flatten()
        df['i_max'] = i_maxs.flatten()
        df.to_csv(f'{data_dir}{data_name}_i_max.csv', index=False)
    
    
def main():
    for beta1, name in zip(beta1s[1:], names[1:]):
        plot_peak_for_r(beta1, name)


if __name__ == '__main__':
    main()
