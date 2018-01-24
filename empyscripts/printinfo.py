"""
Add-on for `empymod`: tools to print date, time, and version information
========================================================================

Print date, time, and package version information in any environment (Jupyter
notebook, IPython console, Python console, QT console).

    - versions : Print a nice html-table in a Jupyter notebook. If it is called
                 from an IPython console or a Python console then it calls
                 `versions_rawtxt`. This does not work in a QT console, as it
                 returns a HTML object which cannot be rendered. Use
                 `versions_rawtxt` in QT consoles.

    - versions_rawtxt : Print information to stdout in plain text. Works for
                        all environments.

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
    # Check if Jupyter is used or another IPython instance (e.g., terminal)
    # https://github.com/ipython/ipython/issues/9732#issuecomment-231592556
    ip = IPython.get_ipython()
    if ip:
        no_HTML = not ip.has_trait('kernel')
    else:
        no_HTML = True
except ImportError:
    IPython = False
    no_HTML = True


def versions(add_pckg=[]):
    """Return date, time, and version information in Jupyter as a html table.

    Works for Jupyter notebooks. If called from Ipython or Python consoles,
    it will run `versions_rawtxt(add_pckg)` instead. DOES NOT work in QT
    consoles, use `versions_rawtxt(add_pckg)`.


    Parameters
    ----------
    add_pckg : modules, optional
        Module or list of modules to add to output information.


    Returns
    -------
    A `IPython.display.HTML`-object, which is rendered in the notebook. If
    called from something else than a notebook, the output is directly printed
    to stdout.


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

    # Call rawtxt if not in jupyter notebook
    if no_HTML:
        versions_rawtxt(add_pckg)
        return

    # Get required modules
    pckgs = _get_modules(add_pckg)

    # Define styles
    style1 = " style='border: 2px solid #fff; text-align: left;'"
    style2 = " style='background-color: #ccc; border: 2px solid #fff;'"

    # Print date and time info as title
    html = "<h3>%s</h3>" % time.strftime('%a %b %d %H:%M:%S %Y %Z')

    # Start table
    html += '<table>'

    # OS and CPUs
    html += "<tr" + style1 + ">"
    html += "<td" + style2 + ">%s</td>" % platform.system()
    html += "<td" + style1 + ">OS</td>"
    html += "<td" + style2 + ">%s</td>" % multiprocessing.cpu_count()
    html += "<td" + style1 + ">CPU(s)</td>"
    i = 2

    # Loop over packages
    for pckg in pckgs:
        html += "<td" + style2 + ">%s</td>" % pckg.__version__
        html += "<td" + style1 + ">"+pckg.__name__+"</td>"
        i += 1
        if i % 3 == 0:
            html += "</tr>"
            html += "<tr" + style1 + ">"
    html += "</tr>"

    # sys.version
    html += "<tr" + style1 + ">"
    html += "<td" + style1 + " colspan='6'>%s</td>" % sys.version
    html += "</tr>"

    # vml version
    if numexpr:
        html += "<tr" + style2 + ">"
        html += "<td" + style2
        html += " colspan='6'>%s</td>" % numexpr.get_vml_version()
        html += "</tr>"

    # Finish table
    html += "</table>"

    return HTML(html)


def versions_rawtxt(add_pckg=[]):
    """Print date, time, and version information in plain text.

    Works for any environment
    """

    # width
    n = 54

    # Get required modules
    pckgs = _get_modules(add_pckg)

    # Print date and time info as title
    print(time.strftime('\n  %a %b %d %H:%M:%S %Y %Z'))
    print(n*'-')

    # OS and CPUs
    print('{:>15}'.format(platform.system())+' : OS')
    print('{:>15}'.format(multiprocessing.cpu_count())+' : CPU(s)')

    # Loop over packages
    for pckg in pckgs:
        print('{:>15}'.format(pckg.__version__)+' : '+pckg.__name__)

    # sys.version
    print()
    for txt in textwrap.wrap(sys.version, n-4):
        print('  '+txt)

    # vml version
    if numexpr:
        print()
        for txt in textwrap.wrap(numexpr.get_vml_version(), n-4):
            print('  '+txt)

    print(n*'-')


def _get_modules(add_pckg):
    """Create list of modules."""

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
