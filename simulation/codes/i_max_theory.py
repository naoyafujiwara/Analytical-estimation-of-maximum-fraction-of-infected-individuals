import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root_scalar
from default_params import mu as gamma, beta0, beta1s


def plot_theory(beta1, levels=np.arange(0.06, 0.18, 0.02),
                phase_boundary=True):
    for i_max in levels:
        level_b(i_max, beta1)
        level_c(i_max, beta1)
        level_d(i_max, beta1)
        
    if phase_boundary:
        phase_a()
        phase_b(beta1)
        phase_c(beta1)
        phase_d(beta1)


boundary_b_a = gamma / beta0 * np.log(beta0 / gamma)


def boundary_c_b(beta1):
    return max(gamma / beta0 * np.log(beta1 / gamma), 0)


def lower_bound_c(r_on, beta1):
    r_off = -(beta0 / beta1 - 1) * r_on \
            + gamma / beta1 * (
                    1 + 1 / (beta0 - beta1) * (beta0 * np.log(beta1 / gamma) - beta1 * np.log(beta0 / gamma)))
    return max(r_off - r_on, 0)


def lower_bound_b(r_on, beta1):
    return beta0 / (beta0 - beta1) * (np.exp(-beta0 / gamma * r_on) + r_on) - gamma / (beta0 - beta1) * (
                1 + np.log(beta0 / gamma))


def level_b(i_max, beta1):
    def f(r_on_value):
        return 1 - i_max - np.exp(-beta0 / gamma * r_on_value) - r_on_value

    solution = root_scalar(f, x0=0.05, x1=0.15)
    r_on = solution.root
    if boundary_c_b(beta1) < r_on < boundary_b_a:
        plt.vlines(r_on, lower_bound_b(r_on, beta1), 0.5, colors='k')


def level_c(i_max, beta1):
    if beta1 < gamma:
        return None
    term = i_max - 1 + gamma / beta1 * (1 + np.log(beta1 / gamma))
    r_on = term * beta1 / (beta0 - beta1)
    if 0 < r_on < boundary_c_b(beta1):
        plt.vlines(r_on, lower_bound_c(r_on, beta1), 0.5, colors='k')


def level_d(i_max, beta1):
    term = i_max - 1 + gamma / beta0 * (1 + np.log(beta0 / gamma))
    r_off_minus_r_on = - term * beta0 / (beta0 - beta1)
    if 0 < r_off_minus_r_on < 1:
        # upper_bound = boundary_d_b(r_off_minus_r_on=r_off_minus_r_on, beta1=beta1)
        plt.hlines(r_off_minus_r_on, 0, 0.5, colors='k')


def phase_b(beta1):
    lower_bound = boundary_c_b(beta1)
    upper_bound = boundary_b_a

    xs_middle = np.linspace(lower_bound, upper_bound, 30)
    ys_middle = np.array([lower_bound_b(x, beta1) for x in xs_middle])
    xs = np.concatenate([[lower_bound], xs_middle, [upper_bound]])
    ys = np.concatenate([[0.5], ys_middle, [0.5]])
    plt.plot(xs, ys, color='b')


def phase_c(beta1):
    lower_bound = 0
    upper_bound = boundary_c_b(beta1)

    xs_middle = np.linspace(lower_bound, upper_bound, 30)
    ys_middle = np.array([lower_bound_c(x, beta1) for x in xs_middle])
    xs = np.concatenate([[lower_bound], xs_middle, [upper_bound]])
    ys = np.concatenate([[0.55], ys_middle, [0.5]])
    plt.plot(xs, ys, color='c')


def phase_d(beta1):
    lower_bound = 0
    boundary = boundary_c_b(beta1)
    upper_bound = boundary_b_a

    xs_middle_c = np.linspace(lower_bound, boundary, 30)
    ys_middle_c = np.array([lower_bound_c(x, beta1) for x in xs_middle_c])
    xs_middle_b = np.linspace(boundary, upper_bound, 30)
    ys_middle_b = np.array([lower_bound_b(x, beta1) for x in xs_middle_b])
    xs = np.concatenate([[lower_bound], xs_middle_c, xs_middle_b, [upper_bound]])
    ys = np.concatenate([[0], ys_middle_c, ys_middle_b, [0]])
    plt.plot(xs, ys, color='g')


def phase_a():
    lower_bound = boundary_b_a
    xs = [lower_bound, lower_bound, .8]
    ys = [0.5, 0, 0]
    plt.plot(xs, ys, color='m')


def debug():
    plot_theory(beta1s[1])
    plt.show()


if __name__ == "__main__":
    debug()
