#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['koji']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Jason Guiditta",
    author_email='jason.guiditta@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description=("Helper library to work with areas of koji that are "
                 "not well supported in that project's api."),
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='koji_wrapper',
    name='koji_wrapper',
    packages=find_packages(include=['koji_wrapper']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/release-depot/koji_wrapper',
    version='0.2.0',
    zip_safe=False,
)
