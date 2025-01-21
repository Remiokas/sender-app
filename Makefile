include .env

PORT=${EVENT_SENDER_PORT}

export-requirements:
	poetry export --output requirements.txt --without-hashes;

install:
	python 3.11 -m venv venv; \
	. venv/Scripts/activate; \
	python 3.11 -m pip install -r requirements.txt

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