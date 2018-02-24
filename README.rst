empyscripts
###########

.. image:: https://travis-ci.org/empymod/empyscripts.svg?branch=master
   :target: https://travis-ci.org/empymod/empyscripts
   :alt: Travis-CI
.. image:: https://coveralls.io/repos/github/empymod/empyscripts/badge.svg?branch=master
   :target: https://coveralls.io/github/empymod/empyscripts?branch=master
   :alt: Coveralls

This repo contains *add-ons* for ``empymod``. These are scripts that did not
make it into ``empymod``. Most likely because they require some sort of change
to the ``empymod`` core features, but are only for a very specific use cases.
Hence it was decided to not implement them in ``empymod``.

Please note that these add-ons are not as thoroughly tested as ``empymod``, and
potentially not as well documented either.


More information
================

For information regarding ``empymod`` have a look at https://empymod.github.io.


Installation
============

You can install empyscripts via ``conda``

.. code-block:: console

   > conda install -c prisae empyscripts

via ``pip``:

.. code-block:: console

   > pip install empyscripts

or download this repo and run

.. code-block:: console

    > python setup.py install


Add-ons
=======

- ``tmtemod``: Return up- and down-going TM/TE-mode contributions for x-directed
  electric sources and receivers, which are located in the same layer.
- ``fdesign``: Design digital linear filters for the Hankel and Fourier
  transforms.

There is also ``empyscripts.versions()``: ``versions('HTML')`` (in Jupyter
Notebooks) or ``versions()`` (in IPython, QT, and Python consoles) can be used
to show date, time, and package version information at the end of a notebook or
script.


License information
===================

Copyright 2017-2018 Dieter Werthmüller

Licensed under the Apache License, Version 2.0. See the ``LICENSE``-file or the
documentation for more information.
