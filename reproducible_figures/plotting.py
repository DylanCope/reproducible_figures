from typing import List, Optional
import subprocess
import seaborn as sns


def is_tex_available() -> bool:
    """
    Check if TeX/LaTeX is installed on the system.
    """
    try:
        # Attempt to run the 'tex --version' command to check for TeX/LaTeX installation
        subprocess.run(["tex", "--version"],
                       check=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # If the command fails or is not found, TeX is likely not installed
        return False


def get_latex_preamble_string(latex_packages: List[str]) -> str:
    return ' '.join([f'\\usepackage{{{package}}}' for package in latex_packages])


def set_plotting_style(font_scale: float = 1.5,
                       use_times_font: bool = True,
                       latex_packages: Optional[List[str]] = None,
                       rc: Optional[dict] = None):
    """
    Set the default plotting style for matplotlib and seaborn.
    """
    use_tex = is_tex_available()
    default_rc = {
        'font.family':'serif',
        "text.usetex": use_tex,
        'savefig.facecolor': 'white',
    }
    if use_tex:
        latex_packages = latex_packages or []
        if use_times_font:
            latex_packages.append('times')
        if latex_packages:
            default_rc['text.latex.preamble'] = \
                get_latex_preamble_string(latex_packages)

    rc = {**default_rc, **(rc or {})}

    sns.set(font_scale=font_scale, rc=rc)
