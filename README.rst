============
Koji Wrapper
============


.. image:: https://img.shields.io/pypi/v/koji_wrapper.svg
        :target: https://pypi.python.org/pypi/koji_wrapper

.. image:: https://img.shields.io/travis/release-depot/koji_wrapper.svg
        :target: https://travis-ci.org/release-depot/koji_wrapper

.. image:: https://readthedocs.org/projects/koji-wrapper/badge/?version=latest
        :target: https://koji-wrapper.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/release-depot/koji_wrapper/shield.svg
     :target: https://pyup.io/repos/github/release-depot/koji_wrapper/
     :alt: Updates



Helper library to work with areas of koji that are not well supported in that project's api.

* Free software: MIT license
* Documentation: https://koji-wrapper.readthedocs.io.


Features
--------

* TODO

Development
-----------

There are several dependencies needed to build and work on koji_wrapper.  Using
your distribution's package manager, install these system packages::

  openssl-devel python3-devel rpm-devel krb5-devel

koji_wrapper uses the upcoming standard of Pipfiles via pipenv.  This is integrated
into our Makefile and once you have the above dependencies, you can simply run::

  make

This will install our dev environment for the package via pipenv.  It is installed
with --user, so it does not affect your site-packages.  Pipenv create a unique virtualenv
for us, which you can activate via::

  pipenv shell

See the `pipenv documentation <https://docs.pipenv.org/>`_ for more detail.

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
