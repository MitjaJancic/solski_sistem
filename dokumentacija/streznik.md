# Dokumentacija namestitve in konfiguracije strežnika

> Dokument se dopolnjuje skozi projekt (začet v 3. tednu). Trenutno pokriva
> lokalno/razvojno okolje; produkcijska postavitev (javna domena, Let's
> Encrypt) se doda v 4. tednu.

## 1. Arhitektura

```
                 ┌──────────────┐
  uporabnik ───► │  proxy       │  nginx:alpine, vrata 80/443
                 │  (nginx)     │  – preusmeritev 80→443
                 └──────┬───────┘  – TLS (samopodpisano potrdilo v razvoju)
                        │ proxy_pass :8000
                 ┌──────▼───────┐
                 │  aplikacija  │  Django (Python 3.12), vrata 8000 (interno)
                 └──────┬───────┘
                        │ TCP 3306
                 ┌──────▼───────┐
                 │  baza        │  MariaDB 11, poimenovan volumen baza_podatki
                 └──────────────┘
                 ┌──────────────┐
                 │  adminer     │  spletna administracija baze, vrata 8081
                 └──────────────┘
```

Vsi vsebniki tečejo v skupnem Docker omrežju, ki ga samodejno ustvari
`docker compose`; med seboj komunicirajo po imenih storitev (`baza`,
`aplikacija`, `proxy`).

## 2. Namestitev razvojnega okolja

Predpogoj: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
(vključuje Docker Compose).

```bash
cp .env.example .env          # uredi gesla po želji
sh scripts/generiraj-certifikat.sh   # ustvari samopodpisano TLS potrdilo
docker compose up -d --build
docker compose exec aplikacija python manage.py seed_podatki   # testni podatki
```

- aplikacija (prek posrednika, HTTPS): https://localhost — brskalnik bo
  opozoril na samopodpisano potrdilo, kar je v razvojni fazi pričakovano
- Adminer (administracija baze): http://localhost:8081 — sistem: MySQL,
  strežnik: `baza`, uporabnik/geslo iz `.env`

## 3. Obrnjeni posrednik (reverse proxy)

Konfiguracija: [`nginx/nginx.conf`](../nginx/nginx.conf).

- vrata 80 preusmerijo vse zahteve na 443 (`return 301 https://...`)
- vrata 443 streže TLS in posreduje zahteve na `aplikacija:8000`
- aplikacijski vsebnik ni javno dostopen neposredno (v `docker-compose.yml`
  ima le `expose`, ne `ports`) — ves promet gre skozi posrednika

## 4. HTTPS potrdilo

- **razvoj:** samopodpisano potrdilo, ustvarjeno s
  `scripts/generiraj-certifikat.sh` (openssl, veljavnost 365 dni, ni v Gitu)
- **produkcija (4. teden):** Let's Encrypt prek Certbota na javni domeni;
  `ssl_certificate`/`ssl_certificate_key` v `nginx.conf` se zamenjata s
  potema do pravega potrdila

## 5. Varnostne kopije baze

Načrtovano za 4. teden: `scripts/varnostna-kopija.sh` bo redno izvajal
`mariadb-dump` v vsebniku `baza` in izhod shranjeval izven vsebnika.

## 6. Spremenljivke okolja

Glej [`.env.example`](../.env.example) za popoln seznam. Datoteka `.env`
ni v repozitoriju (`.gitignore`) — vsak član skupine si jo ustvari lokalno.
