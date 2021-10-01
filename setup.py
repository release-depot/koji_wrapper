#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os

from setuptools import setup


# RTD cannot install any dependencies that require C libraries, and since we
# cannot do a conditional in toml, we are stuck with this way of conditionally
# including the real deps for now.
def check_if_rtd():
    on_rtd = os.environ.get('READTHEDOCS') == 'True'
    if on_rtd:
        return ''
    else:
        return ['koji', 'toolchest']


# Pypi will not work with the .dev scheme, so exclude that when doing
# test builds in ci.
def check_if_scm():
    if os.environ.get('SCM_NO_LOCAL_SCHEME'):
        return "no-local-version"
    else:
        return "node-and-date"


setup(
    use_scm_version={'local_scheme': check_if_scm()},
    install_requires=check_if_rtd()
)
