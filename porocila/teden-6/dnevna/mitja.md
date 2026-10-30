# Dnevna poročila – Mitja Jančič (vzdrževalec IS + razvijalec)

## 2026-10-19

**Kaj sem delal:**
- vzpostavitev produkcijske konfiguracije: streženje spletne aplikacije prek WSGI strežnika `gunicorn` in knjižnice `WhiteNoise` za učinkovito streženje statičnih datotek
- premik razvojnih pripomočkov (Adminer, lokalno mapiranje kode, `runserver`) v `docker-compose.override.yml`, tako da je osnovni `docker-compose.yml` pripravljen za produkcijo
- vklop produkcijskih varnostnih nastavitev v `settings.py` ob izklopu `DJANGO_DEBUG` (varni piškotki `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`, `SECURE_SSL_REDIRECT`, HSTS)

**Kaj sem dokončal:**
- ločena čista produkcijska in razvojna okoljska sestava

**Kaj mi ni uspelo in zakaj:**
- pri `collectstatic` je bilo potrebno zagotoviti obstoj mape `staticfiles/` pred zagonom vsebnika.

## 2026-10-20

**Kaj sem delal:**
- zaključni preizkus delovanja Cloudflare tunela in zanesljivosti javnega dostopa
- posodobitev skript `scripts/pokazi-javni-url.ps1` in `scripts/pokazi-javni-url.sh`, da vedno natančno izpišeta zadnji veljaven URL iz dnevniških zapisov
- preizkus dostopnosti delujoče aplikacije prek javnega spleta na telefonu in računalniku
- zaključni preizkus varnostne kopije z zagonom `scripts/varnostna-kopija.sh`

**Kaj sem dokončal:**
- potrjeno nemoteno delovanje na javni domeni z delujočimi varnostnimi kopijami

**Kaj mi ni uspelo in zakaj:**
- vse je delovalo brez težav.

## 2026-10-22

**Kaj sem delal:**
- končni pregled stanja repozitorija in uskladitev vseh vej (`develop`, `mitja`, `nal`, `main`)
- izdelava Git oznake končne različice (tag `v1.0`)
- priprava skupnega zaključnega poročila v `porocila/zakljucno-porocilo.md` ter posodobitev `README.md`
- uskladitev zaključnih točk za oddajo projekta mentorju Maticu Holobarju

**Kaj sem dokončal:**
- projekt je uspešno zaključen, repozitorij označen z različico `v1.0` in pripravljen na zagovor

**Kaj mi ni uspelo in zakaj:**
- vse zahteve iz učnega načrta in projektne naloge so v celoti izpolnjene.
