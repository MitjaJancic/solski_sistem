# Zaključno poročilo skupine

**Projekt:** Šolski IS — spletna aplikacija za podporo šolskemu delu na daljavo
**Skupina:** Mitja Jančič (vzdrževalec IS + razvijalec), Nal Dobravc (razvijalec), Matic Holobar (mentor)
**Povezava do repozitorija:** https://github.com/MitjaJancic/solski_sistem
**Povezava do delujoče aplikacije:** https://lens-computing-marina-chemical.trycloudflare.com (Cloudflare Tunnel HTTPS, preveri s skripto `scripts/pokazi-javni-url.ps1`)
**Končna različica:** oznaka (tag) `v1.0`

## 1. Povzetek

Izdelali smo spletno aplikacijo s podatkovno bazo, postavljeno v Docker
vsebnike, dostopno prek HTTPS na javni domeni. Sistem podpira tri poglede
(administrator, učitelj, učenec) z avtentikacijo in avtorizacijo po vlogah.
Projekt izpolnjuje zahteve iz 3. in 4. poglavja navodil.

**Tehnologije:** Python + Django 5.1, MariaDB 11, Docker + Docker Compose,
Nginx (obrnjeni posrednik + HTTPS), gunicorn + WhiteNoise (produkcija),
Git + GitHub (veje, vlečni zahtevki, Issues).

## 2. Potek dela po tednih

| Teden | Vsebina | Glavni rezultat |
|------|---------|-----------------|
| 1 | Analiza, načrtovanje, priprava okolja | repozitorij, struktura, Docker, specifikacija, ER diagram, wireframi |
| 2 | Infrastruktura in podatkovna baza | docker-compose, MariaDB v vsebniku, SQL/seed, ogrodje aplikacije |
| 3 | Administratorski CRUD + osnove varnosti | CRUD predmetov/učiteljev/učencev + relacije; Nginx reverse proxy; samopodpisano HTTPS |
| 4 | Prijava, avtorizacija, pogleda učitelja in učenca | prijava/registracija, vloge, gradiva, oddaje z zaščito datotek; skripta za backup |
| 5 | Testiranje, oblikovanje, dokumentacija | 26 avtomatiziranih testov, seznam testnih primerov, odprava napak, odzivni UI, arhitektura, uporabniška navodila |
| 6 | Zaključno testiranje, predstavitev, oddaja | produkcijska sestava (gunicorn/WhiteNoise, varnostne nastavitve), predstavitev, zaključni pregled, tag `v1.0` |

## 3. Izpolnjevanje zahtev (3. in 4. poglavje)

- **Administrator:** vpis/urejanje/brisanje predmetov (≥10), učiteljev (≥20),
  učencev (≥100) ter relacij (predmeti z več učitelji, učitelji z več predmeti,
  učenci z več predmeti) — prek vmesnika.
- **Učitelj:** nalaganje/brisanje gradiv samo za predmete, ki jih poučuje;
  pregled oddanih nalog.
- **Učenec:** registracija, urejanje profila, izbira predmetov (>1), vpogled v
  gradiva, oddaja nalog s poimenovanjem »Priimek Ime – Naslov naloge« in
  potrditvijo povozitve.
- **Varnost:** gesla zgoščena (PBKDF2-SHA256); naložene datoteke niso javno
  dostopne; avtorizacija dosledna (nepooblaščen dostop = 403); HTTPS.
- **Podatkovni model:** 8 tabel (zahtevane najmanj 4).

## 4. Glavni izzivi in rešitve

| Izziv | Rešitev |
|------|---------|
| Ime oddane datoteke mora biti točno »Priimek Ime – Naslov naloge« | Django privzeto očisti ime datoteke (presledki, pomišljaj); uvedli smo lastno shranjevanje (`PovoznoShranjevanje`), ki ime ohrani in ob ponovni oddaji povozi datoteko |
| Povozitev prejšnje oddaje šele po potrditvi | Potrditveno polje v obrazcu; brez potrditve se obstoječa oddaja ne povozi (preverjeno s testom) |
| Naložene datoteke ne smejo biti javno dostopne | Nginx ne streže `media/`; dostop le prek prijavljenih poti `/prenos/...` s preverjanjem pravic |
| Učitelj sme videti/urejati samo svoje predmete | Omejen queryset + dodatno preverjanje ob shranjevanju; centralizirana pravila v `portal/dovoljenja.py` |
| Sporočila o napakah brez oblikovanja (BUG-01) | Preslikava Django oznake `error` v Bootstrap `danger` |
| Produkcijsko streženje (javna domena) | gunicorn + WhiteNoise; ločen razvojni `docker-compose.override.yml` in produkcijska osnovna sestava |

## 5. Delitev dela med člani skupine

- **Mitja Jančič (vzdrževalec IS + razvijalec):** repozitorij in veje,
  Docker/Docker Compose, `docker-compose(.override).yml` in `.env`, Nginx +
  HTTPS, produkcijska sestava (gunicorn/WhiteNoise), varnostne kopije,
  dokumentacija strežnika in arhitekture; sodelovanje pri backend logiki.
- **Nal Dobravc (razvijalec):** specifikacija, ER diagram in wireframi, modeli
  in obrazci, administratorski CRUD, pogleda učitelja in učenca, uporabniška
  navodila; sodelovanje pri testiranju.
- **Oba (skupno):** sistematično testiranje, odprava napak (GitHub Issues),
  dnevna in tedenska poročila, predstavitev.
- **Matic Holobar (mentor):** pregled ob mejnikih in potrjevanje napredka.

> Sledljivost dela vseh članov je razvidna iz zgodovine commitov in vlečnih
> zahtevkov v repozitoriju.

## 6. Zaključek

Aplikacija je ob zagovoru v celoti dostopna in delujoča na javni domeni.
Skupina je sposobna samostojno predstaviti in utemeljiti sprejete tehnične
odločitve. Priloge: povezava do repozitorija in do delujoče aplikacije (zgoraj),
predstavitev v mapi [`predstavitev/`](../predstavitev/predstavitev.md).
