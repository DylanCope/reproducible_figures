from math import sqrt
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


matplotlib.use("pdf")


def create_figure_test_import_from(data: pd.DataFrame):
    _, ax = plt.subplots()
    k = sqrt(4)
    ax.plot(data["x"], k * data["y"])


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
        for csv_path in sorted(Path("figures/test_fig_import_from").glob("data_*.csv"))
    ]
    create_figure_test_import_from(*data)
    plt.savefig(
        "figures/test_fig_import_from/test_fig_import_from.pdf",
        bbox_inches="tight",
        dpi=1000,
    )


if __name__ == "__main__":
    reproduce_figure()
