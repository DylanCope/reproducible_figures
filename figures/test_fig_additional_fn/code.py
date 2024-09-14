from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


matplotlib.use("pdf")


def random_additional_fn():
    print("Unused but here anyways!")


def create_test_figure(data: pd.DataFrame) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    ax.plot(data.x, data.y)
    return fig


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
        for csv_path in sorted(
            Path("figures/test_fig_additional_fn").glob("data_*.csv")
        )
    ]
    fig = create_test_figure(*data)
    fig.savefig(
        "figures/test_fig_additional_fn/test_fig_additional_fn.pdf",
        bbox_inches="tight",
        dpi=1000,
    )


if __name__ == "__main__":
    reproduce_figure()
