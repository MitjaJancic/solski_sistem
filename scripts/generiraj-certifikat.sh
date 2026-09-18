#!/bin/sh
# Ustvari samopodpisano TLS potrdilo za lokalni razvoj (velja 365 dni).
# V 4. tednu ga na produkcijskem strežniku zamenja pravo potrdilo (Let's Encrypt/Certbot).
set -e

# Prepreči, da bi Git Bash na Windows pot "/C=SI/..." pomotoma pretvoril v datotečno pot.
export MSYS_NO_PATHCONV=1

CILJNA_MAPA="$(dirname "$0")/../nginx/certs"
mkdir -p "$CILJNA_MAPA"

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "$CILJNA_MAPA/samopodpisano.key" \
  -out "$CILJNA_MAPA/samopodpisano.crt" \
  -subj "/C=SI/ST=Slovenija/L=Ljubljana/O=Solski IS/CN=localhost"

echo "Samopodpisano potrdilo ustvarjeno v $CILJNA_MAPA"
