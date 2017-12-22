cover:	## Execute all tests and report coverage results
	coverage run manage.py test --settings=config.settings_test
	coverage report
	coverage html

.PHONY: help
help:	## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
