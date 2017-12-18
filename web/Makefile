all: migrate server

migrate:
	python manage.py makemigrations
	python manage.py migrate

server:
	python manage.py runserver 0.0.0.0:8000

setup: migrate
	python manage.py createsuperuser

clean:
	rm -rf db.sqlite3
	rm -rf .cover
	coverage erase

test:
	python manage.py test

cover:
	coverage run manage.py test
	coverage report
	coverage html