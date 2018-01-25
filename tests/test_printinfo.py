import pytest

from empyscripts import versions

# Note: Tests assume that there is no IPython in the test environment.


def test_versions(capsys):

    # Check the 'auto'-version, providing a package
    versions(add_pckg=pytest)
    out1, _ = capsys.readouterr()

    # Check one of the standard packages
    assert 'numpy' in out1

    # Check the provided package, with number
    assert pytest.__version__ + ' : pytest' in out1

    # Check the 'text'-version, providing a package as tuple
    versions('print', add_pckg=(pytest, ))
    out2, _ = capsys.readouterr()

    # They have to be the same, except time (run at slightly different times)
    assert out1[:-50] == out2[:-50]

    # Check the 'plain'-version, providing a package as list
    out3 = versions('plain', add_pckg=[pytest, ])

    # Check one of the standard packages
    assert 'numpy' in out3

    # Check the provided package, with number
    assert pytest.__version__ + ' : pytest' in out3

    # Check html-version, providing a package as a list
    out4 = versions('html', add_pckg=[pytest])

    # Check row of provided package, with number
    teststr = "<td style='background-color: #ccc; border: 2px solid #fff;'>"
    teststr += pytest.__version__
    teststr += "</td>\n    <td style='"
    teststr += "border: 2px solid #fff; text-align: left;'>pytest</td>"
    assert teststr in out4
