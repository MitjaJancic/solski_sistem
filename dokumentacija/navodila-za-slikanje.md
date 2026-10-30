# Navodila za zajem zaslonskih posnetkov (Screenshots)

Ta dokument vsebuje natančen kontrolni seznam vseh zaslonskih posnetkov, ki jih potrebujete za oddajo tedenskih poročil, zaključnega poročila ter za diapozitive predstavitve pred mentorjem Maticem Holobarjem.

---

## Priporočila za kakovost posnetkov
- **Orodje za zajem:** Uporabite bližnjico `Win + Shift + S` (Orodje za izrezovanje v sistemu Windows) ali aplikacijo *Snipping Tool*.
- **Ločljivost:** Priporočljivo je zajeti celotno okno brskalnika skupaj z naslovno vrstico (da se vidi URL naslov in ključavnica HTTPS).
- **Format:** Slike shranite v obliki PNG v mapo poročil (npr. `porocila/teden-X/slika-opis.png`).

---

## 1. Infrastruktura in Docker okolje

### Posnetek 1.1: Docker Desktop – delujoči vsebniki
- **Kaj odpreti:** Aplikacijo **Docker Desktop** na namizju.
- **Kaj mora biti vidno:** Razdelek z vsebniško skupino `sola_sistem`.
- **Ključni elementi:** Vseh 5 vsebnikov mora imeti zeleno ikono in status **Running / Up**:
  - `sola_sistem-aplikacija-1` (vrata 8000)
  - `sola_sistem-baza-1` (vrata 3306)
  - `sola_sistem-proxy-1` (vrata 80, 443)
  - `sola_sistem-adminer-1` (vrata 8081)
  - `sola_sistem-tunel-1` (Cloudflare tunnel)
- **Alternativa v terminalu:** Ukaz `docker compose ps` v mapi projekta.

### Posnetek 1.2: Podatkovna baza v orodju Adminer
- **Kaj odpreti:** Povezavo `http://localhost:8081` v brskalniku.
- **Prijava:**
  - Sistem: `MySQL` (ali MariaDB)
  - Strežnik: `baza`
  - Uporabnik: `sola_user`
  - Geslo: `geslo_za_bazo`
  - Baza: `sola_is`
- **Kaj mora biti vidno:**
  - Seznam tabel v shemi: `administracija_predmet`, `administracija_ucitelj`, `administracija_ucenec`, `administracija_uciteljpredmet`, `administracija_ucenecpredmet`, `portal_naloga`, `portal_oddaja`, `portal_obvestilo`.
  - Klik na tabelo `administracija_predmet` ali `administracija_ucenec` → gumb *Izberi podatke* (da se vidi vnesenih 10 predmetov / 100 učencev).

---

## 2. Javna domena in HTTPS (Cloudflare Tunnel)

### Posnetek 2.1: Javni URL z varnostnim certifikatom
- **Kaj odpreti:** V brskalniku odprite javni naslov, ki ga izpiše skripta:
  `powershell .\scripts\pokazi-javni-url.ps1`
  (npr. `https://photos-sensitive-scheduled-enough.trycloudflare.com`).
- **Kaj mora biti vidno:**
  - Vstopna stran portala.
  - V naslovni vrstici brskalnika mora biti jasno vidna **ikona varnostne ključavnice** (veljavno HTTPS potrdilo).

### Posnetek 2.2: Mobilni pogled (Pametni telefon)
- **Kaj odpreti:** Zgoraj navedeni javni URL odprite na svojem pametnem telefonu (preko mobilnih podatkov ali Wi-Fi).
- **Kaj mora biti vidno:**
  - Mobilna prilagoditev strani (odzivno / responsive oblikovanje).
  - Skrčen navigacijski meni (hamburger gumb) in lepo poravnane tabele/kartice.

---

## 3. Pogled Administratorja (CRUD in relacije)

*Prijava z uporabniškim računom:* `admin` / `Admin123!`

### Posnetek 3.1: Seznam predmetov z iskanjem
- **Kaj odpreti:** Meni *Predmeti* (`/predmeti/`).
- **Kaj mora biti vidno:**
  - Tabela predmetov (šifra, naziv, število učiteljev in vpisanih učencev).
  - V iskalno polje vpišite del imena (npr. `Mat`) in pokažite filtriran rezultat.
  - Gumbi *Uredi*, *Izbriši* in zgoraj zeleni gumb *+ Nov predmet*.

