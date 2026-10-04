#!/bin/bash
set -e

echo "=== Starting Supplier Quality Review Portal ==="
echo "Author: AADITYA ASWALE (23102B0044)"

# Wait for PostgreSQL if configured
if [ "$USE_SQLITE" != "True" ] && [ "$USE_SQLITE" != "true" ]; then
    echo "Waiting for PostgreSQL database at ${DB_HOST}:${DB_PORT}..."
    while ! nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null && ! curl -s "http://${DB_HOST}:${DB_PORT}" 2>/dev/null; do
        # Use python socket check
        python -c "
import socket, time, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('$DB_HOST', int('$DB_PORT')))
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
" && break
        echo "PostgreSQL is unavailable - sleeping 1s"
        sleep 1
    done
    echo "PostgreSQL is reachable!"
fi

echo "Running database migrations..."
python backend/manage.py migrate --noinput

echo "Collecting static assets..."
python backend/manage.py collectstatic --noinput --clear

echo "Seeding default demonstration data..."
python backend/manage.py seed_portal

echo "Starting Gunicorn WSGI server on 0.0.0.0:8000..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
