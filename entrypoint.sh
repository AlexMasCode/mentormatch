#!/bin/sh
set -e

if [ "$SKIP_MIGRATIONS" != "true" ]; then
    echo "Applying migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

echo "Creating admin user if not exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
admin_email = "${ADMIN_EMAIL}"
if not User.objects.filter(email=admin_email).exists():
    User.objects.create_superuser(
        email=admin_email,
        first_name="${ADMIN_FIRST_NAME}",
        last_name="${ADMIN_LAST_NAME}",
        password="${ADMIN_PASSWORD}",
        role="ADMIN"
    )
EOF

echo "Starting application..."
exec "$@"
