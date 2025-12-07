# Use an official Python image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock* /app/

## Install Python dependencies
RUN poetry install --no-root --only main
#
## Copy the rest of the application
#COPY . /app

# Install dependencies
#RUN poetry install --no-interaction

# Copy the rest of the code
COPY . /app

EXPOSE 8000

# Run Django
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]