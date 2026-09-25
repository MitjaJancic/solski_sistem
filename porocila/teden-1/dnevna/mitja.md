# Dnevna poročila – Mitja Jančič (vzdrževalec IS + razvijalec)

## 2026-09-28

**Kaj sem delal:**
- pripravil strukturo repozitorija (`dokumentacija/`, `porocila/`, `aplikacija/`, `nginx/`, `scripts/`)
- izbral tehnološki sklad: Django 5.1 + MariaDB 11 + Docker Compose + Nginx (utemeljitev v [specifikaciji](../../dokumentacija/specifikacija.md))
- napisal `docker-compose.yml` (baza, aplikacija, adminer, proxy) in `.env.example`
- napisal specifikacijo sistema (vsi trije pogledi) in ER diagram (5 tabel: Predmet, Ucitelj, Ucenec, UciteljPredmet, UcenecPredmet)
- izdelal žične modele (wireframe) za administratorski, učiteljski in učenčev pogled
- postavil Django aplikacijo `administracija`: modeli, admin.py, obrazci, CRUD poglede in predloge za predmete/učitelje/učence
- napisal `seed_podatki` ukaz za testne podatke (10 predmetov, 20 učiteljev, 100 učencev) in ga lokalno preizkusil (SQLite, brez Dockerja, ker Docker Desktop na tem računalniku še ni nameščen)
- pripravil Nginx konfiguracijo kot obrnjeni posrednik + skripto za generiranje samopodpisanega TLS potrdila in ga generiral
- začel dokumentacijo strežnika ([`streznik.md`](../../dokumentacija/streznik.md))

**Kaj sem dokončal:** ogrodje projekta, specifikacija, ER diagram, wireframi, CRUD administratorja, docker-compose in nginx konfiguracija; ustvaril GitHub repozitorij ([MitjaJancic/solski_sistem](https://github.com/MitjaJancic/solski_sistem)), povezal veje `main`/`develop`/`mitja`/`nal` in povabil Nala kot sodelavca.

**Popoldanska posodobitev:** po namestitvi Docker Desktop sem dejansko pognal `docker compose up -d --build` — vsi štirje vsebniki (baza, aplikacija, adminer, proxy) so se zagnali in delujejo; `entrypoint.sh` je pravilno počakal na bazo in pognal migracije. Poganjal sem `seed_podatki` na resnični MariaDB bazi (10 predmetov, 20 učiteljev, 100 učencev) in preveril, da je aplikacija dosegljiva na https://localhost (skozi Nginx, samopodpisano potrdilo) ter Adminer na http://localhost:8081.

**Kaj mi ni uspelo in zakaj:**
- GitHub repozitorij je javen (public), mentor še ni dodan kot sodelavec, ker njegovo uporabniško ime še ni znano — dodam ga takoj, ko bo določen
