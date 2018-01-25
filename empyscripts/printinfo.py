"""
Add-on for `empymod`: tools to print date, time, and version information
========================================================================

Print date, time, and package version information in any environment (Jupyter
notebook, IPython console, Python console, QT console), either as html-table
(notebook) or as plain text (anywhere).

This script was heavily inspired by:

    - ipynbtools.py from qutip https://github.com/qutip
    - watermark.py from https://github.com/rasbt/watermark

"""

# Mandatory modules
import sys
import time
import numpy
import scipy
import textwrap
import platform
import multiprocessing

# empymod
import empymod
import empyscripts

# Optional modules
try:
    import matplotlib
except ImportError:
    matplotlib = False
try:
    import numexpr
except ImportError:
    numexpr = False

# Check if IPython is installed
try:
    import IPython
    from IPython.display import HTML
except ImportError:
    IPython = False


def versions(add_pckg=[], mode='auto', ncol=3):
    """Return date, time, and version information.

    Prints a nice table if called from a Jupyter notebook. If called from
    Ipython or Python consoles, it will print the information as plain text.
    For QT consoles, use `mode='text'`, as it cannot be distinguished from a
    Jupyter notebook, but cannot render html.

    Parameters
    ----------
    add_pckg : packages, optional
        Package or list of packages to add to output information (must be
        imported beforehand).

    mode : string, optional; {<'auto'>, 'text', 'html'}
        Defaults to 'auto':
            - 'auto': Returns HTML(html) for Jupyter notebooks, and text for
                      IPython and Python consoles. Unfortunately, returns
                      HTML(html) for QT consoles.
            - 'text': Forces plain-text version. Good for QT consoles.
            - 'html': Returns html instead of HTML(html).
            - 'plain': Returns text instead of print(text).

    ncol : int, optional
        Number of package-columns in html table (therefore only affects the
        html version, not the plain-text version). Defaults to 3.


    Returns
    -------
    Depends on `mode`:


    Examples
    --------
    >>> import pytest
    >>> import dateutil
    >>> from empyscripts import versions

    Default values
    >>> versions()

    Provide additional package
    >>> versions(pytest)

    Provide additional packages
    >>> versions([pytest, dateutil])

    """

    # Check HTML with mode
    no_HTML = _check_html_mode(mode)

    # Get packages
    pckgs = _get_packages(add_pckg)

    # Print text or return html
    if mode == 'html':
        return _get_html(pckgs, ncol)
    elif mode == 'plain':
        return _get_text(pckgs)
    else:
        if no_HTML:
            print(_get_text(pckgs))
        else:
            return HTML(_get_html(pckgs, ncol))


def _get_html(pckgs, ncol):
    """HTML version."""

    # Define html-styles
    style1 = " style='border: 2px solid #fff; text-align: left;'"
    style2 = " style='background-color: #ccc; border: 2px solid #fff;'"

    # Create new html-row
    def newrow(i, ncol, html):
        """Create new raw after ncol entries."""
        if i % ncol == 0:
            html += "  </tr>\n"
            html += "  <tr" + style1 + ">\n"
        return i+1, html

    # Date and time info as title
    date_time_info = time.strftime('%a %b %d %H:%M:%S %Y %Z')
    html = "<h3>%s</h3>\n" % date_time_info

    # Start html-table
    html += '<table>\n'

    # OS and CPUs
    html += "  <tr" + style1 + ">\n"
    html += "    <td" + style2 + ">%s</td>\n" % platform.system()
    html += "    <td" + style1 + ">OS</td>\n"
    i, html = newrow(1, ncol, html)
    html += "    <td" + style2 + ">%s</td>\n" % multiprocessing.cpu_count()
    html += "    <td" + style1 + ">CPU(s)</td>\n"

    # Loop over packages
    for pckg in pckgs:
        i, html = newrow(i, ncol, html)
        html += "    <td" + style2 + ">%s</td>\n" % pckg.__version__
        html += "    <td" + style1 + ">"+pckg.__name__+"</td>\n"
    html += "  </tr>\n"

    # sys.version
    html += "  <tr" + style1 + ">\n"
    html += "     <td" + style1 + " colspan='"
    html += str(2*ncol)+"'>%s</td>\n" % sys.version
    html += "  </tr>\n"

    # vml version
    if numexpr:
        html += "  <tr" + style2 + ">\n"
        html += "    <td" + style2[:-2]
        html += "; text-align: left;' colspan='" + str(2*ncol)
        html += "'>%s</td>\n" % numexpr.get_vml_version()
        html += "  </tr>\n"

    # Finish table
    html += "</table>"

    return html


def _get_text(pckgs):
    """Plain-text version."""

    # Width for text-version
    n = 54

    # Date and time info as title
    date_time_info = time.strftime('%a %b %d %H:%M:%S %Y %Z')
    text = "\n  " + date_time_info + "\n" + n*'-' + '\n'

    # OS and CPUs
    text += '{:>15}'.format(platform.system())+' : OS\n'
    text += '{:>15}'.format(multiprocessing.cpu_count())+' : CPU(s)\n'

    # Loop over packages
    for pckg in pckgs:
        text += '{:>15} : {}\n'.format(pckg.__version__, pckg.__name__)

    # sys.version
    text += '\n'
    for txt in textwrap.wrap(sys.version, n-4):
        text += '  '+txt+'\n'

    # vml version
    if numexpr:
        text += '\n'
        for txt in textwrap.wrap(numexpr.get_vml_version(), n-4):
            text += '  '+txt+'\n'

    # Finish
    text += n*'-'

    return text


def _get_packages(add_pckg):
    """Create list of packages."""

    # Cast add_pckg
    if isinstance(add_pckg, tuple):
        add_pckg = list(add_pckg)
    if not isinstance(add_pckg, list):
        add_pckg = [add_pckg, ]

    # Create package-list
    pckgs = [numpy, scipy, empymod, empyscripts]   # Mandatory ones
    for module in [IPython, numexpr, matplotlib]:  # Optional ones
        if module:
            pckgs += [module]
    pckgs += add_pckg  # Add the ones from the input

    return pckgs


def _check_html_mode(mode):
    """Check HTML and mode."""

    # Check mode, IPython, and no_html
    if mode == 'auto':
        # Check if Jupyter is used or another IPython instance (e.g., terminal)
        # https://github.com/ipython/ipython/issues/9732#issuecomment-231592556
        # Unfortunately, cannot distinguish between Jupyter and Qt console.
        if IPython:
            ip = IPython.get_ipython()
            if ip:
                no_HTML = not ip.has_trait('kernel')
            else:
                no_HTML = True
        else:
            no_HTML = True
    else:
        no_HTML = True

    return no_HTML
