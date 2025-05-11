FROM python:3.13-slim AS base

# Set common environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    POETRY_VERSION=2.1.2 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    INITIALIZE_VECTOR_DB=true

# Set working directory
WORKDIR /app

# Install system dependencies in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Install Poetry
    curl -sSL https://install.python-poetry.org | python3 - && \
    # Add Poetry to PATH
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry && \
    # Verify Poetry is installed
    poetry --version && \
    # Create directory structure
    mkdir -p /app/data/chroma_db && \
    chmod -R 777 /app/data

# Copy only the dependency files first
COPY pyproject.toml ./
RUN touch README.md

# Generate lock file and install dependencies - Use the same base image
FROM base AS dependencies

# Generate the lock file
RUN poetry --version && poetry lock

# Install main dependencies
RUN poetry install --no-interaction --no-ansi --only main --no-root

# Install UI dependencies separately to improve caching - Use the dependencies stage
FROM dependencies AS ui-dependencies
RUN poetry install --no-interaction --no-ansi --with ui --no-root

# Final stage with minimal image
FROM python:3.13-slim AS runtime

# Set runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    INITIALIZE_VECTOR_DB=true

# Install minimal runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/data/chroma_db && \
    chmod -R 777 /app/data

# Set working directory
WORKDIR /app

# Copy installed packages from dependency stage
COPY --from=ui-dependencies /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=ui-dependencies /usr/local/bin /usr/local/bin

# Copy entrypoint script and make executable
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Copy application code last to improve caching
COPY . .

# Expose ports
EXPOSE 8000 8501

# Set entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default command
CMD ["uvicorn", "ui.api:app", "--host", "0.0.0.0", "--port", "8000"] 