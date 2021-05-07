from collections import namedtuple

from matplotlib import pyplot as plt
import numpy as np

figs_dir = "../figs/"
data_dir = "../data/"

mesh = 401
cmap = "viridis"

t_ons = np.linspace(0, 100, mesh)
durations = np.linspace(0, 250, mesh)

t_max = t_ons.max(initial=0) + durations.max(initial=0)

ts = np.concatenate([np.linspace(0, 300, 300*1000)])
ts_for_optimisation = np.concatenate([np.linspace(0, 1000, 1000001)])
ts_for_r = np.concatenate([np.linspace(0, 200, 10001),
                           np.logspace(np.log10(201), np.log10(1000), 1001)])

mu = 1 / 7
beta0 = 2 * mu

names = ['low', 'high']
beta1_values = [.8 * mu, 1.4 * mu]
beta1s = namedtuple('beta1s', names)(*beta1_values)

peak_levels = np.linspace(0, 1, 201)
r_steady_levels = np.linspace(0.6, 1, 201)
peak_levels_theory_figS1 = np.arange(0.04, 0.18, 0.02)
peak_levels_theory_figS2 = np.arange(0.04, 0.18, 0.02)
r_steady_levels_theory = np.arange(0.5, 0.85, 0.05)

cases_duration = 60
starts_dict = {beta1_values[0]: [None, 12, 30.166, 42.681, 61],
               beta1_values[1]: [None, 10, 19.210, 33.429, 65]}

scatter_options = {"marker": "x", "c": "k", "s": 100}

panel_width = 4.1

fig1_grid = plt.GridSpec(10, 10)
figS1_grid = plt.GridSpec(2, 1)

t_on_max = 70
delta_t_max = 70

y0 = [1 - 1 / 1000, 1 / 1000]
