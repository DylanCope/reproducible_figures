
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


matplotlib.use('pdf')


GLOBAL_COL_TO_USE = 'z'


def create_figure_with_global_vars(data: pd.DataFrame):
    fig, ax = plt.subplots()
    global GLOBAL_COL_TO_USE
    ax.plot(data['x'], data[GLOBAL_COL_TO_USE])
    return fig


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
<<<<<<< HEAD
        for csv_path in sorted(Path("figures/test_fig_global_vars").glob("data_*.csv"))
=======
        for csv_path in Path('figures/test_fig_global_vars').glob('data_*.csv')
>>>>>>> 901d94dc1d836ade4eedc04319f91bf776971c22
    ]
    fig = create_figure_with_global_vars(*data)
    fig.savefig(
        'figures/test_fig_global_vars/test_fig_global_vars.pdf',
        bbox_inches='tight', dpi=1000
    )


if __name__ == '__main__':
    reproduce_figure()
