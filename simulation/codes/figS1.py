import matplotlib.pyplot as plt

from default_params import beta1s, panel_width, figs_dir

from i_max_rForXy_phase_diagram import plot_peak_for_r
from r_steady_rForXy_phase_diagram import plot_r_steady_for_r


def plot(beta1, fig_name="figS1"):
    plt.figure(figsize=(panel_width * 1, panel_width * 2))
    plot_peak_for_r(beta1, save_fig=False, theory=True, data_name=fig_name)
    plot_r_steady_for_r(beta1, save_fig=False, theory=True, data_name=fig_name)
    plt.savefig(f"{figs_dir}{fig_name}.pdf")
    plt.savefig(f"{figs_dir}{fig_name}.eps")
    plt.savefig(f"{figs_dir}{fig_name}.tiff")
    plt.show()


if __name__ == "__main__":
    plot(beta1=beta1s[1])
