import matplotlib.pyplot as plt
import numpy as np
from default_params import mu as gamma, beta0, beta1s


def plot_theory(beta1, levels=np.linspace(0.55, 0.8, 6)):
    for r_steady_value in levels:
        r_steady(r_steady_value, beta1)


def r_steady(r_steady_value, beta1):
    term = (1 - r_steady_value) / np.exp(-beta0 / gamma * r_steady_value)
    r_off_minus_r_on = np.log(term) / (beta0-beta1) * gamma
    if 0 < r_off_minus_r_on < 1:
        plt.hlines(r_off_minus_r_on, 0, 0.7, colors='k')


def debug():
    plot_theory(beta1s[1])
    plt.show()


if __name__ == "__main__":
    debug()
