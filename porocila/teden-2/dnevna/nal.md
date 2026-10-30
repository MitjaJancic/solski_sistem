# Dnevna poročila – Nal Dobravc (razvijalec aplikacije)

## 2026-09-22

**Kaj sem delal:**
- postavitev Django projekta `solski_sistem` in Django aplikacije `administracija`
- definicija podatkovnih modelov v `aplikacija/administracija/models.py`:
  - `Predmet` (sifra, naziv, opis)
  - `Ucitelj` (ime, priimek, email, kabinet)
  - `Ucenec` (ime, priimek, vpisna_stevilka, email, razred)
  - `UciteljPredmet` in `UcenecPredmet` za realizacijo relacij M:N z ustreznimi omejitvami
- generiranje začetnih migracij z ukazom `makemigrations`

**Kaj sem dokončal:**
- modelna plast aplikacije z ustreznimi polji, primarnimi ključi in tujimi ključi

**Kaj mi ni uspelo in zakaj:**
- pri nastavljanju `related_name` relacij je prišlo do manjšega prekrivanja imen, kar sem popravil z jasnejšimi imeni povezav.

## 2026-09-24

**Kaj sem delal:**
- izdelava Django ukaza za avtomatski vnos testnih podatkov (`aplikacija/administracija/management/commands/seed_podatki.py`)
- priprava realističnih testnih podatkov po zahtevah:
  - 10 šolskih predmetov
  - 20 učiteljev (pri čemer določeni učitelji poučujejo več predmetov in nekateri predmeti imajo več učiteljev)
  - 100 učencev (pri čemer vsak učenec obiskuje več kot en predmet)
- lokalni preizkus polnjenja baze na začasni SQLite bazi

**Kaj sem dokončal:**
- delujoča skripta `seed_podatki`, ki z enim ukazom napolni bazo z vsemi predpisanimi relacijami

**Kaj mi ni uspelo in zakaj:**
- generiranje 100 verodostojnih slovenskih imen in unikatnih e-poštnih naslovov je zahtevalo nekoliko več ročnega oblikovanja seznamov.

## 2026-09-25

**Kaj sem delal:**
- zagon ukaza `python manage.py seed_podatki` v pravem MariaDB vsebniku v Dockerju skupaj z Mitjem
- pregled tabel in povezav prek spletnega orodja Adminer (preverjanje tabel `administracija_predmet`, `administracija_ucitelj`, `administracija_ucenec`, `administracija_uciteljpredmet`, `administracija_ucenecpredmet`)
- preverjanje normaliziranosti in celovitosti podatkov

**Kaj sem dokončal:**
- baza vsebuje točno 10 predmetov, 20 učiteljev in 100 učencev z veljavnimi povezavami in brez sirot med tujimi ključi

**Kaj mi ni uspelo in zakaj:**
- vse je teklo gladko in v skladu s časovnim načrtom.
