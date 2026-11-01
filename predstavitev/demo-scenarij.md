# Scenarij praktične demonstracije za zagovor

Natančen potek korak za korakom za živo predstavitev pred mentorjem (≈8 do 10 minut).

## Predpogoj pred začetkom predstavitve
Preverite, da vsi Docker vsebniki tečejo in da je tunel aktiven:
```bash
docker compose ps
powershell scripts\pokazi-javni-url.ps1
```
Pripravite dva odprta zavihka v brskalniku:
1. `http://localhost/` (ali javna domena)
2. `https://github.com/MitjaJancic/solski_sistem`

---

## 1. Uvod in arhitektura (≈1 minuta)
- Predstavite ekipo: **Mitja Jančič** (vzdrževalec IS in razvijalec) in **Nal Dobravc** (razvijalec).
- Omenite tehnološki sklad: **Django 5.1**, **MariaDB 11**, **Nginx reverse proxy** s HTTPS ter **Cloudflare Tunnel** za javno domeno.
- V terminalu pokažite izpis `docker compose ps` (5 ločenih vsebnikov) in zagon testov:
  ```bash
  docker compose exec aplikacija python manage.py test
  ```
  *(poudarite: vseh 26 avtomatiziranih testov se uspešno zaključi v nekaj sekundah)*.

---

## 2. Administrator — `admin` / `Admin123!` (≈2 minuti)
1. **Prijava** kot `admin` na `/prijava/`.
2. **Nadzorna plošča:** pokažite števce statistike (10 predmetov, 20 učiteljev, 120 učencev, aktivne naloge in oddaje).
3. **Predmeti:**
   - Odprite meni *Predmeti*.
   - Kliknite *+ Nov predmet* → vnesite npr. šifro `ROB` in ime `Robotika` ter shranite.
4. **Učitelji & M:N relacija:**
   - Odprite meni *Učitelji*.
   - Pokažite učitelja **Matic Holobar** (`M.Holobar`), ki poučuje *Informatiko* in *Matematiko*.
   - Pokažite predmet *Informatika*, ki ga poučuje več učiteljev (M:N relacija).
5. **Učenci in razredi:**
   - Odprite meni *Učenci*.
   - Pokažite razdelitev učencev v razrede **4.A**, **4.B** in **4.C**.
   - V iskalno polje zgoraj vnesite `Jančič` ali `Dobravc` → pokažite hitro dinamično iskanje in gumb za čiščenje.
6. **Odjava.**

---

## 3. Učitelj — `M.Holobar` / `Ucitelj123!` (≈2 minuti)
1. **Prijava** z mentorjevim računom `M.Holobar`.
2. **Učiteljski pregled:**
   - Pokažite KPI kartice (dodeljeni predmeti, aktivne naloge, oddaje, ki čakajo na oceno).
   - Poudarite, da učitelj vidi **samo predmete, ki jih poučuje** (Informatika, Matematika).
3. **Učna gradiva:**
   - Kliknite *Naloži gradivo* ali pojdite v učilnico predmeta *Informatika*.
   - Pokažite seznam naloženih PDF gradiv z varnim prenosom.
4. **Naloge in ocenjevanje:**
   - Kliknite na nalogo *»Načrtovanje podatkovne baze«*.
   - Pokažite tabelo oddanih nalog učencev.
   - Kliknite gumb **Oceni** ob oddaji učenca, vnesite oceno (npr. `5`) in spodbuden komentar: *»Izjemno natančen ER diagram, odlično delo.«*
5. **Odjava.**

---

## 4. Učenec — `M.Jancic` / `Ucenec123!` (≈3 minute)
1. **Pristajalna stran in prijava:**
   - Pokažite gumb za **preklop med svetlim in temnim načinom** (Dark/Light mode).
   - Prijavite se kot učenec `M.Jancic`.
2. **Učenčev pregled:**
   - Pokažite vpisane predmete, povprečno oceno in center za obvestila (rdeča značka z obvestilom, da je mentor pravkar ocenil nalogo!).
3. **Moji predmeti:**
   - Kliknite *Moji predmeti* → pokažite interaktivno izbiro predmetov (sistem zahteva vsaj 1 predmet).
4. **Oddaja naloge in poimenovanje:**
   - Kliknite na odprto nalogo pri Informatiki.
   - Izberite datoteko (npr. PDF dokument) in kliknite **Oddaj**.
   - **Ključni dokaz za mentorja:** Odprite *Moje oddaje* in pokažite ime shranjene datoteke:  
     `Jančič Mitja – Načrtovanje podatkovne baze.pdf` (točno po navodilih!).
5. **Potrditev prepisa (povozitve):**
   - Ponovno kliknite na isto nalogo za ponovno oddajo.
   - Pokažite opozorilo, da nova oddaja nadomesti staro šele, ko učenec to **izrecno potrdi**.

---

## 5. Varnostni mehanizmi in zaključek (≈1 minuta)
1. **Avtorizacija (preizkus vdora):**
   - Kot prijavljen učenec v naslovno vrstico ročno vpišite `/admin-portal/` → sistem nemudoma zavrne dostop s kodo **403 Forbidden**.
   - Poskusite neposreden prenos datoteke brez prijave → Nginx in Django zavrneta dostop (datoteke niso javne).
2. **Zaključek:**
   - Pokažite repozitorij na GitHubu z oznako izdaje **`v2.0`** ter Pull Requesti članov skupine.
   - Zahvalite se mentorju in povabite k vprašanjem.
