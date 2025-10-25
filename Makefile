.PHONY: lint test format

lint:
	python -m ruff check backend scripts tests

format:
	python -m ruff format backend scripts tests

test:
	pytest --maxfail=1
