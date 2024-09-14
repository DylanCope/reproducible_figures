
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


matplotlib.use('pdf')


def create_nx_figure(data: pd.DataFrame):
    data.columns = data.index
    graph = nx.from_pandas_adjacency(data)
    nx.draw(graph)


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
<<<<<<< HEAD
        for csv_path in sorted(Path("figures/test_nx_fig").glob("data_*.csv"))
=======
        for csv_path in Path('figures/test_nx_fig').glob('data_*.csv')
>>>>>>> 901d94dc1d836ade4eedc04319f91bf776971c22
    ]
    create_nx_figure(*data)
    plt.savefig(
        'figures/test_nx_fig/test_nx_fig.pdf',
        bbox_inches='tight', dpi=1000
    )


if __name__ == '__main__':
    reproduce_figure()
