# Dnevna poročila – Nal Dobravc (razvijalec aplikacije)

## 2026-09-15

**Kaj sem delal:**
- uvodni sestanek z Mitjem in podrobna analiza zahtev iz 3. in 4. poglavja navodil
- določitev vseh potrebnih podatkovnih entitet (predmet, učitelj, učenec ter njune presečne tabele)
- analiza delovnih tokov za tri ločene poglede uporabnikov (administrator, učitelj, učenec)

**Kaj sem dokončal:**
- strukturiran seznam funkcionalnih zahtev sistema za vse tri vloge uporabnikov

**Kaj mi ni uspelo in zakaj:**
- točna logika za potrditev prepisa naloženih datotek pri nalogah je zahtevala dodaten razmislek glede uporabniške izkušnje.

## 2026-09-16

**Kaj sem delal:**
- izdelava ER diagrama podatkovne baze z orodjem Mermaid v markdown dokumentu (`dokumentacija/er-diagram.md`)
- določitev primarnih in tujih ključev ter ustreznih kardinalnosti med tabelami (`Predmet`, `Ucitelj`, `Ucenec`, `UciteljPredmet`, `UcenecPredmet` - 5 tabel)
- priprava podrobnega opisa vseh podatkovnih polj in normalizacije modela

**Kaj sem dokončal:**
- ER diagram z več kot 4 zahtevanimi tabelami in vsemi potrebnimi relacijami M:N

**Kaj mi ni uspelo in zakaj:**
- vse je potekalo v skladu z načrtom.

## 2026-09-18

**Kaj sem delal:**
- izdelava žičnih modelov (wireframov) za administratorski, učiteljski in učenčev pogled v `dokumentacija/specifikacija.md`
- opredelitev elementov vmesnika za CRUD operacije administratorja ter sezname gradiv in oddaj
- uskladitev strukture z Mitjem glede načrtovanih Django predlog

**Kaj sem dokončal:**
- celovita specifikacija sistema z vsemi žičnimi modeli in opisi poteka dela za vse tri uporabniške vloge

**Kaj mi ni uspelo in zakaj:**
- žični modeli so izdelani v obliki markdown skic in preglednic, kar v celoti zadostuje načrtovalni fazi.
