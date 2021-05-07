import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

from model import simulate

# rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
# rc('text', usetex=True)


y0 = [1-1/1000, 1/1000]
ts = np.linspace(0, 300, 301 * 10)

mu = 1
beta0 = 2 * mu
beta1 = 0.8 * mu

duration = 1

t_ons = np.linspace(0, 10, 101)

r_ons = []
r_offs = []
i_maxs = []


def main():
    for start in t_ons:
        end = start + duration
        ss, i_s, rs = simulate(ts, y0, mu, beta0, beta1, start=start, end=end)
        r_ons.append(rs[ts.searchsorted(start)])
        r_offs.append(rs[ts.searchsorted(end)])
        i_maxs.append(max(i_s))
    
    plt.scatter(r_ons, r_offs, c=i_maxs)
    plt.title(f"beta0={beta0}, beta1={beta1}, mu={mu}, Delta T={duration}")
    plt.axis('square')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.colorbar(label="$\max_t\;i(t)$")
    plt.savefig("max_i.pdf")
    plt.show()


if __name__ == '__main__':
    main()
