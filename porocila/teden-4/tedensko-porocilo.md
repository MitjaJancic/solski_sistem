# Tedensko poročilo – teden 4 (Prijava uporabnikov ter pogleda učitelja in učenca)

**Povzetek napredka:** dodana je nova Django aplikacija `portal`, ki uvaja
prijavo, registracijo in avtorizacijo ter pogleda učitelja in učenca.

- **Prijava/registracija in dve vrsti uporabnikov:** uporabniki se prijavijo
  prek Djangove prijave (`/prijava/`, `/odjava/`). Učenec se lahko sam
  registrira (`/registracija/`), kar ustvari Djangovega uporabnika in povezan
  zapis `Ucenec`. Vloge (administrator, učitelj, učenec) hrani model
  `portal.Profil`, ki povezuje uporabnika z zapisom učitelja oz. učenca. Demo
  račune pripravi ukaz `python manage.py seed_uporabniki`.
- **Avtorizacija po vlogah:** preverjanje pravic je zbrano v
  `portal/dovoljenja.py` (mešalniki + funkcije `je_admin/je_ucitelj/je_ucenec`).
  Administratorski CRUD je odslej dostopen le administratorju; nepooblaščen
  dostop vrne 403. Učitelj vidi in ureja **izključno predmete, ki jih poučuje**
  (omejen queryset + dodatno preverjanje ob shranjevanju).
- **Pogled učitelja:** nalaganje in brisanje gradiv za svoje predmete ter
  pregled nalog, ki so jih učenci oddali pri teh predmetih
  (`/ucitelj/...`).
- **Pogled učenca:** urejanje profila, določanje/popravljanje seznama predmetov
  (vsaj en), vpogled v gradiva vpisanih predmetov in oddaja nalog
  (`/ucenec/...`). Datoteka se na strežniku shrani pod imenom
  »Priimek Ime – Naslov naloge« z izvorno končnico; **ponovna oddaja povozi
  prejšnjo datoteko šele po izrecni potrditvi učenca**.

**Sprejete varnostne odločitve:**

- **Zaščita gesel:** gesla se hranijo izključno zgoščena z Djangovim privzetim
  algoritmom **PBKDF2-SHA256** (z naključno soljo in številom iteracij, ki ju
  vzdržuje Django). Gesla se nikoli ne shranijo v čistem besedilu; to potrjuje
  avtomatiziran test, ki preveri, da zapis uporabnika ne vsebuje vnesenega
  gesla in da `check_password` uspe le s pravim geslom.
- **Naložene datoteke niso javno dostopne:** shranjujejo se v `MEDIA_ROOT`, ki
  ga Nginx ne izpostavlja (ni lokacije `/media/`). Dostop je mogoč le prek
  prijavljenih poti `/prenos/gradivo/<id>/` in `/prenos/oddaja/<id>/` s
  preverjanjem pravic (gradivo: administrator / učitelj predmeta / vpisani
  učenec; oddaja: administrator / učitelj predmeta / lastnik oddaje).
- **Varnostne kopije baze:** pripravljena je skripta
  `scripts/varnostna-kopija.sh` (`mariadb-dump` v vsebniku `baza`, stisnjen
  izhod v mapo `backup/` izven vsebnika, hramba zadnjih 7 kopij), z navodilom za
  redni zagon prek crona.

**Javna domena:** aplikacija je pripravljena za postavitev na javno domeno
(Linux strežnik). Postopek in konfiguracija (nastavitev `DOMENA` in
`DJANGO_ALLOWED_HOSTS`, `server_name` v Nginxu, pridobitev in samodejno
podaljševanje Let's Encrypt potrdila s Certbotom) so opisani v
[`dokumentacija/streznik.md`](../../dokumentacija/streznik.md), 4. poglavje.

> Povezava do delujoče javne domene (URL): _<vpiši sem, ko je domena postavljena>_

**Kako je bilo preizkušeno:** samodejni testi (`portal/tests.py`, 13 testov)
z Django test client in SQLite bazo v pomnilniku pokrivajo: preusmeritev/403 za
nepooblaščen dostop, registracijo in zgoščevanje gesla, urejanje predmetov
učenca, omejitev učitelja na svoje predmete, poimenovanje oddane datoteke,
potrditev povozitve ob ponovni oddaji ter zaščiten prenos datotek. Vseh 13
testov je uspešnih.

```bash
cd aplikacija
DJANGO_TEST_SQLITE=1 python manage.py test
```

**Manjka za dokončno oddajo tega tedna:** dejanska postavitev na javno domeno
in vpis URL-ja zgoraj (odvisno od dodeljenega strežnika/domene) ter zaslonski
posnetki pogledov učitelja in učenca za mentorja.

**Načrt za naslednji teden (teden 5):** sistematično testiranje po seznamu
testnih primerov za vse tri poglede, beleženje napak prek GitHub Issues,
izboljšave odzivnega oblikovanja in dokončanje uporabniških navodil ter tehnične
dokumentacije (diagram arhitekture).
