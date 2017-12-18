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

test:
	python manage.py test

cover:
	coverage run --source='.' --omit='*/migrations/*.py,manage.py,config/*' manage.py test
	coverage report -m