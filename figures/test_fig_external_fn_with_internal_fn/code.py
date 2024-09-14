from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


matplotlib.use("pdf")


def external_fn_with_internal_fn():
    def internal_fn(x):
        return np.sqrt(x)

    return internal_fn


def create_figure_with_external_fn_with_internal_fn(data: pd.DataFrame):
    fig, ax = plt.subplots()
    preprocessor = external_fn_with_internal_fn()
    data["x"] = preprocessor(data["x"])
    ax.plot(data["x"], data["y"])
    return fig


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
        for csv_path in sorted(
            Path("figures/test_fig_external_fn_with_internal_fn").glob("data_*.csv")
        )
    ]
    fig = create_figure_with_external_fn_with_internal_fn(*data)
    fig.savefig(
        "figures/test_fig_external_fn_with_internal_fn/test_fig_external_fn_with_internal_fn.pdf",
        bbox_inches="tight",
        dpi=1000,
    )


if __name__ == "__main__":
    reproduce_figure()
