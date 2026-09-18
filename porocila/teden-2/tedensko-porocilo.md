# Tedensko poročilo – teden 2 (Postavitev infrastrukture in podatkovne baze)

**Povzetek napredka:** `docker-compose.yml` je dokončan s štirimi storitvami:

- `baza` – MariaDB 11, podatki v poimenovanem volumnu `baza_podatki`, ločena
  od aplikacije
- `aplikacija` – Django, vgrajen `entrypoint.sh` počaka na bazo in požene
  migracije pred zagonom strežnika
- `adminer` – spletna administracija baze (vrata 8081)
- `proxy` – Nginx (dodano nekoliko prej kot je predvideno, glej teden 3)

Django modeli (`Predmet`, `Ucitelj`, `Ucenec` + presečni tabeli
`UciteljPredmet`/`UcenecPredmet`) so migrirani; ukaz `seed_podatki` vnese 10
predmetov, 20 učiteljev in 100 učencev z ustreznimi relacijami (preverjeno:
vsaj en predmet ima več učiteljev, vsaj en učitelj poučuje več predmetov,
vsak učenec obiskuje več kot en predmet). Funkcionalnost je bila preizkušena
lokalno prek SQLite (brez Dockerja), saj Docker Desktop na razvojnem
računalniku še ni nameščen.

**Manjka za dokončanje zahtev tega tedna:** zaslonski posnetek dejansko
zagnanega `docker compose up` okolja — sledi takoj po namestitvi Docker
Desktop.

**Načrt za naslednji teden:** namestiti Docker Desktop, zagnati celotno
okolje z enim ukazom, preveriti povezavo znotraj Docker omrežja in nadaljevati
s CRUD funkcionalnostjo administratorja (glej teden 3).
