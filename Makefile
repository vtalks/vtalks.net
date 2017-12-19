.PHONY: help
help:	## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

# Deploy development environment:
# -------------------------------
# - postgresql is exported to host at 5432
# - web is exported to host at 8000
#
# $ source .venv/bin/activate
# $ source environment.sh
# $ docker-compose -f deploy/docker-compose.yml up
# $ docker-compose -f deploy/docker-compose.yml exec web python3 manage.py createsuperuser