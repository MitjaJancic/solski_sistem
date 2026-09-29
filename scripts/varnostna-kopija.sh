#!/bin/sh
# Varnostna kopija (backup) podatkovne baze MariaDB iz Docker vsebnika `baza`.
# Ustvari stisnjen dump v mapi backup/ izven vsebnika in obdrži zadnjih 7 kopij.
#
# Ročni zagon:   sh scripts/varnostna-kopija.sh
# Samodejno (cron, npr. vsak dan ob 2:30):
#   30 2 * * * cd /pot/do/projekta && sh scripts/varnostna-kopija.sh >> backup/backup.log 2>&1
set -e

KOREN="$(cd "$(dirname "$0")/.." && pwd)"
CILJ="$KOREN/backup"
mkdir -p "$CILJ"

# Preberi ime baze in geslo iz .env
if [ -f "$KOREN/.env" ]; then
  # shellcheck disable=SC1090
  . "$KOREN/.env"
fi
DB_IME="${DB_IME:-sola_is}"

CAS="$(date +%Y%m%d_%H%M%S)"
DATOTEKA="$CILJ/${DB_IME}_${CAS}.sql.gz"

echo "Izdelujem varnostno kopijo baze '${DB_IME}' → ${DATOTEKA}"
docker compose exec -T baza \
  sh -c "exec mariadb-dump -u root -p\"\$MARIADB_ROOT_PASSWORD\" --single-transaction --databases ${DB_IME}" \
  | gzip > "$DATOTEKA"

echo "Kopija ustvarjena ($(du -h "$DATOTEKA" | cut -f1))."

# Obdrži zadnjih 7 kopij, starejše pobriši.
ls -1t "$CILJ"/${DB_IME}_*.sql.gz 2>/dev/null | tail -n +8 | while read -r stara; do
  echo "Brišem staro kopijo: $stara"
  rm -f "$stara"
done

echo "Končano."
