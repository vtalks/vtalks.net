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
		exec web coverage run --rcfile=.coveragerc manage.py test \
		--settings=settings.test

.PHONY: coverage-report
coverage-report:
	$(DOCKER-COMPOSE) \
		-f ../deploy/docker-compose.yml \
		-f ../deploy/docker-compose-dev.yml \
		exec web coverage report --show-missing --skip-covered --rcfile=.coveragerc

.PHONY: coverage-html
coverage-html:
	$(DOCKER-COMPOSE) \
		-f ../deploy/docker-compose.yml \
		-f ../deploy/docker-compose-dev.yml \
		exec web coverage html --directory ../.cover --rcfile=.coveragerc

.PHONY: coveralls
coveralls:	cover ## Send coverage report to coveralls.io
	$(DOCKER-COMPOSE) \
		-f ../deploy/docker-compose.yml \
		-f ../deploy/docker-compose-dev.yml \
		exec web codecov

# Docker container images

.PHONY: docker	## Builds and publishes the container
docker: docker-build docker-publish

.PHONY: docker-build
docker-build:	## Builds container and tag resulting image
	docker build --force-rm --tag vtalks/web .
	docker tag vtalks/web vtalks/web:$(VERSION)

.PHONY: docker-publish
docker-publish:	## Publishes container images
	docker push vtalks/web:$(VERSION)
	docker push vtalks/web:latest

include Makefile.help.mk
