import pytest

from empyscripts import printinfo


def test_versions(capsys):

    # Check the rawtxt-version, providing a package
    printinfo.versions_rawtxt(pytest)
    out1, _ = capsys.readouterr()

    # Check the 'normal'-version, providing a package as tuple
    # Tests run without IPython, so versions will switch to versions_rawtxt.
    # We do not test the html-version therefore
    printinfo.versions((pytest,))
    out2, _ = capsys.readouterr()

    # They have to be the same, because there is no IPython
    assert out1 == out2

    # Check one of the standard packages
    assert 'numpy' in out2

    # Check the provided package, with number
    assert pytest.__version__ + ' : pytest' in out2
