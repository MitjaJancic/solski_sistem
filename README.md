# Šolski IS+

Spletna aplikacija za podporo šolskemu delu na daljavo — zaključni projekt.

## Skupina
- **Mitja Jančič** ([@MitjaJancic](https://github.com/MitjaJancic)) — vzdrževalec informacijskega sistema (IS) + razvijalec aplikacije
- **Nal Dobravc** ([@naldobravc](https://github.com/naldobravc)) — razvijalec aplikacije
- **Matic Holobar** — mentor (učitelj)

## Tehnologije
- **Backend:** Python + Django 5.1
- **Baza:** MariaDB 11 (relacijska baza v lastnem Docker vsebniku)
- **Frontend:** Django predloge + Bootstrap 5 + Bootstrap Icons (popolna podpora za svetli in temni način)
- **Vsebniki:** Docker + Docker Compose (5 povezanih servisov)
- **Reverse proxy + HTTPS:** Nginx z varnostnimi glavami
- **Javna domena:** Cloudflare Tunnel (HTTPS z veljavnim digitalnim potrdilom)
- **Nadzor različic:** Git + GitHub (veje `main`, `develop`, `mitja`, `nal`, Pull Requesti in Issues)

Utemeljitev izbire tehnologij: [dokumentacija/specifikacija.md](dokumentacija/specifikacija.md).

## Struktura repozitorija
```
solski_sistem/
├── aplikacija/            Django projekt
│   ├── administracija/    administratorski CRUD (predmeti/učitelji/učenci)
│   ├── portal/            prijava, avtorizacija, pogleda učitelja in učenca, gradiva/oddaje, ocene, obvestila
│   ├── solski_sistem/     nastavitve (varnost, PBKDF2, seje), urls, wsgi
│   ├── static/            sodobni slogi (slog.css) s podporo za svetlo in temno temo
│   ├── templates/         skupna osnovna predloga (base.html) z Bootstrap Icons
│   ├── Dockerfile
│   └── requirements.txt
├── nginx/                 obrnjeni posrednik (nginx.conf) + certs/ (TLS certifikati)
├── scripts/               pomožne skripte (varnostna kopija baze, obnovitev, generiranje certifikata, tunel)
├── dokumentacija/         specifikacija, ER diagram, arhitektura, uporabniška navodila, poročilo z 29 posnetki
├── porocila/              dnevna in tedenska poročila po 6 tednih + zaključno poročilo
├── predstavitev/          prosojnice (predstavitev.md) in natančen scenarij demonstracije v živo (demo-scenarij.md)
├── docker-compose.yml
├── .env.example
└── README.md
```

## Kako pognati lokalno

Predpogoj: [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
# 1. Kloniranje repozitorija in priprava okolja
git clone https://github.com/MitjaJancic/solski_sistem.git
cd solski_sistem
cp .env.example .env

# 2. Zagon vseh 5 vsebnikov
docker compose up -d --build

# 3. Vnos šolskega kataloga in demo računov (če baza še ni inicializirana)
docker compose exec aplikacija python manage.py seed_podatki
docker compose exec aplikacija python manage.py seed_uporabniki
```

- **Lokalna aplikacija (stalni dostop):** [http://localhost/](http://localhost/) ali [https://localhost/](https://localhost/)
- **Administracija podatkovne baze (Adminer):** [http://localhost:8081/](http://localhost:8081/)
- **Javni HTTPS dostop (Cloudflare Tunnel):** zaženite `powershell scripts\pokazi-javni-url.ps1`

### Pripravljeni demo računi (za zagovor in testiranje)

Vsi uporabniški računi so poenoteni v formatu **`I.Priimek`** ter podpirajo prijavo neobčutljivo na velike/male črke in šumnike. Gesla so varno zgoščena z algoritmom **PBKDF2-SHA256**.

| Vloga | Uporabniško ime | Geslo | Opis in posebnosti |
|---|---|---|---|
| **Administrator** | `admin` | `Admin123!` | Celoten nadzor nad bazo podatkov, predmeti, učitelji in učenci |
| **Učitelj / Mentor** | `M.Holobar` | `Ucitelj123!` | Učitelj informatike in matematike (gradiva, naloge, ocenjevanje) |
| **Učiteljica** | `M.Horvat` | `Ucitelj123!` | Učiteljica slovenščine |
| **Učenec 1** | `M.Jancic` | `Ucenec123!` | Učenec razreda 4.A (oddaja nalog, gradiva, ocene z opombami) |
| **Učenec 2** | `N.Dobravc` | `Ucenec123!` | Učenec razreda 4.A (oddaja nalog z zamudo, prejeta obvestila) |

*Opomba: novi učenci se lahko sami registrirajo na povezavi `/registracija/`.*

### Zagon avtomatiziranih testov

Vseh 26 avtomatiziranih testov pokriva vse funkcionalnosti, avtorizacijske pravice in varnostne mehanizme:

```bash
# Zagon v Docker vsebniku:
docker compose exec aplikacija python manage.py test

# Ali lokalno z začasno SQLite bazo:
cd aplikacija
DJANGO_TEST_SQLITE=1 python manage.py test
```

## Časovni načrt (6 tednov) — Zaključeno (v2.0)

Projekt v celoti izpolnjuje in presega vse zahteve iz 3. in 4. poglavja navodil:
1. **Administrator:** CRUD nad 10 predmeti, 20 učitelji in 120 učenci v 3 razredih (4.A, 4.B, 4.C) ter M:N relacijami z iskanjem.
2. **Učitelj:** nalaganje in brisanje gradiv le za lastne predmete, ustvarjanje nalog z roki, pregled oddaj in ocenjevanje (1–5).
3. **Učenec:** samoregistracija, urejanje profila, izbira predmetov, vpogled v gradiva, oddaja nalog s formatom »Priimek Ime – Naslov naloge« ter obvezno potrditvijo pred prepisom datoteke.
4. **Varnost:** zaščiten prenos `/prenos/...`, zaščita pred SQLi, CSRF, XSS, zgoščena gesla, redne varnostne kopije.
5. **Uporabniški vmesnik:** Bootstrap 5, vektorske ikone Bootstrap Icons, preklop med svetlim in temnim načinom.

### Ključna dokumentacija:
- [dokumentacija/porocilo-o-implementaciji-s-posnetki.md](dokumentacija/porocilo-o-implementaciji-s-posnetki.md) — celovito poročilo z navodili za 29 zaslonskih posnetkov
- [predstavitev/predstavitev.md](predstavitev/predstavitev.md) — prosojnice za predstavitev + [demo-scenarij](predstavitev/demo-scenarij.md)
- [dokumentacija/testni-primeri.md](dokumentacija/testni-primeri.md) — matrika 26 testnih primerov in statusov
- [dokumentacija/arhitektura.md](dokumentacija/arhitektura.md) — arhitektura sistema z diagrami
- [dokumentacija/uporabniska-navodila.md](dokumentacija/uporabniska-navodila.md) — uporabniška navodila za vse tri vloge
- [dokumentacija/streznik.md](dokumentacija/streznik.md) — namestitev, konfiguracija, HTTPS in varnostne kopije

**Repozitorij projekta:** https://github.com/MitjaJancic/solski_sistem  
**Aktivna javna domena (Cloudflare HTTPS):** https://situations-generating-taken-rouge.trycloudflare.com
