# Python base
FROM python:3.13-slim

# Prevent writing .pyc files and enable better logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies needed for common Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Disable Poetry virtualenv creation (we use container environment)
RUN poetry config virtualenvs.create false

# Copy project metadata
COPY pyproject.toml poetry.lock* /app/

# Install only main dependencies
RUN poetry install --no-root --only main

# Copy the application source code
COPY . /app/

# Expose app port
EXPOSE 8000

# Run Django server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
