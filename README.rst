empyscripts
###########

.. image:: https://readthedocs.org/projects/empyscripts/badge/?version=latest
   :target: http://empyscripts.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://travis-ci.org/empymod/empyscripts.svg?branch=master
   :target: https://travis-ci.org/empymod/empyscripts
   :alt: Travis-CI
.. image:: https://coveralls.io/repos/github/empymod/empyscripts/badge.svg?branch=master
   :target: https://coveralls.io/github/empymod/empyscripts?branch=master
   :alt: Coveralls

.. sphinx-inclusion-marker

**Note**: ``v0.3.2`` is the *last release* of ``empyscripts``. From ``empymod
v1.7.0`` onwards ``empyscripts`` is directly included in ``empymod`` as
``empymod.scripts``.

The **empyscripts** are *add-ons* for the electromagnetic modeller **empymod**.
These add-ons provide some very specific, additional functionalities:

- ``tmtemod``: Return up- and down-going TM/TE-mode contributions for
  x-directed electric sources and receivers, which are located in the same
  layer.
- ``fdesign``: Design digital linear filters for the Hankel and Fourier
  transforms.

There is also ``empyscripts.versions()``, which can be used to show date, time,
and package version information at the end of a notebook or script:

- ``versions('HTML')`` for Jupyter Notebooks, and
- ``versions()`` for IPython, QT, and Python consoles.

See https://empymod.github.io/#features for a complete list of features of
empymod.


More information
================

For more information regarding installation, usage, add-ons, contributing,
roadmap, bug reports, and much more, see

- **Website**: https://empymod.github.io,
- **Documentation empymod**: https://empymod.readthedocs.io,
- **Documentation add-ons**: https://empyscripts.readthedocs.io,
- **Source Code**: https://github.com/empymod,
- **Examples**: https://github.com/empymod/example-notebooks.


License information
===================

Copyright 2017-2018 Dieter Werthmüller

Licensed under the Apache License, Version 2.0. See the ``LICENSE``-file or the
documentation for more information.
