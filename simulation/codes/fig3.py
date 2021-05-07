import matplotlib.pyplot as plt
import numpy as np
import math
from tqdm import tqdm
import pandas as pd

from model import simulate
from default_params import y0, mu, beta0, data_dir, figs_dir

duration = 200
R0s = np.arange(.5, 2.1, 0.1)

ts = np.arange(0, 2000, 0.01)
t_ons = np.linspace(0, 300, 1000)


def plot_simulation():
    minimum_peak = np.ones_like(R0s)
    for i, R0 in enumerate(tqdm(R0s)):
        beta1 = R0 * mu
        for t_on in t_ons:
            ss, i_s, rs = simulate(ts, y0, mu, beta0, beta1, start=t_on,
                                   end=t_on + duration)
            
            if minimum_peak[i] > i_s.max():
                minimum_peak[i] = i_s.max()
    print(minimum_peak)
    plt.scatter(R0s, minimum_peak)

    df = pd.DataFrame()
    df["R0"] = R0s
    df["minimum_of_peak"] = minimum_peak
    df.to_csv(f"{data_dir}fig3_simulation.csv")


def plot_theory():
    theory = np.loadtxt(f"{data_dir}fig3.csv", delimiter=",").T
    plt.plot(theory[0], theory[1])
    
    
def main():
    plot_theory()
    plot_simulation()
    plt.ylim([0, 0.16])
    plt.xlabel(r"$R_{0,\rm{on}}$",size="xx-large")
    plt.ylabel(r"$\bar{i}_{\rm{max}}$",size="xx-large")
    plt.xticks([0.5, 1, 1.5, 2],["0.5", "1", "1.5", "2"])
    plt.yticks([0, 0.04, 0.08, 0.12, 0.16],["0", "0.04", "0.08", "0.12", "0.16"])
    plt.savefig(f"{figs_dir}fig3_v0.eps")
    plt.savefig(f"{figs_dir}fig3_v0.tiff")
    plt.show()
    

if __name__ == "__main__":
    main()
