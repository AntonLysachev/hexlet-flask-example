install:
		poetry install

start:
		flask --app example --debug run --port 8000

env-start:
		poetry run flask --app example --debug run --port 8000

start guincorn:
		poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 example:app