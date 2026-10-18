---
marp: true
title: Šolski IS – predstavitev projekta
paginate: true
---

# Šolski IS

### Spletna aplikacija za podporo šolskemu delu na daljavo

Zaključni projekt · skupina 3 dijakov + mentor

- Mitja Jančič — vzdrževalec IS + razvijalec
- Nal Dobravc — razvijalec
- mentor — spremljanje in potrjevanje mejnikov

---

## Cilj projekta

- spletna aplikacija s podatkovno bazo pod nadzorom različic (Git/GitHub)
- postavitev v Docker vsebnike na strežniku Linux
- objava delujoče aplikacije na javni domeni (HTTPS)
- samostojno timsko delo

Trije pogledi: **administrator**, **učitelj**, **učenec**.

---

## Tehnologije

| Kategorija | Izbira |
|---|---|
| Ogrodje | Python + Django 5.1 |
| Baza | MariaDB 11 |
| Vsebniki | Docker + Docker Compose |
| Posrednik / HTTPS | Nginx + Let's Encrypt |
| Aplikacijski strežnik | gunicorn + WhiteNoise |
| Nadzor različic | Git + GitHub (veje, PR, Issues) |

Utemeljitev: vgrajeni ORM, avtentikacija in obrazci pospešijo CRUD-intenziven projekt.

---

## Arhitektura

```
uporabnik --HTTPS--> [ Nginx ] --:8000--> [ Django (gunicorn) ] --:3306--> [ MariaDB ]
                        proxy               administracija + portal          volumen
```

- ves promet skozi posrednik (TLS)
- aplikacija in baza v ločenih, povezanih vsebnikih
- naložene datoteke **niso** javno dostopne

Podroben diagram: `dokumentacija/arhitektura.md`.

---

## Podatkovni model (8 tabel)

- `Predmet`, `Ucitelj`, `Ucenec` + presečni tabeli M:N
- `Profil` (vloga + povezava z Django uporabnikom)
- `Gradivo`, `Oddaja`

Vsaj 4 tabele s pravilnimi primarnimi/tujimi ključi — izpolnjeno (8).

---

## Funkcionalnosti — administrator

- CRUD predmetov (≥10), učiteljev (≥20), učencev (≥100)
- relacije: predmeti z več učitelji, učitelji z več predmeti,
  učenci z več predmeti
- dostop omejen na prijavljenega administratorja

---

## Funkcionalnosti — učitelj in učenec

**Učitelj:** nalaganje/brisanje gradiv *samo za svoje predmete*, pregled oddanih nalog.

**Učenec:** registracija, profil, izbira predmetov, vpogled v gradiva,
oddaja nalog:
- datoteka shranjena kot **»Priimek Ime – Naslov naloge.ext«**
- ponovna oddaja povozi prejšnjo **šele po potrditvi**

---

## Varnost

- gesla zgoščena (PBKDF2-SHA256), nikoli v čistem besedilu
- avtorizacija po vlogah — nepooblaščen dostop = 403
- naložene datoteke le prek preverjenih poti `/prenos/...`
- HTTPS, varni piškotki in HSTS v produkciji
- redne varnostne kopije baze

---

## Kakovost: testiranje

- **26 avtomatiziranih testov** za vse tri poglede — vsi uspešni
- seznam testnih primerov z opisom in statusom
- napake beležene in odpravljene (GitHub Issues)

```bash
cd aplikacija
DJANGO_TEST_SQLITE=1 python manage.py test
```

---

## Potek dela po tednih

1. analiza, načrtovanje, priprava okolja
2. infrastruktura in podatkovna baza
3. administratorski CRUD + osnove varnosti strežnika
4. prijava/avtorizacija + pogleda učitelja in učenca
5. testiranje, oblikovanje, dokumentacija
6. zaključno testiranje, predstavitev, oddaja

---

## Demonstracija

Živa predstavitev (glej `predstavitev/demo-scenarij.md`):

1. administrator: doda predmet/učitelja/učenca
2. učitelj: naloži gradivo za svoj predmet
3. učenec: registracija → izbira predmetov → vpogled v gradivo → oddaja naloge
4. ponovna oddaja s potrditvijo povozitve
5. prikaz zavrnjenega dostopa (403) do tuje funkcije

---

## Zaključek

- projekt izpolnjuje vse zahteve navodil (3. in 4. poglavje)
- delujoča aplikacija na javni domeni: _<URL>_
- repozitorij: _<povezava do GitHub repozitorija>_
- končna različica označena z oznako `v1.0`

### Hvala za pozornost — vprašanja?
