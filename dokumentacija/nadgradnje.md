# Šolski IS+ — nadgradnje in nove ideje

Ta različica nadgradi osnovni projekt (zahteve navodil so v celoti ohranjene) z
idejami, ki aplikacijo spremenijo iz preprostega *nalaganja datotek* v
zaokrožen **učni potek**: naloge z roki, oddaje, ocenjevanje s povratno
informacijo, pregledne nadzorne plošče, obvestila in temni način.

## 1. Naloge z roki (nova entiteta `Naloga`)

Prej je učenec oddal datoteko s poljubnim naslovom. Zdaj **učitelj ustvari
nalogo** (naslov, navodila, **rok oddaje**) pri predmetu, ki ga poučuje, učenci
pa oddajo rešitev točno te naloge.

- jasna povezava naloga → oddaje,
- stanje naloge: *odprta* / *rok potekel*,
- oddaja po roku se samodejno označi kot **prepozna** (`Oddaja.prepozno`).

Ohranjeno iz navodil: datoteka se shrani kot »Priimek Ime – Naslov naloge«;
ponovna oddaja povozi prejšnjo šele po potrditvi učenca.

## 2. Ocenjevanje s povratno informacijo

Učitelj oddajo **oceni (1–5)** in doda **komentar**. Učenec vidi oceno in
povratno informacijo pri nalogi. Ob ponovni oddaji se prejšnja ocena razveljavi
(učitelj znova pregleda). Polja: `Oddaja.ocena`, `Oddaja.komentar`,
`Oddaja.ocenjeno`.

## 3. Nadzorni plošči s statistiko

- **Učenec:** število predmetov, oddaj in ocen, **povprečna ocena** ter seznam
  **prihajajočih nalog** (odprte, še neoddane).
- **Učitelj:** število predmetov in nalog, **število neocenjenih oddaj**, tabela
  nalog s številom oddaj in »za oceniti«.

Uporabljeni so agregati ORM (`Count`, `Avg`, `Q`) namesto ročnega štetja.

## 4. Obvestila (`Obvestilo`)

Preprosta obvestila ob ključnih dogodkih:

- učenec dobi obvestilo ob **novi nalogi** pri svojem predmetu in ob **prejeti
  oceni**;
- učitelj dobi obvestilo ob **novi oddaji**.

Število neprebranih se prikaže kot značka ob zvončku v navigaciji (prek
kontekstnega procesorja `portal.context.obvestila`); ob ogledu seznama se
označijo kot prebrana.

## 5. Temni način (dark mode)

Preklopnik teme v navigaciji uporablja vgrajene barvne načine Bootstrap 5.3
(`data-bs-theme`), izbira se shrani v `localStorage` in se uporabi pred izrisom
(brez utripanja). Tabele in kartice so prilagojene obema temama (`bg-body`).

## 6. Vpliv na podatkovni model

Novi/spremenjeni modeli v `portal`:

| Model | Opis |
|------|------|
| `Naloga` | naloga z rokom pri predmetu (ustvari učitelj) |
| `Oddaja` | vezana na `Naloga`; polja `prepozno`, `ocena`, `komentar`, `ocenjeno` |
| `Obvestilo` | obvestilo prejemniku (neprebrano/prebrano) |

Ostali modeli (`Profil`, `Gradivo`, `Predmet`, `Ucitelj`, `Ucenec` + presečni
tabeli) ostajajo. Preverjanje pravic ostaja centralizirano v
`portal/dovoljenja.py`, datoteke ostajajo zaščitene (`/prenos/...`).

## 7. Testiranje

Posodobljen nabor avtomatiziranih testov pokriva nov potek (naloge,
poimenovanje datotek, prepozna oddaja, potrditev povozitve z razveljavitvijo
ocene, ocenjevanje + obvestila, omejitve pravic). Skupaj **26 testov**, vsi
uspešni:

```bash
cd aplikacija
DJANGO_TEST_SQLITE=1 python manage.py test
```
