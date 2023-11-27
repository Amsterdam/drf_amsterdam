.PHONY: release dist build test coverage clean distclean

PYTHON = python3
DC = docker-compose run --rm tests

release: test
	$(PYTHON) -m twine upload dist/*

dist:
	$(PYTHON) setup.py bdist bdist_wheel

build:
	$(PYTHON) setup.py build

pytest:
	$(DC) pytest --cov --cov-fail-under=100

isort:
	$(DC) isort . --check --diff

flake8:
	$(DC) flake8

mypy:
	$(DC) bash -c "mypy datapunt_api/ --strict | mypy-baseline filter"

test: pytest isort flake8 mypy

install:                            ## Install requirements and sync venv with expected state as defined in requirements.txt
	pip install --upgrade -r requirements.txt -r requirements_dev.txt

requirements:                       ## Not used
	@echo "Make requirements is not used. This library does explicitly not pin its dependencies."

upgrade: requirements install       ## Run 'requirements' and 'install' targets
