# Specifikacija sistema

Šolski IS je spletna aplikacija za podporo šolskemu delu na daljavo. Sistem
omogoča tri poglede: **administrator**, **učitelj** in **učenec**, vsak s
svojimi pravicami (avtorizacija je uvedena v 4. tednu).

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

**Status v 4. tednu:** A1–A5 implementirano (CRUD + urejanje relacij prek
obrazcev). Dostop do administratorskih pogledov je od 4. tedna omejen na
prijavljenega administratorja (`AdminZahtevanMixin`).

## 2. Učitelj

| # | Funkcionalnost |
|---|---|
| U1 | Nalaganje in brisanje gradiv za predmete, ki jih dejansko poučuje |
| U2 | Pregled nalog, ki so jih učenci oddali pri izbranem predmetu |

**Status v 4. tednu:** implementirano. Učitelj vidi in ureja izključno predmete,
ki jih poučuje (queryset omejen na `Predmet.objects.filter(ucitelji=...)`,
dodatno preverjanje ob shranjevanju). Nalaganje/brisanje gradiv:
`/ucitelj/gradivo/...`; pregled oddanih nalog: `/ucitelj/predmet/<id>/`.

## 3. Učenec

| # | Funkcionalnost |
|---|---|
| E1 | Registracija in urejanje lastnega profila |
| E2 | Določanje in popravljanje seznama predmetov, ki jih obiskuje |
| E3 | Vpogled v gradiva vsakega predmeta s seznama |
| E4 | Oddaja nalog; datoteka se shrani kot `Priimek Ime – Naslov naloge`; ponovna oddaja povozi prejšnjo šele po potrditvi učenca |

**Status v 4. tednu:** implementirano. Učenec se samoregistrira
(`/registracija/`), ureja profil (`/ucenec/profil/`) in seznam predmetov
(`/ucenec/predmeti/`, vsaj en predmet), pregleduje gradiva vpisanih predmetov
in oddaja naloge (`/ucenec/oddaje/nova/`). Datoteka se na strežniku shrani pod
imenom »Priimek Ime – Naslov naloge« z izvorno končnico (`pot_oddaje` +
`PovoznoShranjevanje`). Ponovna oddaja iste naloge povozi prejšnjo datoteko
šele, ko učenec označi potrditev povozitve.

## Skupne zahteve

- gesla se shranjujejo izključno zgoščena (Django privzeto `PBKDF2-SHA256`;
  preverjeno s testom, da zapis uporabnika ne vsebuje gesla v čistem besedilu)
- naložene datoteke (gradiva, oddaje) **niso javno dostopne** — postrežejo se
  le prek prijavljenih poti s preverjanjem pravic (`/prenos/...`); zunanji
  posrednik (Nginx) mape `media/` ne izpostavlja
- odzivno oblikovanje (Bootstrap 5)
- vsa koda je pod nadzorom različic (Git/GitHub), delo je sledljivo po
  članih skupine prek vej in commit-ov

## Avtorizacija (4. teden)

Dve vrsti prijavljenih uporabnikov po zahtevi navodil sta **učitelj** in
**učenec**; **administrator** je tretja vloga (Djangov `is_staff`/`is_superuser`
oz. `Profil.vloga = admin`). Vloga je shranjena v modelu
[`portal.Profil`](../aplikacija/portal/models.py), ki povezuje Djangovega
uporabnika z zapisom `Ucitelj`/`Ucenec`. Preverjanje pravic je zbrano v
[`portal/dovoljenja.py`](../aplikacija/portal/dovoljenja.py) (mešalniki
`AdminZahtevanMixin`, `UciteljZahtevanMixin`, `UcenecZahtevanMixin` in funkcije
`je_admin`/`je_ucitelj`/`je_ucenec`). Pravilo: noben uporabnik ne dostopa do
funkcij, ki mu ne pripadajo (nepooblaščen dostop vrne 403).

## Tehnološke odločitve in utemeljitev

| Kategorija | Izbira | Utemeljitev |
|---|---|---|
| Ogrodje | Python + Django 5.1 (LTS) | vgrajen ORM, admin, avtentikacija in obrazci pospešijo CRUD-intenziven projekt kot je ta |
| Podatkovna baza | MariaDB 11 | ustreza primeru iz navodil, odprtokodna, dobro podprta v Django ORM-u |
| Vsebniki | Docker + Docker Compose | zahteva navodil; ločeni, medsebojno povezani vsebniki za bazo, aplikacijo in posrednika |
| Reverse proxy / HTTPS | Nginx + samopodpisano potrdilo (razvoj) → Let's Encrypt/Certbot (4. teden) | standardna, dobro dokumentirana kombinacija |
| Nadzor različic | Git + GitHub (veje, PR, Issues) | zahteva navodil |
