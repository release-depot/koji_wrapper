============
Koji Wrapper
============


.. image:: https://img.shields.io/pypi/v/koji_wrapper.svg
        :target: https://pypi.python.org/pypi/koji_wrapper

.. image::
   https://github.com/release-depot/koji_wrapper/actions/workflows/test.yml/badge.svg
   :target: `test workflow`_

.. image:: https://readthedocs.org/projects/koji_wrapper/badge/?version=latest
        :target: https://koji_wrapper.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. _test workflow: https://github.com/release-depot/koji_wrapper/actions/workflows/test.yml


Helper library to work with areas of koji that are not well supported in that project's api.

* Free software: MIT license


Notes
-----

This library only supports python 3. Some features may still work with python
2.7 but not all of the syntax and features may be compatible.

Development
-----------

There are several dependencies needed to build and work on koji_wrapper.  These
are a result of a dependency upstream from us in the `cryptography`_ library,
which lists the packages needed if you run into problems pip installing our
requirements.

.. _cryptography:  https://cryptography.io/en/latest/installation/

koji_wrapper supports both standard python virtual environment setups and pipenv,
which is integrated into our Makefile. To set up a pipenv-based development
environment, you can simply run::

  make dev

This will install our dev environment for the package via pipenv.  It is installed
with --user, so it does not affect your site-packages.  Pipenv creates a unique virtualenv
for us, which you can activate via::

  pipenv shell

See the `pipenv documentation <https://docs.pipenv.org/>`_ for more detail.

Alternatively, you can use a standard python virtualenv if you prefer.

Documentation
*************

To build the documentation on your checkout, simply run::

  make docs

This is useful for verifying any documentation you have changed or added is
generated correctly and looks as expected before submitting a Pull Request.

Contributions
*************

All new code should include tests that excercise the code and prove that it
works, or fixes the bug you are trying to fix.  Any Pull Request without tests
will not be accepted. See CONTRIBUTING.rst for more details.

Building
********

If you wish to build a local package for testing at any time, you can simply
run::

  make dist

this will build a package with a .dev extension that you can install for testing
and verification.
