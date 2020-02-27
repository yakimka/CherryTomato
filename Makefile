all: init clean lint test

clean: clean-build clean-pyc  ## Clean build files and pyc files

clean-build:  ## Clean build files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf contrib/pkg
	rm -rf contrib/src
	rm -rf contrib/*.tar.xz

clean-pyc:  ## Clean pyc files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

init:  ## Install test packages
	pip install pytest pytest-qt pytest-mock flake8

test:  ## Run tests
	pytest

flake:  ## Run flake8
	flake8 --statistics --count

lint: flake  ## Run all linters

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
