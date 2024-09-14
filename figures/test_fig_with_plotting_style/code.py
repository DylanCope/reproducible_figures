
from pathlib import Path
from reproducible_figures.plotting import set_plotting_style
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


matplotlib.use('pdf')


def create_test_figure(data: pd.DataFrame) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    ax.plot(data.x, data.y)
    return fig



def create_figure_with_plotting_style(data: pd.DataFrame):
    set_plotting_style()
    create_test_figure(data)


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
<<<<<<< HEAD
        for csv_path in sorted(
            Path("figures/test_fig_with_plotting_style").glob("data_*.csv")
        )
=======
        for csv_path in Path('figures/test_fig_with_plotting_style').glob('data_*.csv')
>>>>>>> 901d94dc1d836ade4eedc04319f91bf776971c22
    ]
    create_figure_with_plotting_style(*data)
    plt.savefig(
        'figures/test_fig_with_plotting_style/test_fig_with_plotting_style.pdf',
        bbox_inches='tight', dpi=1000
    )


if __name__ == '__main__':
    reproduce_figure()
