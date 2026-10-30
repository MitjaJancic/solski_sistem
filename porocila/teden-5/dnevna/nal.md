# Dnevna poročila – Nal Dobravc (razvijalec aplikacije)

## 2026-10-13

**Kaj sem delal:**
- priprava podrobnega seznama testnih primerov za vse tri poglede v `dokumentacija/testni-primeri.md` (opredelitev predpogojev, korakov, pričakovanega in dejanskega rezultata ter statusa uspešnosti)
- razširitev zbirke samodejnih testov v `administracija/tests.py` in `portal/tests.py`
- skupni zagon testov: 26 testov, vseh 26 uspešno prestanih brez napak

**Kaj sem dokončal:**
- celovit katalog testnih primerov in 26 avtomatiziranih testov, ki pokrivajo ključne točke sistema

**Kaj mi ni uspelo in zakaj:**
- vse je delovalo brezhibno.

## 2026-10-15

**Kaj sem delal:**
- odprava napake **BUG-02**: dodajanje ovitka `.table-responsive` okoli vseh tabel v seznamih administratorja, učitelja in učenca, s čimer je omogočeno vodoravno drsenje na ozkih zaslonih
- oblikovne izboljšave uporabniškega vmesnika: poenotenje slogov kartic, gumbov in oblike noge strani (`footer`), ki se sedaj lepo prilega dnu strani
- testiranje delovanja vmesnika na mobilnem pogledu

**Kaj sem dokončal:**
- odziven (responsive) uporabniški vmesnik na vseh podstraneh, BUG-02 odpravljen in zaprt na GitHubu

**Kaj mi ni uspelo in zakaj:**
- pri nekaterih gumbih na mobilnih napravah je bilo treba nekoliko prilagoditi razmike (`gap`).

## 2026-10-16

**Kaj sem delal:**
- priprava podrobnih uporabniških navodil za vse tri vloge v `dokumentacija/uporabniska-navodila.md`:
  - navodila za administratorja (vnos, urejanje in brisanje podatkov ter dodeljevanje predmetov)
  - navodila za učitelja (pregled predmetov, delo z gradivi, pregledovanje oddaj)
  - navodila za učenca (registracija, vpisovanje predmetov, pregled gradiv in oddaja nalog)
- pregled razumljivosti navodil za nove uporabnike

**Kaj sem dokončal:**
- izčrpna uporabniška navodila za vse tri tipe uporabnikov

**Kaj mi ni uspelo in zakaj:**
- vse naloge so bile uspešno dokončane.
