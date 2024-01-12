from ..utility import save_reproducible_figure

from pathlib import Path
import subprocess

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

matplotlib.use('pdf')


def generate_random_data() -> pd.DataFrame:
    """Generate random data."""
    return pd.DataFrame({
        'x': range(10),
        'y': np.random.normal(size=10)
    })


def create_test_figure(data: pd.DataFrame) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    ax.plot(data['x'], data['y'])
    return fig


def run_checks_after_saving(fig_name: str):

    figure_dir = f'figures/{fig_name}'

    assert Path(f'{figure_dir}/{fig_name}.pdf').exists()
    assert Path(f'{figure_dir}/data.csv').exists()
    assert Path(f'{figure_dir}/code.py').exists()

    with open(f'{figure_dir}/{fig_name}.pdf') as f:
        figure_file_before = f.buffer.read()

    res = subprocess.run(['python', f'{figure_dir}/code.py'])
    assert res.returncode == 0

    with open(f'{figure_dir}/{fig_name}.pdf') as f:
        figure_file_after = f.buffer.read()

    assert figure_file_before != figure_file_after, \
        "Figure file should have been modified after running code.py"


def test_simple_save_figure():
    data = generate_random_data()
    fig_name = 'test_fig'
    save_reproducible_figure(fig_name, data, create_test_figure)
    run_checks_after_saving(fig_name)


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """Preprocess data."""
    data['y'] = data['y'] * 100
    return data


def create_test_figure_with_helper_fns(data: pd.DataFrame) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    data = preprocess_data(data)
    ax.plot(data['x'], data['y'])
    return fig


def test_save_figure_with_helper_fns():
    data = generate_random_data()
    fig_name = 'test_fig_preprocessor'
    save_reproducible_figure(fig_name, data,
                             create_test_figure_with_helper_fns,
                             helper_fns=[preprocess_data])
    run_checks_after_saving(fig_name)


def create_nx_data() -> pd.DataFrame:
    import networkx as nx
    graph = nx.random_graphs.erdos_renyi_graph(10, 0.5)
    return nx.to_pandas_adjacency(graph)


def create_nx_figure(data: pd.DataFrame):
    data.columns = data.index
    graph = nx.from_pandas_adjacency(data)
    nx.draw(graph)


def test_save_figure_with_additional_imports():
    additional_imports = ['import networkx as nx']
    data = create_nx_data()
    fig_name = 'test_nx_fig'
    save_reproducible_figure(fig_name, data, create_nx_figure,
                             additional_imports=additional_imports)
    run_checks_after_saving(fig_name)
