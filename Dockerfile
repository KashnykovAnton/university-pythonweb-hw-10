# First stage - get PostgreSQL client tools
FROM postgres:17 as pgclient

# Second stage - your main app
FROM python:3.13-slim

# Install only the essential PostgreSQL client libraries
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Then copy the binaries from postgres:17
COPY --from=pgclient /usr/lib/postgresql/17/bin/pg_dump /usr/bin/
COPY --from=pgclient /usr/lib/postgresql/17/bin/pg_restore /usr/bin/

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.1.1
RUN pip install "poetry==$POETRY_VERSION"

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --without dev

# Copy application code
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["sh", "-c", "alembic upgrade head && python -m sync_databases && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]