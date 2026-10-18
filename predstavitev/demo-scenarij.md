# Scenarij praktične demonstracije

Korak za korakom za živo predstavitev (≈5 minut). Predpogoj: okolje teče in so
vneseni testni podatki ter demo računi.

```bash
docker compose up -d --build
docker compose exec aplikacija python manage.py seed_podatki
docker compose exec aplikacija python manage.py seed_uporabniki
```

Demo računi: `admin/Admin123!`, `ucitelj1/Ucitelj123!`, `ucenec1/Ucenec123!`
(na javni domeni uporabi enakovredne račune).

## 1. Administrator (≈1 min)
1. Prijava kot `admin`.
2. *Predmeti* → *+ Nov predmet* → npr. `TJ2 / Tuji jezik 2` → **Shrani**.
3. *Učitelji* → pokaži učitelja z več predmeti (značke).
4. *Učenci* → odpri učenca, pokaži seznam predmetov (M:N).
5. Odjava.

## 2. Učitelj (≈1 min)
1. Prijava kot `ucitelj1`.
2. *Moji predmeti* → **odpri** enega od svojih predmetov.
3. *Naloži gradivo* → izberi predmet (na voljo so **samo** njegovi), naslov +
   datoteka → **Naloži**.
4. Pokaži, da se gradivo pojavi v seznamu; pokaži tudi tabelo *Oddane naloge*.
5. Odjava.

## 3. Učenec (≈2 min)
1. *Registracija* novega učenca (ali prijava kot `ucenec1`).
2. *Moji predmeti* → označi predmete → **Shrani**.
3. Odpri *Gradiva* pri predmetu, kjer je učitelj naložil gradivo → **Prenesi**.
4. *Oddaj nalogo* → izberi predmet, vpiši naslov `1. domača`, izberi datoteko →
   **Oddaj**.
   - pokaži *Moje oddaje*: ime datoteke je **»Priimek Ime – 1. domača.ext«**.
5. Ponovna *Oddaj nalogo* z istim naslovom → sistem **zahteva potrditev**
   povozitve; označi potrditev → nova datoteka povozi prejšnjo.

## 4. Avtorizacija (≈30 s)
1. Kot učenec poskusi odpreti administratorski URL (`/predmeti/`) → **403**.
2. (Po želji) pokaži, da neposreden dostop do `/media/...` ne vrne datoteke.

## 5. Zaključek
- pokaži rezultat testov (`python manage.py test` → 26 OK),
- omeni tag `v1.0` in povezavo do repozitorija ter javne domene.
