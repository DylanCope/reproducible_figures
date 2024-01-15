from typing import Optional
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


def set_plotting_style(font_scale: float = 1.5,
                       use_times_font: bool = True,
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
    if use_tex and use_times_font:
        default_rc['text.latex.preamble'] = r'\usepackage{times}'
    rc = {**default_rc, **(rc or {})}
    sns.set(font_scale=font_scale, rc=rc)
