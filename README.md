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

Podrobnosti: [dokumentacija/streznik.md](dokumentacija/streznik.md).

## Časovni načrt (6 tednov)
Izvorna navodila: glejte `navodila.txt` in `5. Časovni načrt dela – 6 tednov.txt`
v mapi projekta. Tedenska poročila o napredku: [porocila/](porocila/).

**Trenutno stanje: teden 5 od 6** — vse funkcionalnosti iz 3. in 4. tedna
(administratorski CRUD; prijava/avtorizacija; pogleda učitelja in učenca;
zaščitene naložene datoteke; varnostne kopije baze). V 5. tednu dodano:
sistematično testiranje vseh treh pogledov (26 avtomatiziranih testov, vsi
uspešni), odprava odkritih napak, izboljšave odzivnega oblikovanja ter
dokončana dokumentacija in uporabniška navodila.

Ključni dokumenti:
- [dokumentacija/testni-primeri.md](dokumentacija/testni-primeri.md) — seznam testnih primerov in status
- [dokumentacija/arhitektura.md](dokumentacija/arhitektura.md) — arhitektura z diagramom
- [dokumentacija/uporabniska-navodila.md](dokumentacija/uporabniska-navodila.md) — navodila za vse tri vloge
- [dokumentacija/streznik.md](dokumentacija/streznik.md) — namestitev, javna domena, varnostne kopije
