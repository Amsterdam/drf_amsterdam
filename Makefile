.PHONY: release dist build test coverage clean distclean

PYTHON = python3
DC = docker-compose

release: test
	$(PYTHON) -m twine upload dist/*

dist:
	$(PYTHON) setup.py bdist bdist_wheel

build:
	$(PYTHON) setup.py build

test:
	$(DC) up tests

pip-tools:
	pip install pip-tools

install: pip-tools                  ## Install requirements and sync venv with expected state as defined in requirements.txt
	pip-sync requirements_dev.txt

requirements: pip-tools             ## Upgrade requirements (in requirements.in) to latest versions and compile requirements.txt
	pip-compile --upgrade --output-file requirements.txt requirements.in
	pip-compile --upgrade --output-file requirements_dev.txt requirements_dev.in

upgrade: requirements install       ## Run 'requirements' and 'install' targets
