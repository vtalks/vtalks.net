all: migrate server

migrate:
	python manage.py makemigrations
	python manage.py migrate

server:
	python manage.py runserver 0.0.0.0:8000

setup: migrate
	python manage.py createsuperuser

test:
	python manage.py test --settings=settings_test

cover:
	coverage run manage.py test --settings=settings_test
	coverage report
	coverage html