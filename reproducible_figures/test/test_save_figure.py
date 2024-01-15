from cycler import V
from reproducible_figures.plotting import set_plotting_style
from ..utility import save_reproducible_figure

from pathlib import Path
import subprocess

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from math import sqrt


matplotlib.use('pdf')


GLOBAL_COL_TO_USE = 'z'


def generate_random_data(n_points: int = 1000) -> pd.DataFrame:
    """Generate random data."""
    return pd.DataFrame({
        'x': range(n_points),
        'y': np.random.normal(size=n_points)
    })


def create_test_figure(data: pd.DataFrame) -> plt.Figure:
    """Create a figure."""
    fig, ax = plt.subplots()
    y = np.sin(data['x'] * 2 * np.pi / 1000) + 0.2 * data['y']
    ax.plot(data['x'], y)
    return fig


def run_checks_after_saving(fig_name: str, check_code_runs: bool = True):

    figure_dir = f'figures/{fig_name}'

    assert Path(f'{figure_dir}/{fig_name}.pdf').exists()
    assert Path(f'{figure_dir}/data.csv').exists()
    assert Path(f'{figure_dir}/code.py').exists()

    if check_code_runs:
        with open(f'{figure_dir}/{fig_name}.pdf') as f:
            figure_file_before = f.buffer.read()

        res = subprocess.run(['python', f'{figure_dir}/code.py'])
        assert res.returncode == 0, \
            f"Running code.py should not return an error code: {res.stderr}"

        with open(f'{figure_dir}/{fig_name}.pdf') as f:
            figure_file_after = f.buffer.read()

        assert figure_file_before != figure_file_after, \
            "Figure file should have been modified after running code.py"


def test_simple_save_figure():
    data = generate_random_data()
    fig_name = 'test_fig'
    save_reproducible_figure(fig_name, data, create_test_figure)
    run_checks_after_saving(fig_name)


def create_figure_with_plotting_style(data: pd.DataFrame):
    set_plotting_style()
    create_test_figure(data)


def test_save_figure_with_plotting_style():
    data = generate_random_data()
    fig_name = 'test_fig_with_plotting_style'
    save_reproducible_figure(fig_name, data,
                             create_figure_with_plotting_style)
    # TODO: figure out how to run code that imports from the module during test
    run_checks_after_saving(fig_name, check_code_runs=False)


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
                             create_test_figure_with_helper_fns)
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
    data = create_nx_data()
    fig_name = 'test_nx_fig'
    save_reproducible_figure(fig_name, data, create_nx_figure)
    run_checks_after_saving(fig_name)


def create_figure_with_global_vars(data: pd.DataFrame):
    fig, ax = plt.subplots()
    global GLOBAL_COL_TO_USE
    ax.plot(data['x'], data[GLOBAL_COL_TO_USE])
    return fig


def create_data_for_global_vars_test():
    """Generate random data."""
    return pd.DataFrame({
        'x': range(10),
        'y': np.random.normal(size=10),
        GLOBAL_COL_TO_USE: np.random.normal(size=10),
    })


def test_save_figure_with_global_vars():
    data = create_data_for_global_vars_test()
    fig_name = 'test_fig_global_vars'
    save_reproducible_figure(fig_name, data, create_figure_with_global_vars)
    run_checks_after_saving(fig_name)


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


def test_save_figure_with_helper_class():
    data = generate_random_data()
    fig_name = 'test_fig_helper_class'
    save_reproducible_figure(fig_name, data, create_figure_with_helper_class)
    run_checks_after_saving(fig_name)


def external_fn_with_internal_fn():
    def internal_fn(x):
        return np.sqrt(x)
    return internal_fn


def create_figure_with_external_fn_with_internal_fn(data: pd.DataFrame):
    fig, ax = plt.subplots()
    preprocessor = external_fn_with_internal_fn()
    data['x'] = preprocessor(data['x'])
    ax.plot(data['x'], data['y'])
    return fig


def test_save_figure_with_external_fn_with_internal_fn():
    data = generate_random_data()
    fig_name = 'test_fig_external_fn_with_internal_fn'
    # this is a case where the import finder will fail
    # because the function is defined in a function
    # so we need to specify the dependencies of the internal fn manually
    save_reproducible_figure(fig_name, data,
                             create_figure_with_external_fn_with_internal_fn,
                             additional_imports=['import numpy as np'])
    run_checks_after_saving(fig_name)


def random_additional_fn():
    print('Unused but here anyways!')


def test_save_figure_with_additional_fn():
    data = generate_random_data()
    fig_name = 'test_fig_additional_fn'
    save_reproducible_figure(fig_name, data, create_test_figure,
                             additional_fns=[random_additional_fn])
    run_checks_after_saving(fig_name)


def create_figure_test_import_from(data: pd.DataFrame):
    _, ax = plt.subplots()
    k = sqrt(4)
    ax.plot(data['x'], k * data['y'])


def test_save_figure_with_imported_from_module():
    data = generate_random_data()
    fig_name = 'test_fig_import_from'
    save_reproducible_figure(fig_name, data,
                             create_figure_test_import_from)
    run_checks_after_saving(fig_name)
