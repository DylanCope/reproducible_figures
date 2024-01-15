from types import ModuleType
from typing import Callable, List, Optional

from pathlib import Path
import inspect
import subprocess

import matplotlib.pyplot as plt
import pandas as pd


def save_reproducible_figure(fig_name: str,
                             fig_data: pd.DataFrame,
                             create_figure: Callable[[pd.DataFrame], plt.Figure],
                             save_index: bool = False,
                             show: bool = False,
                             matplotlib_backend: str = 'pdf',
                             figure_file_fmt: Optional[str] = None,
                             figures_dir: str = 'figures',
                             auto_format: bool = True,
                             figure_dpi: int = 1000,
                             additional_imports: Optional[List[str]] = None,
                             additional_fns: Optional[Callable] = None):
    """
    Creates and saves a figure, including the data and the code
    used to create the figure. This allows the figure to be
    easy reproduced later. The figure is saved in a directory
    named after fig_name in figures_dir.

    The code is built automatically by finding all the imports
    needed for create_figure and the functions or classes
    used in create_figure. This process is not flawless and can
    potentially miss some imports if they are not accessible
    through inspection. Additionally, if the code reads from
    external data sources, these may not be avaiable when
    reproducing the figure. However, it should work well
    for most cases!

    Args:
        fig_name: Name of the figure. This will be used to create
            a directory in figures_dir, and the figure will be saved
            in this directory.
        fig_data: Data used to create the figure. This will be saved
            as a csv file in the figure directory.
        create_figure: Function that creates the figure. This function
            must take fig_data as input and return a matplotlib Figure
            object.
        save_index: Whether to save the index of fig_data. Default is True.
        show: Whether to show the figure. Default is False and the
            figure is closed after saving.
        matplotlib_backend: Backend to use for matplotlib. Default is 'pdf'.
        figure_file_fmt: Format to use for saving the figure. Default is
            None, which will use the matplotlib backend.
        figures_dir: Directory where the figure will be saved.
            Default is 'figures'.
        figure_dpi: DPI to use for saving the figure. Default is 1000,
            which will create a high resolution figure ready for publication.
        auto_format: Whether to autoformat the code. Default is True.
            Relies on black being installed.
        additional_imports: Additional imports needed to create the figure.
            In most cases, this should not be needed as the automatic
            imports finder should find all the imports needed. However,
            if there are any issues, additional imports can be added here.
        additional_fns: Additional functions needed to create the figure.
            In most cases, this should not be needed as the automatic
            source builder should find all the functions needed. However,
            if there are any issues or you just want to preserve some code
            (e.g. code used to generate the data), the functions provided
            can be added here to be put into the source file.

    Example Usage:

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

        This will create a directory called figures/test_save_figure with
        the following files:
            - data.csv: csv file containing the data used to create the figure
            - code.py: python script that can be used to reproduce the figure
            - test_save_figure.pdf: figure file
    """
    output_dir = f'{figures_dir}/{fig_name}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    fig_data.to_csv(f'{output_dir}/data.csv', index=save_index)
    fig = create_figure(fig_data)

    figure_file_fmt = figure_file_fmt or matplotlib_backend
    if fig is not None:
        fig.savefig(f'{output_dir}/{fig_name}.{figure_file_fmt}',
                    bbox_inches='tight', dpi=figure_dpi)
    else:
        plt.savefig(f'{output_dir}/{fig_name}.{figure_file_fmt}',
                    bbox_inches='tight', dpi=figure_dpi)

    if show:
        plt.show()
    else:
        plt.close()

    # Save the code used to generate the figure
    default_imports = ['import matplotlib', 'import pandas as pd']
    if additional_imports:
        default_imports += additional_imports

    if fig is None:
        save_fig_code_prefix = "plt"
        default_imports.append('import matplotlib.pyplot as plt')
        create_fig_code = f"{create_figure.__name__}(data)"
    else:
        save_fig_code_prefix = "fig"
        create_fig_code = f"fig = {create_figure.__name__}(data)"

    imports = find_imports(create_figure)

    if additional_fns:
        additional_source = '\n\n'
        for fn in additional_fns:
            imports += find_imports(fn)
            additional_source += build_function_source(fn) + '\n\n'
    else:
        additional_source = ''

    imports = sorted(set(imports + default_imports))
    imports_code = '\n'.join(imports)

    script = f"""
{imports_code}


matplotlib.use({matplotlib_backend!r})
{additional_source}

{build_function_source(create_figure)}

def reproduce_figure():
    data = pd.read_csv('{output_dir}/data.csv')
    {create_fig_code}
    {save_fig_code_prefix}.savefig(
        '{output_dir}/{fig_name}.{figure_file_fmt}',
        bbox_inches='tight', dpi={figure_dpi}
    )


if __name__ == '__main__':
    reproduce_figure()
"""

    try:
        with open(f'{output_dir}/code.py', 'w') as f:
            f.write(script)

    except Exception as e:
        print(f'Failed to save code: {e}')

    if auto_format:
        run_autoformat(f'{output_dir}/code.py')


