.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := @pipenv run python -c "$$BROWSER_PYSCRIPT"

PIPENV_AVAILABLE := $(shell command -v pipenv 2> /dev/null)

help:
	@pipenv run python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	pipenv run tox -eflake8

test: ## run tests quickly with the default Python
	pipenv run  tox -epy

test-all: ## run tests on every Python version with tox
	pipenv run tox

coverage: ## check code coverage quickly with the default Python
	pipenv run  tox -epy

docs: ## generate Sphinx HTML documentation, including API docs
	pipenv run sphinx-apidoc -o docs/ koji_wrapper ##TODO: remove
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	pipenv run watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	pipenv run twine upload dist/*

dist: clean ## builds source and wheel package
	pipenv run tox -etwine
	ls -l dist

install: ## install the package to the active Python's site-packages
	python setup.py install

dev: clean ## set up a development environment
ifndef PIPENV_AVAILABLE
	pip3 install --user pipenv
endif
	pipenv install --dev

reset: clean ## clean out your pipenv virtualenv
	pipenv uninstall --all
