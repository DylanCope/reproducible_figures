# Reproducible Figures


A small Python utility to generate easily reproducible figures for scientific papers.
I often find myself generating figures for papers and then having to go through
needlessly tedious processes to regenerate them when I want to make a small change,
so I made this package.
By generating figures using this package a folder is created with the figure,
the data used to generate the figure, and the code used to generate the figure.
I recommend combining this with a version control system like git to track changes
for your figures.

## Installation

```bash
pip install reproducible_figures
```

## Example Usage

```python
from reproducible_figures import save_reproducible_figure
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_figure(data):
    fig, ax = plt.subplots()
    ax.plot(data['x'], data['y'])
    return fig

data = pd.DataFrame({
    'x': range(10),
    'y': np.random.normal(size=10)
})

save_reproducible_figure('test_save_figure', data, create_figure)
```
This will create the folder `figures/test_save_figure` with the following structure:

```
figures/test_save_figure
├── data.csv
├── test_save_figure.pdf
└── code.py
```

The `data.csv` file contains the data used to generate the figure, the `figure.pdf` file contains the figure itself, and the `code.py` file contains the code used to generate the figure.

In order to reproduce the figure, you can run:
```bash
python figures/test_save_figure/code.py
```

If you want to modify the figure, you can edit the `code.py` file and run it again.

## Advanced Usage

**Additional Imports**

By default, the only libraries available in the `code.py` file are `pandas as pd` and `matplotlib.pyplot as plt`, `matplotlib`, `numpy as np`, and `seaborn as sns`. If you want to use other libraries, you can pass them to the `save_reproducible_figure` function:

```python
save_reproducible_figure('test_save_figure',
                         data,
                         create_figure,
                         additional_imports=['import networkx as nx'])
```

This will add `import networkx as nx` to the `code.py` file.
See the tests for an example using `networkx` to generate a figure.


**Helper Functions**

If you want to use helper functions in your `code.py` file, you can pass them to the `save_reproducible_figure` function. For example:

```python
def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """Preprocess data."""
    data['y'] = data['y'] * 100
    return data


def create_test_figure_with_helper_fns(data: pd.DataFrame):
    """Create a figure."""
    fig, ax = plt.subplots()
    data = preprocess_data(data)
    ax.plot(data['x'], data['y'])

save_reproducible_figure('test_fig_preprocessor', data,
                         create_test_figure_with_helper_fns,
                         helper_fns=[preprocess_data])
```
