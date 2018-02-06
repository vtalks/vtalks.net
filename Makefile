VERSION=`cat VERSION`
PYTHON=python3
DOCKER=docker
DOCKER-COMPOSE=docker-compose


default: help

# Testing

.PHONY: test
test:	## Execute tests suite
	$(DOCKER-COMPOSE) \
		-f ../deploy/docker-compose.yml \
		-f ../deploy/docker-compose-dev.yml \
		exec web $(PYTHON) manage.py test \
		--settings=settings.test

.PHONY: cover
cover:	## Generate coverage report
	$(DOCKER-COMPOSE) \
		-f ../deploy/docker-compose.yml \
		-f ../deploy/docker-compose-dev.yml \
		exec web coverage run manage.py test \
		--settings=settings.test

.PHONY: coveralls
coveralls:	cover ## Send coverage report to coveralls.io
	$(DOCKER-COMPOSE) \
		-f ../deploy/docker-compose.yml \
		-f ../deploy/docker-compose-dev.yml \
		exec web coveralls

# Docker container images

.PHONY: docker
docker: docker-build docker-publish

.PHONY: docker-build
docker-build:	## Builds container and tag resulting image
	docker build --force-rm --tag vtalks/web .
	docker tag vtalks/web vtalks/web:$(VERSION)

.PHONY: docker-publish
docker-publish:	## Publishes container images
	docker push vtalks/web:$(VERSION)
	docker push vtalks/web:latest

.PHONY: help
help:	## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


# Deploy development environment:
# -------------------------------
# - postgresql is exported to host at 5432
# - web is exported to host at 8000
#
# Setup environment:
# $ source .venv/bin/activate
# $ source environment.sh
#
# Create alias:
# $ alias deploy="docker-compose -f deploy/docker-compose.yml"
#
# $ compose up -d
# $ compose exec web python3 manage.py createsuperuser

# How to manage the system:
# -------------------------
#
# Create alias:
# $ alias manage="docker-compose -f deploy/docker-compose.yml exec web python3 manage.py"
#
# Add a talk:
# $ manage add_video https://www.youtube.com/watch?v=ha8gdZ27wMo
#
# Add a playlist:
# $ manage add_playlist https://www.youtube.com/playlist?list=PL2ntRZ1ySWBdD9bru6IR-_WXUgJqvrtx9
