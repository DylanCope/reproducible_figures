from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


matplotlib.use("pdf")


def create_test_figure_with_kwargs(data: pd.DataFrame, value: float) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    ax.plot(data.x, data.y)
    ax.hlines(value, data.x.min(), data.x.max())
    return fig


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
        for csv_path in sorted(Path("figures/test_fig_with_kwargs").glob("data_*.csv"))
    ]
    fig = create_test_figure_with_kwargs(*data, value=-0.0014064872432473408)
    fig.savefig(
        "figures/test_fig_with_kwargs/test_fig_with_kwargs.pdf",
        bbox_inches="tight",
        dpi=1000,
    )


if __name__ == "__main__":
    reproduce_figure()
