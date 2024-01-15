from reproducible_figures.plotting import set_plotting_style
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


matplotlib.use("pdf")


def create_test_figure(data: pd.DataFrame) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    y = np.sin(data["x"] * 2 * np.pi / 1000) + 0.2 * data["y"]
    ax.plot(data["x"], y)
    return fig


def create_figure_with_plotting_style(data: pd.DataFrame):
    set_plotting_style()
    create_test_figure(data)


def reproduce_figure():
    data = pd.read_csv("figures/test_fig_with_plotting_style/data.csv")
    create_figure_with_plotting_style(data)
    plt.savefig(
        "figures/test_fig_with_plotting_style/test_fig_with_plotting_style.pdf",
        bbox_inches="tight",
        dpi=1000,
    )


if __name__ == "__main__":
    reproduce_figure()
