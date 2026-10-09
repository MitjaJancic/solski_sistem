# Seznam testnih primerov

Sistematično testiranje celotne aplikacije za vse tri poglede (5. teden).
Vsak primer ima opis, pričakovan in dejanski rezultat ter status.

**Legenda statusa:** ✅ uspešno · ❌ napaka (glej stolpec Opombe / BUG-ID)

Večina primerov je pokrita tudi z avtomatiziranimi testi
([`aplikacija/administracija/tests.py`](../aplikacija/administracija/tests.py),
[`aplikacija/portal/tests.py`](../aplikacija/portal/tests.py)); zagon:

```bash
cd aplikacija
DJANGO_TEST_SQLITE=1 python manage.py test
```

Rezultat zadnjega zagona: **26 testov, vseh 26 uspešnih.**

## 1. Avtentikacija in avtorizacija

| ID | Opis | Pričakovan rezultat | Dejanski rezultat | Status |
|----|------|---------------------|-------------------|--------|
| AV-01 | Neprijavljen uporabnik odpre administratorski seznam | Preusmeritev na `/prijava/` | Preusmeritev (302) na prijavo | ✅ |
| AV-02 | Učenec odpre administratorski CRUD | Zavrnjeno (403) | 403 | ✅ |
| AV-03 | Administrator odpre CRUD | Prikaz strani (200) | 200 | ✅ |
| AV-04 | Prijava z napačnim geslom | Sporočilo o napaki, ni prijave | Napaka prikazana | ✅ |
| AV-05 | Odjava | Seja se konča, preusmeritev na začetno | Odjava uspešna | ✅ |

## 2. Pogled administratorja

| ID | Opis | Pričakovan rezultat | Dejanski rezultat | Status |
|----|------|---------------------|-------------------|--------|
| AD-01 | Seznam predmetov | Prikaz vseh predmetov | 200, predmeti vidni | ✅ |
| AD-02 | Dodaj predmet | Predmet shranjen, preusmeritev na seznam | Shranjen | ✅ |
| AD-03 | Uredi predmet | Sprememba shranjena | Posodobljeno | ✅ |
| AD-04 | Izbriši predmet | Predmet odstranjen | Izbrisan | ✅ |
| AD-05 | Podvojena šifra predmeta | Zavrnjeno z validacijsko napako | Ostane na obrazcu, ni podvojitve | ✅ |
| AD-06 | Dodaj učitelja z več predmeti (M:N) | Učitelj s 2 predmetoma | 2 predmeta povezana | ✅ |
| AD-07 | Dodaj učenca brez predmeta | Validacijska napaka (vsaj 1 predmet) | Učenec ni ustvarjen | ✅ |
| AD-08 | Dodaj učenca z enim predmetom | Shranjen | Shranjen | ✅ |
| AD-09 | Uredi seznam predmetov učenca | Nov seznam predmetov | Posodobljeno | ✅ |
| AD-10 | Seznam učiteljev / učencev prikaže povezane predmete | Značke predmetov vidne | Vidno | ✅ |

## 3. Pogled učitelja

| ID | Opis | Pričakovan rezultat | Dejanski rezultat | Status |
|----|------|---------------------|-------------------|--------|
| UT-01 | Učitelj vidi samo svoje predmete | Prikaz le poučevanih predmetov | Le svoji predmeti | ✅ |
| UT-02 | Dostop do tujega predmeta (ki ga ne poučuje) | Zavrnjeno (403) | 403 | ✅ |
| UT-03 | Naloži gradivo za svoj predmet | Gradivo shranjeno | Shranjeno | ✅ |
| UT-04 | Naloži gradivo za tuj predmet | Zavrnjeno / obrazec ne dovoli | Ni shranjeno | ✅ |
| UT-05 | Izbriši lastno gradivo | Gradivo odstranjeno | Izbrisano | ✅ |
| UT-06 | Izbriši tuje gradivo | Zavrnjeno (403) | 403 | ✅ |
| UT-07 | Pregled oddanih nalog pri predmetu | Seznam oddaj učencev | Prikazano | ✅ |
| UT-08 | Prenos oddaje učenca pri svojem predmetu | Datoteka prenesena (200) | 200 | ✅ |

