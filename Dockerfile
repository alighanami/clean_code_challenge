# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (important for psycopg2 for PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    # Clean up APT when done installing dependencies
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock ./

# Install dependencies using Pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# Copy the rest of the application code to the working directory
COPY . /app

# Expose port 8000
EXPOSE 8000

# Run the Django application (This will be overridden by docker-compose command)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
