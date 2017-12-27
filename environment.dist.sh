#!/usr/bin/env bash

# virtualenv
source .venv/bin/activate

# Twitter
export TWITTER_TOKEN=''
export TWITTER_SECRET=''
# Youtube
export YOUTUBE_API_KEY=''

# Aliases
alias deploy="docker-compose -f deploy/docker-compose.yml"
alias manage="docker-compose -f deploy/docker-compose.yml exec web python3 manage.py"
