import matplotlib.pyplot as plt

from default_params import beta1s, panel_width, figs_dir

from cases import plot_cases
from i_max_rForXy_phase_diagram import plot_peak_for_r
from i_max_phase_diagram import plot_peak_for_t
from r_steady_phase_diagram import plot_r_steady_for_t
from r_steady_rForXy_phase_diagram import plot_r_steady_for_r


def plot(beta1, fig_name="fig1"):
    plt.figure(figsize=(panel_width * 5, panel_width * 5))
    plot_cases(beta1, save_fig=False, data_name=fig_name)
    plot_peak_for_r(beta1, save_fig=False, data_name=fig_name)
    plot_peak_for_t(beta1, save_fig=False, data_name=fig_name)
    plot_r_steady_for_t(beta1, save_fig=False, data_name=fig_name)
    plot_r_steady_for_r(beta1, save_fig=False, data_name=fig_name)
    plt.savefig(f"{figs_dir}{fig_name}.pdf")
    plt.savefig(f"{figs_dir}{fig_name}.eps")
    plt.savefig(f"{figs_dir}{fig_name}.tiff")
    plt.show()


if __name__ == "__main__":
    plot(beta1=beta1s[1])
