#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Collecting Static Files"
#python manage.py collectstatic

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
#test

#gunicorn demo.wsgi:application --bind 0.0.0.0:8000