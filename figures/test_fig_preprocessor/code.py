
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


matplotlib.use('pdf')

# Helper fns

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """Preprocess data."""
    data['y'] = data['y'] * 100
    return data


# Create figure function

def create_test_figure_with_helper_fns(data: pd.DataFrame) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    data = preprocess_data(data)
    ax.plot(data['x'], data['y'])
    return fig


def reproduce_figure():
    data = pd.read_csv('figures/test_fig_preprocessor/data.csv')
    fig = create_test_figure_with_helper_fns(data)
    fig.savefig(
        f'figures/test_fig_preprocessor/test_fig_preprocessor.pdf',
        bbox_inches='tight'
    )


if __name__ == '__main__':
    reproduce_figure()
