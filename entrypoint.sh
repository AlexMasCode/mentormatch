#!/bin/sh
set -e

# Создаём миграции (если изменений моделей нет – команда ничего не сделает)
python manage.py makemigrations

# Применяем миграции
python manage.py migrate

# При необходимости можно добавить сбор статики (если проект её использует)
python manage.py collectstatic --noinput

# Передаём управление основной команде (CMD)
exec "$@"
