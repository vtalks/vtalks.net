all: migrate server

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

server:
	python3 manage.py runserver 0.0.0.0:8000

setup: migrate
	python3 manage.py createsuperuser

clean:
	rm -rf db.sqlite3
