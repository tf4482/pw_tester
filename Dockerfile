# Use latest Alpine Linux image
FROM alpine:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PORT=5000

# Install system dependencies including Python 3.11
RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    gcc \
    musl-dev \
    linux-headers \
    python3-dev \
    && ln -sf python3 /usr/bin/python \
    && ln -sf pip3 /usr/bin/pip \
    && rm -rf /var/cache/apk/*

# Install Poetry
RUN pip install --no-cache-dir --break-system-packages poetry

# Set work directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-root \
    && rm -rf $POETRY_CACHE_DIR

# Copy application code
COPY . .

# Create non-root user for security
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the application with gunicorn
CMD ["poetry", "run", "gunicorn", "--config", "gunicorn.conf.py", "web_app:app"]
