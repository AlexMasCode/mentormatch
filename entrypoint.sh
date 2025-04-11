#!/bin/sh
set -e

if [ "$SKIP_MIGRATIONS" != "true" ]; then
    echo "Applying migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

echo "Starting application..."
exec "$@"
