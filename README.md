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
- **Reverse proxy + HTTPS:** Nginx (samopodpisano potrdilo v razvoju → Let's Encrypt v 4. tednu)
- **Nadzor različic:** Git + GitHub

Utemeljitev izbire tehnologij: [dokumentacija/specifikacija.md](dokumentacija/specifikacija.md).

## Struktura repozitorija
```
solski_sistem/
├── aplikacija/            Django projekt
│   ├── administracija/    modeli, obrazci, CRUD poglede, predloge (predmeti/učitelji/učenci)
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
```

- aplikacija: https://localhost (samopodpisano potrdilo — brskalnik bo opozoril, kar je v razvoju pričakovano)
- administracija baze (Adminer): http://localhost:8081

Podrobnosti: [dokumentacija/streznik.md](dokumentacija/streznik.md).

## Časovni načrt (6 tednov)
Izvorna navodila: glejte `navodila.txt` in `5. Časovni načrt dela – 6 tednov.txt`
v mapi projekta. Tedenska poročila o napredku: [porocila/](porocila/).

**Trenutno stanje: teden 3 od 6** — administratorski CRUD (predmeti, učitelji,
učenci + relacije) je implementiran; prijava, avtorizacija ter pogleda
učitelja/učenca sledijo v 4. tednu.
