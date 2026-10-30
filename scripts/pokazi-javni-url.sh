#!/bin/sh
# Skripta poišče in izpiše ZADNJI veljavni javni HTTPS naslov Cloudflare tunela
URL=$(docker compose logs tunel 2>&1 | grep -oE "https://[a-zA-Z0-9-]+\.trycloudflare\.com" | tail -n 1)
if [ -n "$URL" ]; then
    echo ""
    echo "=========================================================="
    echo "  JAVNA DOMENA DELUJE (Cloudflare Tunnel):"
    echo "  $URL"
    echo "=========================================================="
    echo "Povezavo lahko odprete na telefonu ali jo posredujete mentorju."
    echo ""
else
    echo "Tunel se še zaganja ali ni zagnan. Zaženite: docker compose up -d"
fi