## 4. Pogled učenca

| ID | Opis | Pričakovan rezultat | Dejanski rezultat | Status |
|----|------|---------------------|-------------------|--------|
| UC-01 | Samoregistracija učenca | Ustvarjen uporabnik + zapis Ucenec, prijava | Uspešno | ✅ |
| UC-02 | Geslo shranjeno zgoščeno | Ni čistega besedila; PBKDF2 | Zgoščeno (pbkdf2_sha256) | ✅ |
| UC-03 | Urejanje profila | Podatki posodobljeni | Posodobljeno | ✅ |
| UC-04 | Urejanje seznama predmetov | Nov seznam shranjen | Posodobljeno | ✅ |
| UC-05 | Vpogled v gradiva vpisanega predmeta | Prikaz gradiv (200) | 200 | ✅ |
| UC-06 | Vpogled v gradiva nevpisanega predmeta | Zavrnjeno (403) | 403 | ✅ |
| UC-07 | Oddaja naloge – poimenovanje datoteke | »Priimek Ime – Naslov naloge.ext« | Ime pravilno | ✅ |
| UC-08 | Ponovna oddaja brez potrditve | Ne povozi, opozorilo | Ohrani staro datoteko | ✅ |
| UC-09 | Ponovna oddaja s potrditvijo | Povozi prejšnjo datoteko | Povoženo, 1 oddaja | ✅ |
| UC-10 | Prenos tuje oddaje (drug učenec) | Zavrnjeno (403) | 403 | ✅ |

## 5. Varnost naloženih datotek

| ID | Opis | Pričakovan rezultat | Dejanski rezultat | Status |
|----|------|---------------------|-------------------|--------|
| VA-01 | Neposreden dostop do `media/` prek posrednika | Ni javno dostopno | Nginx nima lokacije `/media/` | ✅ |
| VA-02 | Prenos datoteke brez prijave | Preusmeritev na prijavo | 302 na prijavo | ✅ |
| VA-03 | Gesla nikoli v čistem besedilu | Le zgoščena | Potrjeno s testom | ✅ |

## 6. Oblikovanje in odzivnost

| ID | Opis | Pričakovan rezultat | Dejanski rezultat | Status | Opombe |
|----|------|---------------------|-------------------|--------|--------|
| OB-01 | Sporočila o napakah (npr. validacija) | Obarvana rdeče (alert-danger) | Popravljeno | ✅ | BUG-01 |
| OB-02 | Tabele na ozkem zaslonu (telefon) | Vodoravno drsenje, brez preliva | Popravljeno (`.table-responsive`) | ✅ | BUG-02 |
| OB-03 | Postavitev z nogo (footer) na dnu strani | Noga na dnu tudi pri kratki vsebini | Sticky footer | ✅ | |
| OB-04 | Navigacija se zloži na telefonu (hamburger) | Meni delujoč na širini 375 px | Delujoče | ✅ | |

## 7. Odkrite in odpravljene napake (povzetek)

Podrobnosti in sledenje: GitHub Issues (glej tedensko poročilo teden 5).

| BUG-ID | Opis | Resnost | Rešitev | Status |
|--------|------|---------|---------|--------|
| BUG-01 | Sporočila vrste *error* se izpišejo brez oblikovanja (Django oznaka `error` ≠ Bootstrap `danger`) | srednja | `MESSAGE_TAGS = {ERROR: "danger"}` v `settings.py` | odpravljeno |
| BUG-02 | Tabele se na ozkih zaslonih prelivajo čez rob | nizka | Ovoj `.table-responsive` okoli tabel | odpravljeno |
