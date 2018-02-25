Steps to carry out for a new release
====================================

Note: I really should replace this with an automatic deploy-setup...

   1. Update:
      - ``CHANGELOG``
      - ``setup.py``: Version number, download url; DO NOT CHANGE THAT
      - ``empyscripts/__init__.py``: Check version number, remove '.dev?'.
      - ``README.md``: Remove all batches

   2. Remove any old stuff (just in case)

        rm -rf build/ dist/ empyscripts.egg-info/

   3. Push it to GitHub, create a release tagging it

   4. Get the Zenodo-DOI and add it to release notes

   5. Ensure ``python3-setuptools`` is installed:

        sudo apt install python3-setuptools

   6. Create tar and wheel

        python setup.py sdist
        python setup.py bdist_wheel

   7. Test it on testpypi (requires ~/.pypirc)

        twine upload dist/* -r testpypi

   8. Push it to PyPi (requires ~/.pypircs)

        twine upload dist/*

   9. conda build

   Has to be done outside of ~/, because conda skeleton cannot handle, at the
   moment, the encrypted home.
   https://conda.io/docs/build_tutorials/pkgs.html


        # Install miniconda in /opt
        wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
        bash miniconda.sh -b -p /opt/miniconda/miniconda
        export PATH="/opt/miniconda/miniconda/bin:$PATH"
        conda update conda
        conda install conda-build anaconda-client
        conda config --set anaconda_upload yes
        anaconda login

        # Now to the conda-build part
        conda skeleton pypi empyscripts
        # Cannot find empymod, matplotlib (why?)
        # => add empymod, matplotlib to meta.yaml -host and -run
        conda build --python 3.4 empyscripts
        conda build --python 3.5 empyscripts
        conda build --python 3.6 empyscripts

        # Convert for all platforms

        conda convert --platform all /opt/miniconda/miniconda/conda-bld/linux-64/empyscripts-[version]-py34_0.tar.bz2
        conda convert --platform all /opt/miniconda/miniconda/conda-bld/linux-64/empyscripts-[version]-py35_0.tar.bz2
        conda convert --platform all /opt/miniconda/miniconda/conda-bld/linux-64/empyscripts-[version]-py36_0.tar.bz2

        # Upload them
        anaconda upload osx-64/*
        anaconda upload win-*/*
        anaconda upload linux-32/*

        # Logout
        anaconda logout

   10. Post-commit changes
      - ``setup.py``: Bump number, add '.dev0' to version number
      - ``empyscripts/__init__.py``: Bump number, add '.dev0' to version number
      - ``README.md``: Add the current batches (|docs| |tests| |coverage|)
