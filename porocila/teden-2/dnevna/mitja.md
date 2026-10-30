# Dnevna poročila – Mitja Jančič (vzdrževalec IS + razvijalec)

## 2026-09-22

**Kaj sem delal:**
- namestitev in nastavitev Docker Desktopa na razvojnem računalniku
- nadgradnja `docker-compose.yml` s štirimi ločenimi storitvami: `baza` (MariaDB 11 z obstojnim volumnom `baza_podatki`), `aplikacija` (Django), `adminer` (spletno orodje za upravljanje baze na vratih 8081) in `proxy` (Nginx reverzni posrednik)
- konfiguracija datoteke `.env` z varnostnimi spremenljivkami za MariaDB in Django

**Kaj sem dokončal:**
- celotna sestava `docker-compose.yml` pripravljena za večvsebniško izvajanje

**Kaj mi ni uspelo in zakaj:**
- ob prvem zagonu se je Django vsebnik poskusil povezati z bazo MariaDB, še preden je bila ta popolnoma inicializirana, kar je sprožilo povezovalno napako.

## 2026-09-24

**Kaj sem delal:**
- izdelava zagonske skripte `aplikacija/entrypoint.sh`, ki z zanko preverja dostopnost MariaDB prek porta 3306 in šele po uspešni povezavi izvede samodejne migracije ter zažene spletni strežnik
- vzpostavitev vej `develop`, `mitja` in `nal` na repozitoriju ter nastavitev osnovnih pravil za delo z vejami
- preizkus ponovnega zagona celotnega okolja z enim samim ukazom `docker compose up -d --build`

**Kaj sem dokončal:**
- avtomatiziran in robusten zagon vseh vsebnikov, vsi štirje servisi uspešno prešli v stanje "Up"

**Kaj mi ni uspelo in zakaj:**
- vse je delovalo brez zapletov.

## 2026-09-25

**Kaj sem delal:**
- preverjanje dostopnosti storitev: preizkus povezave do spletne administracije Adminer na `http://localhost:8081`
- skupni zagon Nalovega upravljalnega ukaza `seed_podatki` znotraj aplikacijskega vsebnika proti pravi MariaDB bazi podatkov
- zajem zaslonskega posnetka delovanja okolja v Docker Desktopu in Adminerju za tedensko poročilo

**Kaj sem dokončal:**
- uspešno potrjeno delovanje vseh 4 vsebnikov v skupnem Docker omrežju z uvoženimi testnimi podatki

**Kaj mi ni uspelo in zakaj:**
- vse predvidene naloge za 2. teden so bile uspešno zaključene.
