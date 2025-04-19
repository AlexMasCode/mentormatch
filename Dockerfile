FROM python:3.12-slim

# Disable writing .pyc files and enable unbuffered output

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

# Copy and install dependencies

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

# Copy and set up entrypoint script

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Use entrypoint to run migrations, collectstatic, then start the app

ENTRYPOINT ["/app/entrypoint.sh"]

# Default command: run the Django app with Gunicorn on port 8000

CMD ["gunicorn", "session_rating_service.wsgi:application", "--bind", "0.0.0.0:8000"]