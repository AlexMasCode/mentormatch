# Use the official Python image (you can choose the slim version)
FROM python:3.12-slim

# Disable writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Specify that entrypoint.sh will be executed first
ENTRYPOINT ["/app/entrypoint.sh"]

# CMD will be executed after entrypoint.sh; you can run gunicorn or runserver for testing
CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000"]
