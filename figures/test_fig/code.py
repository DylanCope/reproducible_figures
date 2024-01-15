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


def reproduce_figure():
    data = pd.read_csv("figures/test_fig/data.csv")
    fig = create_test_figure(data)
    fig.savefig("figures/test_fig/test_fig.pdf", bbox_inches="tight", dpi=1000)


if __name__ == "__main__":
    reproduce_figure()
