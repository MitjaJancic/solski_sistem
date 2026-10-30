# Dnevna poročila – Mitja Jančič (vzdrževalec IS + razvijalec)

## 2026-09-15

**Kaj sem delal:**
- uvodni usklajevalni sestanek z Nalom in pregled dodeljenih vlog (vzdrževalec IS / razvijalec)
- vzpostavitev Git repozitorija na GitHubu (`MitjaJancic/solski_sistem`) in priprava osnovne strukture map (`aplikacija/`, `dokumentacija/`, `porocila/`, `nginx/`, `scripts/`)
- zasnova začetne konfiguracije `docker-compose.yml` (storitve za MariaDB 11, Django aplikacijo in spletni strežnik Nginx)
- priprava predloge za okoljske spremenljivke `.env.example`

**Kaj sem dokončal:**
- GitHub repozitorij, mapa projekta z osnovnimi datotekami in `.env.example`

**Kaj mi ni uspelo in zakaj:**
- zagon vsebnikov z Dockerjem še ni bil mogoč, ker Docker Desktop na računalniku še ni bil posodobljen in nameščen.

## 2026-09-17

**Kaj sem delal:**
- priprava Nginx konfiguracijske datoteke (`nginx/nginx.conf`) kot obrnjenega posrednika (reverse proxy) pred Django vsebnikom
- izdelava pomožne skripte za generiranje samopodpisanega certifikata za razvojno okolje (`scripts/generiraj-certifikat.sh`)
- začetek pisanja strežniške dokumentacije (`dokumentacija/streznik.md`) z opisom zahtevanih komponent in namestitve

**Kaj sem dokončal:**
- Nginx konfiguracija za posredovanje zahtevkov in skripta za generiranje TLS certifikata; ogrodje dokumentacije strežnika

**Kaj mi ni uspelo in zakaj:**
- dodajanje mentorja Matica Holobarja na GitHubu je bilo začasno zadržano, dokler nismo pridobili točnega uporabniškega imena.

## 2026-09-18

**Kaj sem delal:**
- pregled Nalove specifikacije zahtev in predloga ER diagrama s stališča infrastrukture in tipov podatkov v MariaDB
- uskladitev podatkovnega modela (uporaba ustreznih tujih ključev in unikatnih indeksov)
- priprava in oddaja zbirnega tedenskega poročila za 1. teden

**Kaj sem dokončal:**
- potrjena specifikacija in ER načrt, usklajen časovni načrt za 2. teden

**Kaj mi ni uspelo in zakaj:**
- vse načrtovane naloge za 1. teden so bile uspešno izvedene.
