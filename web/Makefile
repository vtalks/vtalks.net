VERSION=`cat ../VERSION`

.PHONY: build
build: 	## Builds container images and tag them with the current version
	docker build --force-rm -t vtalks/web .
	docker tag vtalks/web vtalks/web:$(VERSION)

.PHONY: push
push:	build	## Pushes the built containers to the register
	docker push vtalks/web:$(VERSION)
	docker push vtalks/web:latest


.PHONY: help
help:	## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
