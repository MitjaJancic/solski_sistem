# Tedensko poročilo – teden 1 (Analiza, načrtovanje in priprava okolja)

**Povzetek napredka:** repozitorij in mapna struktura sta pripravljena;
izbran je tehnološki sklad (Django + MariaDB + Docker + Nginx) z utemeljitvijo
v [specifikaciji](../../dokumentacija/specifikacija.md); pripravljen je ER
diagram s 5 tabelami in žični modeli (wireframe) za vse tri poglede
(administrator, učitelj, učenec). Razvojno okolje z Dockerjem je konfigurirano,
a še ni bilo dejansko zagnano, ker Docker Desktop na razvojnem računalniku še
ni nameščen.

**Sklepi:** ker gre trenutno za ekipo dveh dijakov (Mitja – vzdrževalec IS in
razvijalec, Nal – razvijalec), je Mitja pripravil začetno ogrodje projekta v
enem srečanju; mentor bo dodan kot sodelavec repozitorija, ko bo določen.

**Načrt za naslednji teden:** namestitev Docker Desktop, dejanski zagon
`docker compose up`, preverjanje povezave aplikacije z bazo, vnos testnih
podatkov (`seed_podatki`) v resnično MariaDB bazo.
