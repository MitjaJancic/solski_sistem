# Šolski IS

Spletna aplikacija za podporo šolskemu delu na daljavo — zaključni projekt.

## Skupina
- **Mitja Jančič** ([@MitjaJancic](https://github.com/MitjaJancic)) — vzdrževalec informacijskega sistema (IS) + razvijalec aplikacije
- **Nal Dobravc** ([@naldobravc](https://github.com/naldobravc)) — razvijalec aplikacije
- **mentor** — bo dodan kasneje

## Tehnologije
- **Backend:** Python + Django 5.1
- **Baza:** MariaDB 11
- **Frontend:** Django predloge + Bootstrap 5
- **Vsebniki:** Docker + Docker Compose
- **Reverse proxy + HTTPS:** Nginx (samopodpisano potrdilo v razvoju → Let's Encrypt na javni domeni)
- **Nadzor različic:** Git + GitHub

Utemeljitev izbire tehnologij: [dokumentacija/specifikacija.md](dokumentacija/specifikacija.md).

## Struktura repozitorija
```
solski_sistem/
├── aplikacija/            Django projekt
│   ├── administracija/    administratorski CRUD (predmeti/učitelji/učenci)
│   ├── portal/            prijava, avtorizacija, pogleda učitelja in učenca, gradiva/oddaje
│   ├── solski_sistem/     nastavitve, urls, wsgi
│   ├── static/            css
│   ├── templates/         skupna osnovna predloga (base.html)
│   ├── Dockerfile
│   └── requirements.txt
├── nginx/                 obrnjeni posrednik (nginx.conf) + certs/ (samopodpisano potrdilo, negitano)
├── scripts/                pomožne skripte (generiranje TLS potrdila ...)
├── dokumentacija/          specifikacija, ER diagram, wireframi, dokumentacija strežnika
├── porocila/                dnevna in tedenska poročila
├── docker-compose.yml
├── .env.example
└── README.md
```

## Kako pognati lokalno

Predpogoj: [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
cp .env.example .env
sh scripts/generiraj-certifikat.sh
docker compose up -d --build
docker compose exec aplikacija python manage.py seed_podatki
docker compose exec aplikacija python manage.py seed_uporabniki   # demo računi (4. teden)
```

- aplikacija: https://localhost (samopodpisano potrdilo — brskalnik bo opozoril, kar je v razvoju pričakovano)
- administracija baze (Adminer): http://localhost:8081

### Demo računi (za predstavitev/testiranje)

Ustvari jih `seed_uporabniki`. Gesla so shranjena zgoščeno (PBKDF2).

| Vloga | Uporabnik | Geslo |
|---|---|---|
| administrator | `admin` | `Admin123!` |
| učitelj | `ucitelj1`–`ucitelj3` | `Ucitelj123!` |
| učenec | `ucenec1`–`ucenec3` | `Ucenec123!` |

Novi učenci se lahko tudi sami registrirajo na `/registracija/`.

### Zagon testov (brez Dockerja)

```bash
cd aplikacija
DJANGO_TEST_SQLITE=1 python manage.py test
```

### Produkcija (javna domena)

V produkciji se uporablja samo osnovna sestava (gunicorn + WhiteNoise, brez
Adminerja in priklopa kode). V `.env` nastavi `DJANGO_DEBUG=0` in
`DJANGO_ALLOWED_HOSTS` na javno domeno, nato:

```bash
docker compose -f docker-compose.yml up -d --build
```

Podrobnosti (domena, Let's Encrypt, varnostne kopije, zaključni pregled):
[dokumentacija/streznik.md](dokumentacija/streznik.md).

Podrobnosti: [dokumentacija/streznik.md](dokumentacija/streznik.md).

## Časovni načrt (6 tednov)
Izvorna navodila: glejte `navodila.txt` in `5. Časovni načrt dela – 6 tednov.txt`
v mapi projekta. Tedenska poročila o napredku: [porocila/](porocila/).

**Stanje: teden 6 od 6 — zaključeno (`v1.0`).** Projekt izpolnjuje zahteve iz
3. in 4. poglavja navodil: administratorski CRUD; prijava in avtorizacija po
vlogah; pogleda učitelja in učenca; zaščitene naložene datoteke; varnostne
kopije baze; 26 avtomatiziranih testov (vsi uspešni); dokončana dokumentacija
in uporabniška navodila. V 6. tednu dodana produkcijska sestava (gunicorn +
WhiteNoise, varnostne nastavitve), predstavitev in zaključno poročilo.

Ključni dokumenti:
- [porocila/zakljucno-porocilo.md](porocila/zakljucno-porocilo.md) — zaključno poročilo skupine
- [predstavitev/predstavitev.md](predstavitev/predstavitev.md) — diapozitivi + [demo-scenarij](predstavitev/demo-scenarij.md)
- [dokumentacija/testni-primeri.md](dokumentacija/testni-primeri.md) — seznam testnih primerov in status
- [dokumentacija/arhitektura.md](dokumentacija/arhitektura.md) — arhitektura z diagramom
- [dokumentacija/uporabniska-navodila.md](dokumentacija/uporabniska-navodila.md) — navodila za vse tri vloge
- [dokumentacija/streznik.md](dokumentacija/streznik.md) — namestitev, javna domena, varnostne kopije

**Delujoča aplikacija (javna domena):** _<vstavi URL>_
