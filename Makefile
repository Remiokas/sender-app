include .env

PORT=${EVENT_SENDER_PORT}

export-requirements:
	poetry export --output requirements.txt --without-hashes;

install:
	py -m venv venv; \
	. venv/Scripts/activate; \
	pip install poetry==1.1.15 \
	export-requirements \
	python -m pip install -r requirements.txt

clean:
	find . -name "*.pyc" -exec rm -rf '{}' \; ; \
	rm -rf venv;

run:
	. venv/Scripts/activate; \
	PYTHONPATH=. uvicorn app.main:app --port $(PORT) --reload

pre-commit:
	poetry run pre-commit run --all-files;

lint:
	black app;
	black tests;
	flake8 app;
	flake8 tests;