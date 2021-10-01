#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os

from setuptools import setup


# Pypi will not work with the .dev scheme, so exclude that when doing
# test builds in ci.
def check_if_scm():
    if os.environ.get('SCM_NO_LOCAL_SCHEME'):
        return "no-local-version"
    else:
        return "node-and-date"


setup(
    use_scm_version={'local_scheme': check_if_scm()}
)
