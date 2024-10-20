PORT ?= 8000

install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app --debug run

lint:
	poetry run flake8

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app --reload

build:
	./build.sh