### Posnetek 3.2: Dodeljevanje predmetov učitelju (M:N)
- **Kaj odpreti:** Meni *Učitelji* → klik na gumb *Uredi* pri enem od učiteljev (npr. `/ucitelji/1/uredi/`).
- **Kaj mora biti vidno:**
  - Obrazec z osebnimi podatki učitelja.
  - Seznam potrditvenih polj (checkbox) za predmete, kjer ima učitelj izbranih več predmetov hkrati.

### Posnetek 3.3: Dodeljevanje predmetov učencu (M:N)
- **Kaj odpreti:** Meni *Učenci* → klik na gumb *Uredi* pri učencu (npr. `/ucenci/1/uredi/`).
- **Kaj mora biti vidno:**
  - Obrazec z vpisno številko, imenom, priimkom in razredom.
  - Potrditvena polja za vpisane predmete (več kot en označen predmet).

---

## 4. Pogled Učitelja (Gradiva, Naloge, Ocenjevanje, CSV)

*Prijava z uporabniškim računom:* `ucitelj1` / `Ucitelj123!`

### Posnetek 4.1: Nadzorna plošča učitelja
- **Kaj odpreti:** Glavna stran učitelja (`/portal/ucitelj/`).
- **Kaj mora biti vidno:**
  - Statistika: število dodeljenih predmetov in število oddaj, ki čakajo na pregled/oceno.
  - Kartice dodeljenih predmetov z gumbi za vstop.

### Posnetek 4.2: Nalaganje učnega gradiva
- **Kaj odpreti:** Odprite posamezen predmet → razdelek *Gradiva* → gumb *Naloži novo gradivo*.
- **Kaj mora biti vidno:**
  - Obrazec za izbiro datoteke in naslova gradiva.
  - Seznam naloženih datotek z gumbi za prenos in brisanje.

### Posnetek 4.3: Upravljanje nalog in ocenjevanje
- **Kaj odpreti:** Zavihek *Naloge* pri predmetu (`/portal/ucitelj/predmet/...`).
- **Kaj mora biti vidno:**
  - Tabela oddanih nalog učencev z datumi oddaje (in rdečo oznako »Prepozno«, če je rok potekel).
  - Prikaz ocene (1–5) ter gumb za vnos/popravek ocene in komentarja.
  - Zgornji gumb **Izvozi CSV** za prenos seznama oddaj in ocen v Excel/CSV formatu.

---

## 5. Pogled Učenca (Vpis predmetov, Oddaja z imenom, Potrditev povozitve, Obvestila)

*Prijava z uporabniškim računom:* `ucenec1` / `Ucenec123!`

### Posnetek 5.1: Nadzorna plošča in temni način (Dark Mode)
- **Kaj odpreti:** Glavna stran učenca (`/portal/ucenec/`).
- **Kaj mora biti vidno:**
  - Prijazen pozdrav učencu z njegovim razredom in seznamom vpisanih predmetov.
  - Kliknite na gumb za preklop temnega načina v navigacijski vrstici (ikona lune/sonca), da se prikaže elegantna temna tema.

### Posnetek 5.2: Izbira predmetov v profilu
- **Kaj odpreti:** Urejanje profila / vpis predmetov (`/portal/ucenec/predmeti/`).
- **Kaj mora biti vidno:**
  - Označena potrditvena polja za predmete, ki jih učenec obiskuje.
  - Opozorilo sistema, da mora učenec imeti izbran vsaj en predmet.

### Posnetek 5.3: Oddaja naloge s pravilnim poimenovanjem
- **Kaj odpreti:** Zavihek *Moje oddaje* (`/portal/ucenec/oddaje/`).
- **Kaj mora biti vidno:**
  - Tabela z oddanimi nalogami.
  - Ime shranjene datoteke v natančnem formatu: **»Priimek Ime – Naslov naloge.končnica«** (npr. *Novak Janez – 1. domača naloga.pdf*).

### Posnetek 5.4: Varnostna potrditev povozitve ob ponovni oddaji
- **Kaj odpreti:** Obrazec za oddajo naloge, ki jo je učenec že enkrat oddal.
- **Kaj mora biti vidno:**
  - Rumeno/rdeče opozorilo: »Ta naloga je že bila oddana!«
  - **Potrditveno polje (checkbox)**: »Potrjujem prepis obstoječe oddaje«.
  - Dokaz, da brez te kljukice sistem zavrne prepis datoteke.

