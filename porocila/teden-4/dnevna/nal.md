# Dnevna poročila – Nal Dobravc (razvijalec aplikacije)

## 2026-10-06

**Kaj sem delal:**
- vzpostavitev nove Django aplikacije `portal` za uporabniško avtentikacijo in delo z nalogami/gradivi
- izdelava modela `Profil`, ki povezuje Djangovega `User` z entiteto `Ucitelj` ali `Ucenec` in določa vlogo uporabnika (admin, ucitelj, ucenec)
- izdelava pogledov za prijavo (`/prijava/`), odjavo (`/odjava/`) in registracijo novih učencev (`/registracija/`)
- izdelava ukaza `python manage.py seed_uporabniki` za samodejno ustvarjanje demo uporabniških računov za vsako vlogo z varnimi gesli

**Kaj sem dokončal:**
- delujoča registracija in prijava uporabnikov po vlogah ter inicializirani testni uporabniki

**Kaj mi ni uspelo in zakaj:**
- ob registraciji je bilo potrebno paziti na sočasno ustvarjanje zapisa `Ucenec` in uporabniškega profila `Profil`.

## 2026-10-07

**Kaj sem delal:**
- načrtovanje in implementacija avtorizacijskih mehanizmov v `aplikacija/portal/dovoljenja.py`
- izdelava dekoratorjev in mešalnikov: `je_admin`, `je_ucitelj`, `je_ucenec` ter `zahtevaj_vlogo`
- zaščita vseh skrbniških pogledov (`administracija`), da nepooblaščen uporabnik prejme kodo 403 Forbidden
- stroga omejitev pogleda učitelja: učitelj lahko vidi in upravlja izključno predmete, ki jih sam poučuje

**Kaj sem dokončal:**
- celovit avtorizacijski sistem po vlogah z doslednim preverjanjem pravic

**Kaj mi ni uspelo in zakaj:**
- vse je teklo po načrtu.

## 2026-10-08

**Kaj sem delal:**
- implementacija pogleda učitelja (`/ucitelj/predmeti/`, `/ucitelj/predmet/<id>/`):
  - pregled dodeljenih predmetov
  - nalaganje novih učnih gradiv za posamezen predmet in brisanje gradiv
  - pregled nalog in seznama oddaj, ki so jih oddali vpisani učenci
- priprava zaščitenega pogleda za varen prenos gradiv (`/prenos/gradivo/<id>/`)

**Kaj sem dokončal:**
- delujoč učiteljski pogled z nalaganjem gradiv in pregledom oddanih nalog

**Kaj mi ni uspelo in zakaj:**
- pri prenosu datotek je bilo potrebno zagotoviti, da učenec ne more prenesti gradiva predmeta, ki ga ne obiskuje.

## 2026-10-09

**Kaj sem delal:**
- implementacija pogleda učenca (`/ucenec/`):
  - urejanje profila in določanje seznama predmetov, ki jih obiskuje (z varovalko: vsaj 1 predmet)
  - pregled gradiv pri vpisanih predmetih in varen prenos datotek
  - oddaja nalog z izrecno zahtevanim poimenovanjem datoteke: »Priimek Ime – Naslov naloge«
  - implementacija varnostne potrditve ob ponovni oddaji naloge (potrditveno stikalo/checkbox v obrazcu; če potrditev ni obkljukana, se predhodna datoteka ne prepiše)
- izdelava razreda `PovoznoShranjevanje` za ohranitev pravilnih imen datotek s šumniki in presledki
- priprava 13 avtomatiziranih testov v `portal/tests.py`

**Kaj sem dokončal:**
- učenčev pogled s specifičnimi zahtevami glede oddaje nalog, vseh 13 novih testov uspešnih

**Kaj mi ni uspelo in zakaj:**
- privzeti Django shrambeni mehanizem je spreminjal znake v imenih datotek, kar smo uspešno rešili z namenskim prilagojenim razredom za shranjevanje.
