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

COMMITS_COUNT := 30

whats-new: ## Get info about last tag
	$(eval LAST_TAG := $(shell git describe --abbrev=0 --tags))
	$(eval PREV_TAG := $(shell git describe --abbrev=0 --tags $(LAST_TAG)^ 2>/dev/null || [ ]))
	$(eval TAGS := $(if $(PREV_TAG),$(PREV_TAG)..$(LAST_TAG),$(LAST_TAG)))
	$(eval NUMBER_OF_COMMITS := $(shell git rev-list --count $(TAGS)))
	@echo ""
	@echo "Since the last release there have been $(NUMBER_OF_COMMITS) commit(s). \
	The descriptions for the first (at most) $(COMMITS_COUNT) of these are as follows"
	@echo ""
	@git --no-pager log $(TAGS) --pretty=format:'- %s' | grep -v '^- Merge.*branch.*into' | head -n $(COMMITS_COUNT)
	@echo ""

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
