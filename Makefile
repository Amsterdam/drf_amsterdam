.PHONY: release dist build test coverage clean distclean

PYTHON = python3

release: test
	twine upload dist/*

dist:
	$(PYTHON) setup.py sdist bdist bdist_wheel

build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) runtests.py
