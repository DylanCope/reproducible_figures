
from math import sqrt
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


matplotlib.use('pdf')




def external_fn(x):
    return np.sqrt(x)




class HelperClass:

    def __init__(self, a: int):
        self.a = a

    def internal_fn(self, x):
        return x * self.a

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess data."""
        data['y'] = self.internal_fn(data['y'])
        data['x'] = external_fn(data['x'])
        return data



def create_figure_with_helper_class(data: pd.DataFrame):
    fig, ax = plt.subplots()
    helper_class = HelperClass(a=10)
    data = helper_class.preprocess_data(data)
    ax.plot(data['x'], data['y'])
    return fig


def reproduce_figure():
    data = [
        pd.read_csv(csv_path)
<<<<<<< HEAD
        for csv_path in sorted(Path("figures/test_fig_helper_class").glob("data_*.csv"))
=======
        for csv_path in Path('figures/test_fig_helper_class').glob('data_*.csv')
>>>>>>> 901d94dc1d836ade4eedc04319f91bf776971c22
    ]
    fig = create_figure_with_helper_class(*data)
    fig.savefig(
        'figures/test_fig_helper_class/test_fig_helper_class.pdf',
        bbox_inches='tight', dpi=1000
    )


if __name__ == '__main__':
    reproduce_figure()
