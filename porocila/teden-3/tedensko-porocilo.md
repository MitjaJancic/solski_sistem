# Tedensko poročilo – teden 3 (Funkcionalnost administratorja in osnove varnosti strežnika)

**Povzetek napredka:** administratorski pogled omogoča vse tri operacije
(vpis, urejanje, brisanje) za predmete, učitelje in učence, vključno z
urejanjem relacij učitelj–predmet in učenec–predmet prek obrazcev
(`/predmeti/`, `/ucitelji/`, `/ucenci/`). Osnovna validacija: šifra/e-pošta
morata biti unikatni, učenec mora imeti izbran vsaj en predmet. Koda je
organizirana po plasteh (`models.py`, `forms.py`, `views.py`, `urls.py`,
predloge ločeno po pogledih) znotraj Django aplikacije `administracija`.

Nginx je konfiguriran kot obrnjeni posrednik pred aplikacijskim vsebnikom
(`nginx/nginx.conf`): vrata 80 preusmerijo na 443, aplikacijski vsebnik ni več
javno dostopen neposredno. Za razvojno fazo je pripravljeno samopodpisano TLS
potrdilo (`scripts/generiraj-certifikat.sh`, že generirano). Dokumentacija
namestitve in konfiguracije strežnika je začeta
([`dokumentacija/streznik.md`](../../dokumentacija/streznik.md)).

**Kako je bila funkcionalnost preizkušena:** ker Docker Desktop na razvojnem
računalniku še ni nameščen, je bila CRUD funkcionalnost preizkušena z
avtomatiziranim testom (Django test client + začasna SQLite baza v pomnilniku)
na realističnih testnih podatkih (10/20/100 zapisov) — seznami, dodajanje,
urejanje, brisanje in validacija so bili preverjeni in delujejo pravilno.
Zagon skozi resnične Docker vsebnike (in s tem nginx/HTTPS pot) še ni bil
preizkušen.

**Manjka za dokončanje zahtev tega tedna:** dejanski zagon celotnega sklada v
Dockerju (aplikacija ⇄ baza ⇄ nginx) po namestitvi Docker Desktop, in
zaslonski posnetki/posnetek delovanja administratorskega pogleda v brskalniku.

**Načrt za naslednji teden (teden 4):** prijava/registracija uporabnikov (dve
vrsti: učitelj, učenec) z gostimi gesli, avtorizacija po vlogah, pogleda
učitelja in učenca, javna domena in prava varnostna kopija baze.
