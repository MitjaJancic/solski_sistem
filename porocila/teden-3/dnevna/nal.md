# Dnevna poročila – Nal Dobravc (razvijalec aplikacije)

## 2026-09-29

**Kaj sem delal:**
- načrtovanje in implementacija CRUD pogledov za predmete v `aplikacija/administracija/views.py`:
  - `predmet_seznam` (pregled vseh predmetov s štetjem vpisov)
  - `predmet_dodaj` (obrazec za vnos novega predmeta z validacijo unikatne šifre)
  - `predmet_uredi` (posodabljanje podatkov predmeta)
  - `predmet_izbrisi` (brisanje s potrditvenim oknom)
- priprava HTML predlog z Bootstrap 5 tabelami in gumbi

**Kaj sem dokončal:**
- celotna CRUD funkcionalnost za predmete z zaščito pred podvajanjem šifer

**Kaj mi ni uspelo in zakaj:**
- pri brisanju predmeta je bilo potrebno paziti na kaskadno brisanje veznih zapisov v `UciteljPredmet` in `UcenecPredmet`.

## 2026-10-01

**Kaj sem delal:**
- izdelava CRUD pogledov in obrazcev za učitelje (`ucitelj_seznam`, `ucitelj_dodaj`, `ucitelj_uredi`, `ucitelj_izbrisi`)
- izdelava CRUD pogledov in obrazcev za učence (`ucenec_seznam`, `ucenec_dodaj`, `ucenec_uredi`, `ucenec_izbrisi`)
- implementacija večizbirnih polj (večkratna izbira predmetov prek checkboxov v obrazcih) za enostavno določanje relacij med učitelji in predmeti ter učenci in predmeti
- dodajanje validacije: učenec mora imeti izbran vsaj en predmet ob vpisu/urejanju

**Kaj sem dokončal:**
- vsi trije seznami s popolnimi CRUD operacijami in urejanjem M:N relacij neposredno v vmesniku

**Kaj mi ni uspelo in zakaj:**
- vse je delovalo v skladu s pričakovanji.

## 2026-10-02

**Kaj sem delal:**
- pisanje avtomatiziranih testov v `aplikacija/administracija/tests.py` (13 testov)
- preverjanje veljavnosti obrazcev, preprečevanje neveljavnih e-poštnih naslovov in podvojenih vpisnih številk
- testiranje delovanja strani z Django testnim odjemalcem

**Kaj sem dokončal:**
- 13 avtomatiziranih testov uspešno prestanih (`OK`), koda je organizirana po plasteh (models, forms, views, urls, templates)

**Kaj mi ni uspelo in zakaj:**
- vse je bilo uspešno zaključeno.