### Posnetek 5.5: Center za obvestila
- **Kaj odpreti:** Klik na ikono zvončka z rdečo številko neprebranih sporočil (`/portal/obvestila/`).
- **Kaj mora biti vidno:**
  - Seznam obvestil o novih nalogah ali prejetih ocenah učitelja.

---

## 6. Varnostni mehanizmi in avtorizacija

### Posnetek 6.1: Zavrnjen nepooblaščen dostop (Koda 403)
- **Kaj storiti:** Kot prijavljen učenec poskusite v naslovno vrstico ročno vtipkati skrbniški naslov:
  `https://localhost/predmeti/` ali `https://localhost/ucitelji/`
- **Kaj mora biti vidno:**
  - Zaslon z napako **403 Forbidden** (Dostop zavrnjen: Za ogled te strani nimate ustreznih pravic).

### Posnetek 6.2: Zaščita naloženih datotek
- **Kaj storiti:** V brskalniku poskusite neposredno odpreti lokacijo datoteke brez avtorizacije, npr.:
  `https://localhost/media/...`
- **Kaj mora biti vidno:**
  - Nginx vrne **404 Not Found** ali **403 Forbidden**, kar dokazuje, da mapa ni javno izpostavljena na spletu.

---

## 7. Preverjanje kakovosti in avtomatizirani testi

### Posnetek 7.1: Uspešno izvedeni testi (26/26 OK)
- **Kaj odpreti:** Terminal (PowerShell) v mapi `c:\Users\mitja\Downloads\sola_sistem`.
- **Ukaz za zagon:**
  ```powershell
  docker compose exec aplikacija python manage.py test
  ```
  *(ali lokalno: `cd aplikacija; python manage.py test`)*
- **Kaj mora biti vidno:**
  - Izpis vseh 26 pikic (`..........................`)
  - Končni izpis: **Ran 26 tests in ...s — OK**.

---

## 8. GitHub repozitorij in sodelovanje

### Posnetek 8.1: Zavihek "Pull requests"
- **Kaj odpreti:** Stran repozitorija na GitHubu: `https://github.com/MitjaJancic/solski_sistem/pulls?q=is%3Apr`
- **Kaj mora biti vidno:**
  - Zaprte in združene zahteve za združitev (Merged Pull Requests) s vijoličnimi ikonami.
  - Sodelovanje med vejami `nal`, `mitja`, `develop` in `main`.

### Posnetek 8.2: Zavihek "Issues"
- **Kaj odpreti:** `https://github.com/MitjaJancic/solski_sistem/issues?q=is%3Aissue+is%3Aclosed`
- **Kaj mora biti vidno:**
  - Rešena in zaprta hrošča: **BUG-01** (Oblikovanje obvestil o napakah) in **BUG-02** (Odzivnost tabel na mobilnih napravah).

### Posnetek 8.3: Oznaka izdaje (Tag v1.0)
- **Kaj odpreti:** `https://github.com/MitjaJancic/solski_sistem/tags`
- **Kaj mora biti vidno:**
  - Oznaka končne različice **`v1.0`**.

---

## Hitri povzetek – katere slike potrebuješ za katero poročilo?

| Poročilo | Zahtevani posnetki |
|---|---|
| **Teden 2** | Posnetek 1.1 (Docker Desktop) in Posnetek 1.2 (Adminer baza z uvoženimi podatki) |
| **Teden 3** | Posnetek 3.1 (Predmeti CRUD), Posnetek 3.2 (Učitelji relacije) |
| **Teden 4** | Posnetek 2.1 (Javna domena), Posnetek 4.2 (Učitelj gradiva), Posnetek 5.3 (Oddaja naloge z imenom) |
| **Teden 5** | Posnetek 2.2 (Mobilni pogled), Posnetek 7.1 (26/26 testov OK), Posnetek 8.2 (GitHub Issues) |
| **Teden 6 / Zagovor** | Posnetki 4.3 (Ocenjevanje + CSV), 5.1 (Dark mode), 5.4 (Potrditev povozitve), 6.1 (403 zaščita), 8.1 (Pull Requests) |
