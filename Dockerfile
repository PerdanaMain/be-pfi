# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11-slim as builder

# Install Poetry
RUN pip install poetry

# Set environment variables for Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory
WORKDIR /app

# Copy the Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --only main --no-root

# Use a new slim image for the runtime
FROM python:3.11-slim as runtime

# Install necessary tools for running the app, including `make`
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy Poetry installation from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application files
COPY . /app/

RUN echo "# Custom configurations added by Dockerfile" >> /root/.bashrc && \
    echo "export APP_PATH=/app" >> /root/.bashrc && \
    echo "alias ll='ls -la'" >> /root/.bashrc && \
    echo "PASSWORD=\"Aimo@2024\"" >> /root/.bashrc && \
    echo "echo -n \"Enter password to access container: \"" >> /root/.bashrc && \
    echo "read -s input_password" >> /root/.bashrc && \
    echo "echo \"\"" >> /root/.bashrc && \
    echo "if [ \"\$input_password\" != \"\$PASSWORD\" ]; then" >> /root/.bashrc && \
    echo "    echo \"Access denied!\"" >> /root/.bashrc && \
    echo "    exit 1" >> /root/.bashrc && \
    echo "fi" >> /root/.bashrc && \
    echo "cd /app" >> /root/.bashrc

# Expose port for the application
EXPOSE 5000

# Set the working directory
WORKDIR /app

# Run `make run` as the entry point
CMD ["gunicorn", "-c", "gunicorn.py", "main:app"]
