#!/bin/sh
set -e

echo "Čakam na podatkovno bazo ${DB_GOSTITELJ}:${DB_VRATA} ..."
until python - <<'PY'
import os, socket, sys
try:
    socket.create_connection((os.environ["DB_GOSTITELJ"], int(os.environ["DB_VRATA"])), timeout=2)
except OSError:
    sys.exit(1)
PY
do
  sleep 1
done
echo "Baza je dosegljiva."

python manage.py migrate --noinput

exec "$@"
