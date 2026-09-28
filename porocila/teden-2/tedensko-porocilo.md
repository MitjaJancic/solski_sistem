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
vsak učenec obiskuje več kot en predmet).

**Docker preverjen v praksi:** po namestitvi Docker Desktop je bilo okolje
dejansko zagnano z `docker compose up -d --build`. Vsi štirje vsebniki
(`baza`, `aplikacija`, `adminer`, `proxy`) tečejo; `docker compose ps` pokaže
status "Up" za vse. Migracije se ob zagonu izvedejo samodejno
(`entrypoint.sh` počaka, da je MariaDB dosegljiva). `seed_podatki` je bil
pognan proti resnični MariaDB bazi (ne več SQLite) z enakim rezultatom kot
prej. Aplikacija je dosegljiva na https://localhost, Adminer na
http://localhost:8081.

**Zaslonski posnetek:** aplikacija je bila odprta v privzetem brskalniku na
https://localhost — zaslonski posnetek doda kdorkoli od dijakov v to mapo
(`porocila/teden-2/`) pred oddajo poročila mentorju.

**Načrt za naslednji teden:** nadaljevati s CRUD funkcionalnostjo
administratorja in osnovami varnosti strežnika (glej teden 3, ki je bil prav
tako že scaffoldan vnaprej).
