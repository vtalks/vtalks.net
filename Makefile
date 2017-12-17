up:
	docker-compose up -d --build
	# docker-compose run --rm web python3 manage.py createsuperuser

down:
	docker-compose down --volumes --remove-orphans --rmi all
	docker volume prune -f

clean:
	find . -type d -name "migrations" -print0|xargs -0 rm -r --
	find . -type d -name "__pycache__" -print0|xargs -0 rm -r --