
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


matplotlib.use('pdf')



# Create figure function

def create_test_figure(data: pd.DataFrame) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    ax.plot(data['x'], data['y'])
    return fig


def reproduce_figure():
    data = pd.read_csv('figures/test_fig/data.csv')
    fig = create_test_figure(data)
    fig.savefig(
        f'figures/test_fig/test_fig.pdf',
        bbox_inches='tight'
    )


if __name__ == '__main__':
    reproduce_figure()
