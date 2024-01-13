from ..utility import find_imports

from math import sqrt


def test_find_imports():
    """Test load_imports."""
    imports = find_imports(find_imports)
    assert imports == ['import inspect']


def fn_using_sqrt(x):
    return sqrt(x)


def test_from_import():
    """Test load_imports."""
    imports = find_imports(fn_using_sqrt)
    assert imports == ['from math import sqrt']
