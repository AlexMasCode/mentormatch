#!/bin/sh
set -e

# Create migrations (if there are no changes in models – this command does nothing)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files (if the project uses static files)
python manage.py collectstatic --noinput

# Pass control to the main command (CMD)
exec "$@"
