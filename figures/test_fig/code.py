
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


matplotlib.use('pdf')


def create_test_figure(data: pd.DataFrame) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    ax.plot(data.x, data.y)
    return fig


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
<<<<<<< HEAD
        for csv_path in sorted(Path("figures/test_fig").glob("data_*.csv"))
=======
        for csv_path in Path('figures/test_fig').glob('data_*.csv')
>>>>>>> 901d94dc1d836ade4eedc04319f91bf776971c22
    ]
    fig = create_test_figure(*data)
    fig.savefig(
        'figures/test_fig/test_fig.pdf',
        bbox_inches='tight', dpi=1000
    )


if __name__ == '__main__':
    reproduce_figure()
