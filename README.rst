============
Koji Wrapper
============


.. image:: https://img.shields.io/pypi/v/koji_wrapper.svg
        :target: https://pypi.python.org/pypi/koji_wrapper

.. image:: https://img.shields.io/travis/release-depot/koji_wrapper.svg
        :target: https://travis-ci.org/release-depot/koji_wrapper


Helper library to work with areas of koji that are not well supported in that project's api.

* Free software: MIT license


Features
--------

* TODO

Notes
-----

This library only supports python 3. Some features may still work with python
2.7 but not all of the syntax and features my be compatible.

Development
-----------

There are several dependencies needed to build and work on koji_wrapper.  Using
your distribution's package manager, install these system packages::

  openssl-devel python3-devel rpm-devel krb5-devel make gcc findutils which

koji_wrapper uses the upcoming standard of Pipfiles via pipenv.  This is integrated
into our Makefile and once you have the above dependencies, you can simply run::

  make dev

This will install our dev environment for the package via pipenv.  It is installed
with --user, so it does not affect your site-packages.  Pipenv creates a unique virtualenv
for us, which you can activate via::

  pipenv shell

See the `pipenv documentation <https://docs.pipenv.org/>`_ for more detail.

Documentation
*************

To build the documentation on your checkout, simply run::

  make docs

We plan to get this published in the near future, and this README will be
updated when that happens.

Contributions
*************

All new code should include tests that excercise the code and prove that it
works, or fixes the bug you are trying to fix.  Any Pull Request without tests
will not be accepted.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
