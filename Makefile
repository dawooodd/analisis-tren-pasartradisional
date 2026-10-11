.PHONY: install scrape etl model app test lint

install:
	pip install -e ".[dev]"
	pre-commit install

scrape:
	python -m agents.orchestrator

etl:
	python -m src.pipeline.run_etl

model:
	python -m src.pipeline.run_models

app:
	streamlit run app/Home.py

test:
	pytest -q

lint:
	ruff check . && mypy agents src
