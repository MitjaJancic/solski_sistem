# Dokumentacija namestitve in konfiguracije strežnika

> Dokument se dopolnjuje skozi projekt (začet v 3. tednu, razširjen v 4.).
> Pokriva lokalno/razvojno okolje ter napotke za produkcijsko postavitev
> (javna domena, Let's Encrypt, varnostne kopije, zaščita naloženih datotek).

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

## 4. Javna domena in HTTPS potrdilo

- **razvoj:** samopodpisano potrdilo, ustvarjeno s
  `scripts/generiraj-certifikat.sh` (openssl, veljavnost 365 dni, ni v Gitu)
- **produkcija (javna domena):** aplikacija se postavi na strežnik z operacijskim
  sistemom Linux, kamor kaže javna domena (npr. `sola-is.primer.si`). Koraki:
  1. v `.env` nastavi `DOMENA=sola-is.primer.si` in
     `DJANGO_ALLOWED_HOSTS=sola-is.primer.si` (Django iz tega samodejno določi
     tudi `CSRF_TRUSTED_ORIGINS`), `DJANGO_DEBUG=0`;
  2. v `nginx/nginx.conf` nastavi `server_name` na domeno;
  3. pridobi potrdilo Let's Encrypt s Certbotom, npr.
     `certbot certonly --webroot -w /var/www/certbot -d sola-is.primer.si`, ter
     `ssl_certificate`/`ssl_certificate_key` v `nginx.conf` usmeri na
     `/etc/letsencrypt/live/<domena>/fullchain.pem` oz. `privkey.pem`
     (mapo priklopi v vsebnik `proxy`);
  4. samodejno podaljševanje: `certbot renew` (cron/systemd timer) +
     ponovni zagon vsebnika `proxy`.

## 5. Zaščita naloženih datotek (gradiva in oddaje)

Naložene datoteke se hranijo v `MEDIA_ROOT` (`aplikacija/media/`, ni v Gitu) in
**niso javno dostopne**:

- Nginx nima lokacije za `media/`, zato datotek ne streže neposredno; ves promet
  gre v Django.
- Django datotek ne izpostavlja na `MEDIA_URL`; dostop je mogoč le prek
  prijavljenih poti s preverjanjem pravic:
  [`/prenos/gradivo/<id>/`](../aplikacija/portal/urls.py) in
  `/prenos/oddaja/<id>/` (funkciji `gradivo_prenos`, `oddaja_prenos`). Gradivo
  lahko prenese administrator, učitelj predmeta ali vpisani učenec; oddajo pa
  administrator, učitelj predmeta ali učenec, ki je oddajo oddal.
- Oddaje se shranijo pod imenom »Priimek Ime – Naslov naloge« z izvorno
  končnico; ponovna oddaja iste naloge povozi datoteko šele po potrditvi
  učenca (posebno shranjevanje `PovoznoShranjevanje`).

## 6. Varnostne kopije baze

Skripta [`scripts/varnostna-kopija.sh`](../scripts/varnostna-kopija.sh) izvede
`mariadb-dump` v vsebniku `baza`, izhod stisne in shrani v mapo `backup/` izven
vsebnika ter obdrži zadnjih 7 kopij. Ročni zagon:

```bash
sh scripts/varnostna-kopija.sh
```

Za redno izvajanje (npr. vsak dan ob 2:30) se doda vnos v cron na strežniku:

```
30 2 * * * cd /pot/do/projekta && sh scripts/varnostna-kopija.sh >> backup/backup.log 2>&1
```

## 7. Spremenljivke okolja

Glej [`.env.example`](../.env.example) za popoln seznam. Datoteka `.env`
ni v repozitoriju (`.gitignore`) — vsak član skupine si jo ustvari lokalno.