def run_autoformat(code_file: str):
    """Runs autoformatting on the code file."""
    try:
        # autoformat the code with black
        res = subprocess.run(['black', code_file])
        if res.returncode != 0:
            print('Failed to autoformat code with black:', res.stderr)

    except Exception as e:
        print(f'Failed to autoformat code with black: {e}')


PRIMITIVES = (bool, str, int, float, type(None))


def is_primitive(obj):
    global PRIMITIVES
    return isinstance(obj, PRIMITIVES)


def find_imports(obj,
                 main_module: Optional[ModuleType] = None,
                 searched_already: List[Callable] = None) -> List[str]:
    """
    Recursively finds the imports needed for a function.

    Args:
        obj: Function to find the imports for.
        main_module: Main module of the function. Used to determine
            whether a function is defined in the main module, or
            can be imported from another module.
        searched_already: List of functions that have already been searched.
            This is used to avoid searching the same function multiple times.
    """
    searched_already = searched_already or []
    if main_module is None:
        main_module = inspect.getmodule(obj)

    searched_already.append(obj)
    imports = []

    for member_name, member in inspect.getmembers(obj):
        if member_name.startswith('__'):
            continue
        if inspect.isfunction(member) and member not in searched_already:
            imports += find_imports(member, main_module, searched_already)

    if inspect.getmodule(obj) not in [main_module, None]:
        module = inspect.getmodule(obj)
        if hasattr(module, '__name__') and hasattr(obj, '__name__'):
            imports.append(f'from {module.__name__} import {obj.__name__}')

    elif inspect.isfunction(obj):
        closure_vars = inspect.getclosurevars(obj)
        for var_name, var_value in closure_vars.globals.items():
            if var_value is None:
                continue

            if inspect.ismodule(var_value):
                module_name = var_value.__name__
                if var_name != module_name:
                    imports.append(f'import {module_name} as {var_name}')
                else:
                    imports.append(f'import {module_name}')

            elif var_value not in searched_already:
                imports += find_imports(var_value, main_module, searched_already)

    return sorted(set(imports))


def build_globals_source(closure_vars: inspect.ClosureVars,
                         main_module: ModuleType,
                         built_already: list) -> str:
    """
    Builds the source code for the global variables used in a function.

    Args:
        closure_vars: Closure variables of the function.
        main_module: Main module of the function. Used to determine
            whether a function is defined in the main module, or
            can be imported from another module.
        built_already: List of functions that have already been built.
            This is used to avoid building the same function multiple times.
    """
    source = ""

    for var_name, var_value in closure_vars.globals.items():

        if is_primitive(var_value):
            source += f'{var_name} = {repr(var_value)}\n\n'

        if inspect.getmodule(var_value) == main_module:
            if inspect.isfunction(var_value) and var_value not in built_already:
                source += build_function_source(var_value, main_module, built_already) + '\n\n'

            elif inspect.isclass(var_value):
                return build_class_source(var_value, main_module, built_already) + '\n\n'

    return source


def build_function_source(fn: Callable,
                          main_module: Optional[ModuleType] = None,
                          built_already: list = None) -> str:
    """
    Recursively builds the source code for a function.

    Args:
        fn: Function to build the source code for.
        main_module: Main module of the function. Used to determine
            whether a function is defined in the main module, or
            can be imported from another module.
        built_already: List of functions that have already been built.
            This is used to avoid building the same function multiple times.
    """
    built_already = built_already or []
    built_already.append(fn)
    main_module = main_module or inspect.getmodule(fn)
    closure_vars = inspect.getclosurevars(fn)

    source = build_globals_source(closure_vars, main_module, built_already)

    if source != "":
        source += '\n'

    source += inspect.getsource(fn)

    return source


def build_class_source(cls: type,
                       main_module: Optional[ModuleType] = None,
                       built_already: Optional[list] = None) -> str:
    """
    Builds the source code for a class.

    Args:
        cls: Class to build the source code for.
        main_module: Main module of the function. Used to determine
            whether an object is defined in the main module, or
            can be imported from another module.
        built_already: List of functions that have already been built.
            This is used to avoid building the same function multiple times.
    """
    built_already = built_already or []
    built_already.append(cls)

    main_module = main_module or inspect.getmodule(cls)

    source = ""
    for var_name, var_value in inspect.getmembers(cls):
        if var_name.startswith('__'):
            continue

        if inspect.isfunction(var_value):
            closure_vars = inspect.getclosurevars(var_value)
            source += build_globals_source(closure_vars, main_module, built_already) + '\n\n'

    source += inspect.getsource(cls)

    return source
