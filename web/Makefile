cover:	## Execute all tests and report coverage results
	coverage run manage.py test --settings=settings_test
	coverage report
	coverage html

.PHONY: help
help:	## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


# How to manage the database
#
# Add a talk
# $ dc -f deploy/docker-compose.yml exec web python3 manage.py add_video https://www.youtube.com/watch?v=ha8gdZ27wMo
#
# Add a playlist
# $ dc -f deploy/docker-compose.yml exec web python3 manage.py add_playlist https://www.youtube.com/playlist?list=PL2ntRZ1ySWBdD9bru6IR-_WXUgJqvrtx9
