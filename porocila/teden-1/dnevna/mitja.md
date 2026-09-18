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

**Kaj sem dokončal:** ogrodje projekta, specifikacija, ER diagram, wireframi, CRUD administratorja, docker-compose in nginx konfiguracija (še nepreizkušena v resničnem Dockerju).

**Kaj mi ni uspelo in zakaj:**
- nisem mogel dejansko pognati `docker compose up`, ker Docker Desktop ni nameščen na tem računalniku — potrebna je namestitev, preden preverimo delovanje v resničnih vsebnikih
- GitHub repozitorij še ni ustvarjen/povezan (čakam na mentorja, ki bo dodan kot sodelavec)
