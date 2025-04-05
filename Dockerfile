# Используем официальный Python-образ (можно выбрать slim-версию)
FROM python:3.12-slim

# Отключаем запись .pyc файлов и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Задаём рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Копируем скрипт entrypoint и делаем его исполняемым
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Указываем, что первым будет выполняться entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# CMD будет выполнен после entrypoint.sh; можно запускать gunicorn или runserver для тестирования
CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8001"]
