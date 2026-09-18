# Specifikacija sistema

Šolski IS je spletna aplikacija za podporo šolskemu delu na daljavo. Sistem
omogoča tri poglede: **administrator**, **učitelj** in **učenec**, vsak s
svojimi pravicami (avtorizacija se izvede v 4. tednu).

## 1. Administrator

| # | Funkcionalnost | Podrobnosti |
|---|---|---|
| A1 | Upravljanje predmetov | vpis, urejanje, brisanje; najmanj 10 predmetov |
| A2 | Upravljanje učiteljev | vpis, urejanje, brisanje; najmanj 20 učiteljev |
| A3 | Dodeljevanje predmetov učiteljem | učitelj–predmet je razmerje M:N; nekateri predmeti imajo več učiteljev, nekateri učitelji poučujejo več predmetov |
| A4 | Upravljanje učencev | vpis, urejanje, brisanje; najmanj 100 učencev |
| A5 | Dodeljevanje predmetov učencem | učenec–predmet je razmerje M:N; vsak učenec obiskuje več kot en predmet |

Vse zgornje operacije so dostopne prek uporabniškega vmesnika (`/predmeti/`,
`/ucitelji/`, `/ucenci/`), neposreden vnos v bazo pa ni obvezen, je pa mogoč.

**Status v 3. tednu:** A1–A5 implementirano (CRUD + urejanje relacij prek
obrazcev). Prijava administratorja in omejitev dostopa prideta v 4. tednu.

## 2. Učitelj

| # | Funkcionalnost |
|---|---|
| U1 | Nalaganje in brisanje gradiv za predmete, ki jih dejansko poučuje |
| U2 | Pregled nalog, ki so jih učenci oddali pri izbranem predmetu |

**Status v 3. tednu:** načrtovano za 4. teden (odvisno od prijave/avtorizacije).

## 3. Učenec

| # | Funkcionalnost |
|---|---|
| E1 | Registracija in urejanje lastnega profila |
| E2 | Določanje in popravljanje seznama predmetov, ki jih obiskuje |
| E3 | Vpogled v gradiva vsakega predmeta s seznama |
| E4 | Oddaja nalog; datoteka se shrani kot `Priimek Ime – Naslov naloge`; ponovna oddaja povozi prejšnjo šele po potrditvi učenca |

**Status v 3. tednu:** načrtovano za 4. teden.

## Skupne zahteve

- gesla se shranjujejo izključno zgoščena (Django `PBKDF2`/`argon2`, glej
  [`AUTH_PASSWORD_VALIDATORS`](../aplikacija/solski_sistem/settings.py))
- odzivno oblikovanje (Bootstrap 5)
- vsa koda je pod nadzorom različic (Git/GitHub), delo je sledljivo po
  članih skupine prek vej in commit-ov

## Tehnološke odločitve in utemeljitev

| Kategorija | Izbira | Utemeljitev |
|---|---|---|
| Ogrodje | Python + Django 5.1 (LTS) | vgrajen ORM, admin, avtentikacija in obrazci pospešijo CRUD-intenziven projekt kot je ta |
| Podatkovna baza | MariaDB 11 | ustreza primeru iz navodil, odprtokodna, dobro podprta v Django ORM-u |
| Vsebniki | Docker + Docker Compose | zahteva navodil; ločeni, medsebojno povezani vsebniki za bazo, aplikacijo in posrednika |
| Reverse proxy / HTTPS | Nginx + samopodpisano potrdilo (razvoj) → Let's Encrypt/Certbot (4. teden) | standardna, dobro dokumentirana kombinacija |
| Nadzor različic | Git + GitHub (veje, PR, Issues) | zahteva navodil |
