#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python3 manage.py makemigrations

# Execute database migrations
echo "Execute database migrations"
python3 manage.py migrate

# Start server
echo "Start server"
python3 manage.py runserver 0.0.0.0:8000
