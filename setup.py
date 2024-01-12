import setuptools
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='reproducible_figures',
    version='{{VERSION_PLACEHOLDER}}',
    author="Dylan R. Cope",
    description='Small utility for creating reproducible figures.',
    url='https://github.com/DylanCope/reproducible_figures',
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=setuptools.find_packages(where='.'),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
    ]
)