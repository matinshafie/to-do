#!/bin/sh
set -e

if [ -n "$MYSQL_HOST" ]; then
    echo "Waiting for MySQL at $MYSQL_HOST:${MYSQL_PORT:-3306}..."
    until python - <<'PYEOF'
import os
import socket
import sys

host = os.environ["MYSQL_HOST"]
port = int(os.environ.get("MYSQL_PORT", "3306"))

try:
    with socket.create_connection((host, port), timeout=2):
        sys.exit(0)
except OSError:
    sys.exit(1)
PYEOF
    do
        sleep 1
    done
    echo "MySQL is up."
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting: $@"
exec "$@"