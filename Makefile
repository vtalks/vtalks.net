up:
	docker-compose up -d --build
	# docker-compose run --rm web python3 manage.py createsuperuser

down:
	docker-compose down --volumes --remove-orphans --rmi all
	docker volume prune -f