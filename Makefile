up:
	docker-compose up -d --build

down:
	docker-compose down --volumes --remove-orphans --rmi all
