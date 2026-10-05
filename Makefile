PYTHON = python3
DC = docker compose run --rm tests

pytest:
	$(DC) uv run pytest --cov --cov-fail-under=100

isort:
	$(DC) uv run isort . --check --diff

flake8:
	$(DC) uv run flake8

mypy:
	$(DC) uv run bash -c "mypy . --strict | mypy-baseline filter"

mypy-sync-baseline:
	$(DC) uv run bash -c "mypy . --strict | mypy-baseline sync"

test: pytest isort flake8 mypy

install:                            ## Install requirements and sync venv with expected state as defined in requirements.txt
	uv sync --locked

requirements:                       ## Not used
	@echo "Make requirements is not used. This library does explicitly not pin its dependencies."

upgrade: requirements install       ## Run 'requirements' and 'install' targets
