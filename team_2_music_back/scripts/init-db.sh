#!/bin/bash
set -e

# Wait for database to be ready
# (Docker Compose depends_on handles this mostly, but good for safety)

echo "Running database migrations..."
alembic upgrade head

echo "Database initialized."
