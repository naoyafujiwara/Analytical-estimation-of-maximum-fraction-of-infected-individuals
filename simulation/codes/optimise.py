import numpy as np
from scipy.optimize import minimize_scalar

from default_params import cases_duration, ts_for_optimisation, y0, mu, beta1s, beta0
from model import simulate

beta1 = beta1s[1]


def peak(start):
    print(start)
    end = start + cases_duration
    ss, i_s, rs = simulate(ts_for_optimisation, y0, mu, beta0, beta1, start=start, end=end)
    return i_s.max()


def r_steady(start):
    print(start)
    end = start + cases_duration
    ss, i_s, rs = simulate(ts_for_optimisation, y0, mu, beta0, beta1, start=start, end=end)
    return rs.max()


def main():
    t_on_peak = minimize_scalar(peak, bounds=(0, 300))
    print(f"optimal t_on for peak is {t_on_peak.x}")
    t_on_r_steady = minimize_scalar(r_steady, bounds=(0, 300))
    print(f"optimal t_on for r_steady is {t_on_r_steady.x}")


main()
