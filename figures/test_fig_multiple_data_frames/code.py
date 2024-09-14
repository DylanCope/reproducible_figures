from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


matplotlib.use("pdf")


def create_test_figure_multiple_frames(
    data1: pd.DataFrame, data2: pd.DataFrame
) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    ax.plot(data1.x, data1.y)
    ax.plot(data2.x, data2.y)
    return fig


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
        for csv_path in sorted(
            Path("figures/test_fig_multiple_data_frames").glob("data_*.csv")
        )
    ]
    fig = create_test_figure_multiple_frames(*data)
    fig.savefig(
        "figures/test_fig_multiple_data_frames/test_fig_multiple_data_frames.pdf",
        bbox_inches="tight",
        dpi=1000,
    )


if __name__ == "__main__":
    reproduce_figure()
