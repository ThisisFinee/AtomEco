#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate

echo "Starting Gunicorn server..."
exec "$@"