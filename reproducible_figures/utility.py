from typing import Callable, List, Optional

from pathlib import Path
import inspect

import matplotlib.pyplot as plt
import pandas as pd


def save_reproducible_figure(fig_name: str,
                             fig_data: pd.DataFrame,
                             create_figure: Callable[[pd.DataFrame], plt.Figure],
                             helper_fns: Optional[List[Callable]] = None,
                             additional_imports: Optional[List[str]] = None,
                             save_index: bool = False,
                             figures_dir: str = 'figures'):
    """
    Creates and saves a figure, including the data and the code
    used to create the figure. The create figure function must
    include all the code needed to create the figure, and only
    call the plotting functions from matplotlib (plt), seaborn (sns),
    pandas (pd), and numpy (np). If more imports are needed, they
    can be added to additional_imports. The code can also be modified
    manually after it is created.

    Args:
        fig_name: Name of the figure. This will be used to create
            a directory in figures_dir, and the figure will be saved
            in this directory.
        fig_data: Data used to create the figure. This will be saved
            as a csv file in the figure directory.
        create_figure: Function that creates the figure. This function
            must take fig_data as input and return a matplotlib Figure
            object.
        helper_fns: Optional list of helper functions used to create
            the figure. These functions will be embedded into the
             code for reproducing the figure.
        additional_imports: Optional list of additional imports needed
            to create the figure. These will be embedded into the code.
        save_index: Whether to save the index of fig_data. Default is True.
        figures_dir: Directory where the figure will be saved.
            Default is 'figures'.

    Usage:
    
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
    """
    output_dir = f'{figures_dir}/{fig_name}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    fig_data.to_csv(f'{output_dir}/data.csv', index=save_index)
    fig = create_figure(fig_data)
    if fig is not None:
        fig.savefig(f'{output_dir}/{fig_name}.pdf',
                    bbox_inches='tight')
    else:
        plt.savefig(f'{output_dir}/{fig_name}.pdf',
                    bbox_inches='tight')

    plt.close()
    try:
        # Save the code used to generate the figure

        if fig is None:
            save_fig_code_prefix = "plt"
        else:
            save_fig_code_prefix = "fig"

        if helper_fns is not None:
            helper_fns_code = '# Helper fns\n\n' + '\n'.join([
                inspect.getsource(fn) for fn in helper_fns
            ])
        else:
            helper_fns_code = ''

        if additional_imports is not None:
            additional_imports_code = '\n'.join(additional_imports)
        else:
            additional_imports_code = ''

        script = f"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
{additional_imports_code}

matplotlib.use('pdf')

{helper_fns_code}

# Create figure function

{inspect.getsource(create_figure)}

def reproduce_figure():
    data = pd.read_csv('{output_dir}/data.csv')
    fig = {create_figure.__name__}(data)
    {save_fig_code_prefix}.savefig(
        f'{output_dir}/{fig_name}.pdf',
        bbox_inches='tight'
    )


if __name__ == '__main__':
    reproduce_figure()
"""

        with open(f'{output_dir}/code.py', 'w') as f:
            f.write(script)

    except Exception as e:
        print(f'Failed to save code: {e}')
