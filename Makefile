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
# $ deploy up -d
# $ deploy exec web python3 manage.py createsuperuser

# How to manage the database:
# ---------------------------
#
# Create alias:
# $ alias manage="docker-compose -f deploy/docker-compose.yml exec web python3 manage.py"
#
# Add a talk:
# $ manage add_video https://www.youtube.com/watch?v=ha8gdZ27wMo
#
# Add a playlist:
# $ manage add_playlist https://www.youtube.com/playlist?list=PL2ntRZ1ySWBdD9bru6IR-_WXUgJqvrtx9
