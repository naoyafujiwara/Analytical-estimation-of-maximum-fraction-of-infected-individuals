import numpy as np
from scipy.integrate import odeint


def f(y, t, beta, mu_in_f):
    s, i = y
    return [-beta*s*i, beta*s*i - mu_in_f*i]


def simulate(ts, y0, mu, beta0, beta1=None, start=None, end=None, ):
    if start is None or ts[-1] < start or start == end:
        sol = odeint(f, y0, ts, args=(beta0, mu))
        ss = sol[:, 0]
        i_s = sol[:, 1]
        rs = 1 - ss - i_s
        return ss, i_s, rs
    assert end is not None
    assert beta0 is not None
    index_start = ts.searchsorted(start)
    index_end = ts.searchsorted(end)
    sol_before = odeint(f, y0, ts[:index_start], args=(beta0, mu))
    y0_intervention = y0 if start == 0 else sol_before[-1, :]
    ts_intervention = ts[: index_end] if start == 0 else \
        ts[index_start-1:index_end]
    sol_intervention = odeint(f, y0_intervention, ts_intervention,
                              args=(beta1, mu))
    sol_after = odeint(f, sol_intervention[-1, :], ts[index_end-1:],
                       args=(beta0, mu))
    sol = np.concatenate([sol_before, sol_intervention[1:], sol_after[1:]],
                         axis=0)

    ss = sol[:, 0]
    i_s = sol[:, 1]
    rs = 1 - ss - i_s
    return ss, i_s, rs


def normalize(nd_array):
    return nd_array / np.max(nd_array)


def r_on_and_delta_r(starts, duration, ts, y0, mu, beta0, beta1):
    r_ons = []
    delta_rs = []
    for start in starts:
        if start is None:
            r_ons.append(0)
            delta_rs.append(0)
            continue
        end = start + duration
        ss, i_s, rs = simulate(ts, y0, mu, beta0, beta1, start, end)

        t_length = rs.size
        mask_on = (ts >= start)[:t_length]
        r_ons.append(rs[mask_on][0])
        mask_off = (ts >= start + duration)[:t_length]
        delta_rs.append(rs[mask_off][0] - r_ons[-1])

    return r_ons, delta_rs
