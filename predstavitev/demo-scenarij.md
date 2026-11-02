# Scenarij zagovora v živo (Mitja Jančič & Nal Dobravc)

Ta dokument je pripravljen kot natančen govorni in praktični scenarij za zagovor pred mentorjem **prof. Maticem Holobarjem**. Delo je enakomerno razdeljeno med **Mitjo** (vzdrževalec IS + razvijalec administracije) in **Nala** (razvijalec portala za učitelje in učence).

---

## Predpriprava (2 minuti pred vstopom mentorja)
1. **Brskalnik – Zavihek 1:** Odprt `http://localhost/` (na pristajalni strani, neprijavljen).
2. **Brskalnik – Zavihek 2:** Odprt Adminer `http://localhost:8081/` (prijavljen v bazo `sola_is`, strežnik `baza`, uporabnik `sola_is_app`, geslo `l0U0Fjj2lQGZS4JiESqvR2IW`).
3. **Brskalnik – Zavihek 3:** Odprt GitHub `https://github.com/MitjaJancic/solski_sistem` (kjer se vidijo veje, Pull Requesti in zaprti Issue-ji).
4. **Terminal (PowerShell):** Odprt v mapi `c:\Users\mitja\Downloads\sola_sistem`.
5. **Pripravljena testna datoteka na namizju:** Ustvarite poljubno datoteko (npr. `naloga_test.pdf` ali `resitev.txt`), ki jo boste med zagovorom v živo oddali.

---

## 1. DEL: Uvod, Docker infrastruktura in GitHub (Govori: MITJA — 2 min)

### 🎤 Kaj pove Mitja:
> »Pozdravljeni. Predstavila bova zaključni projekt **Šolski IS+**, spletno aplikacijo za podporo šolskemu delu na daljavo. Jaz sem skrbel za sistemsko infrastrukturo, kontejnerizacijo, podatkovno bazo, varnost in administratorski del, Nal pa za razvoj uporabniškega portala za učitelje in učence ter sistem oddaje in ocenjevanja nalog.«

### 💻 Kaj pokaže Mitja:
1. **Preklopi na Terminal** in zažene:
   ```powershell
   docker compose ps
   ```
   * **Mitja pove:** »Celoten sistem teče v 5 ločenih, med seboj povezanih Docker vsebnikih: `baza` (MariaDB 11), `aplikacija` (Django 5 / Gunicorn), `proxy` (Nginx kot obrnjeni posrednik s HTTPS šifriranjem), `adminer` za vpogled v bazo ter `tunel` (Cloudflare Tunnel za javno domeno). Podatki so shranjeni na trajnem Docker volumnu, za varnostne kopije pa sva pripravila skripto `scripts/varnostna-kopija.sh`.«

2. **Preklopi na Zavihek 3 (GitHub):**
   * Pokaže veje (`main`, `develop`, `mitja`, `nal`), klikne na **Pull requests -> Closed (3)** in **Issues -> Closed (2)**.
   * **Mitja pove:** »Razvoj je potekal po 6-tedenskem načrtu. Vsak je razvijal na svoji veji, kodo sva pregledovala prek Pull Requestov in odpravila zabeležene napake v GitHub Issues. Končna različica je označena z izdajo `v2.0`.«

3. **Preklopi na Zavihek 2 (Adminer):**
   * Pokaže seznam tabel (`administracija_predmet`, `administracija_ucitelj`, `administracija_ucenec`, `portal_gradivo`, `portal_naloga`, `portal_oddaja`, `portal_obvestilo`, `portal_profil`) in klikne na tabelo `auth_user`.
   * **Mitja pove:** »Podatkovni model obsega 8 glavnih tabel z vmesnimi M:N tabelami. Kot vidite v tabeli `auth_user`, so vsa gesla zgoščena z algoritmom **PBKDF2-SHA256** in nikoli shranjena v čistem besedilu.«

---

## 2. DEL: Pogled Administratorja (Govori: MITJA — 2 min)

### 💻 Kaj klikne in pove Mitja (Zavihek 1 – Aplikacija):
1. Na začetni strani klikne gumb **Temni način / Svetli način** v zgornjem meniju.
   * **Mitja pove:** »Uporabniški vmesnik je zgrajen z ogrodjem Bootstrap 5, vektorskimi ikonami in podpira preklop med svetlim in temnim načinom.«
2. Klikne **Prijava** in vpiše:
   * Uporabniško ime: `admin`
   * Geslo: `Admin123!`
3. **Nadzorna plošča administratorja:**
   * **Mitja pove:** »V bazi imamo 10 predmetov, 20 učiteljev in 120 učencev, razdeljenih v tri razrede (4.A, 4.B in 4.C). Vsa uporabniška imena so standardizirana v obliki `Začetnica.Priimek`, prijava pa je neobčutljiva na velike/male črke in šumnike.«
4. Klikne v meniju na **Predmeti**:
   * Klikne **+ Nov predmet**, vpiše šifro `ROB`, ime `Robotika`, opis `Osnove robotike` in klikne **Shrani**.
   * Nato pri predmetu `Robotika` klikne **Izbriši** in potrdi brisanje.
   * **Mitja pove:** »Administratorju je prek vmesnika omogočen poln CRUD nad predmeti, učitelji in učenci.«
5. Klikne na **Učitelji**:
   * Pokaže vrstico **Holobar Matic (`M.Holobar`)**, kjer se vidita znački `INF` in `MAT`.
   * **Mitja pove:** »Tukaj je prikazana relacija več-proti-več (M:N): posamezen učitelj poučuje več predmetov, prav tako pa ima posamezen predmet več učiteljev.«
6. Klikne na **Učenci**:
   * V iskalno polje vpiše `Jančič` in klikne **Išči**.
   * Pokaže učenca **Jančič Mitja (4.A)** s seznamom vpisanih predmetov.
7. Klikne **Odjava** in preda besedo Nalu.

---

## 3. DEL: Pogled Učitelja in ocenjevanje (Govori: NAL — 2.5 min)

### 🎤 Kaj pove Nal:
> »Jaz bom predstavil uporabniški portal za učitelje in učence, ki vključuje avtorizacijo po vlogah, upravljanje gradiv, oddajo nalog s pravilnim poimenovanjem ter nadgradnjo: ustvarjanje nalog z roki, ocenjevanje in center za obvestila.«

### 💻 Kaj klikne in pove Nal:
1. Prijavi se kot učitelj (mentorjev račun):
   * Uporabniško ime: `M.Holobar` (ali `m.holobar`)
   * Geslo: `Ucitelj123!`
2. **Pregled učitelja:**
   * **Nal pove:** »Ob prijavi učitelj vidi svojo nadzorno ploščo: število dodeljenih predmetov, aktivne naloge in koliko oddaj čaka na oceno. Učitelj ima dostop **izključno do predmetov, ki jih dejansko poučuje** – v tem primeru Informatika in Matematika.«
3. Klikne na predmet **Informatika** (*Učilnica predmeta*):
   * Pokaže tabelo **Učna gradiva predmeta** in klikne **Naloži gradivo** (zgoraj desno).
   * Pokaže spustni seznam predmetov.
   * **Nal pove:** »Pri nalaganju gradiva lahko učitelj izbere samo svoj predmet. Tujih predmetov sistem sploh ne ponudi, tudi ob ročnem poskusu prek URL-ja pa strežnik vrne napako `403 Forbidden`.«
4. Vrne se nazaj v učilnico predmeta **Informatika** in v tabeli nalog klikne **Pregled oddaj** pri nalogi *»Načrtovanje podatkovne baze«*:
   * Pokaže seznam oddanih nalog dijakov.
   * **Nal pove:** »Učitelj tukaj vidi vse oddaje učencev pri svojem predmetu, natančen čas oddaje in rdečo oznako, če je bila naloga oddana po roku. Seznam lahko tudi izvozi v CSV.«
5. Pri enem izmed učencev (npr. **Kovač Luka**, ki ima status *V pregledu* ali pri **Jančič Mitja**) klikne **Oceni** (ali **Popravi**):
   * Izbere oceno **`5`**, v komentar vpiše: `Odlično izdelan ER diagram in normalizacija.` ter klikne **Shrani oceno**.
   * **Nal pove:** »Ko učitelj shrani oceno, sistem učencu samodejno pošlje obvestilo v njegov center za obvestila.«
6. Klikne **Odjava**.

---

## 4. DEL: Pogled Učenca, poimenovanje datoteke in povozitev (Govori: NAL — 2.5 min)

### 💻 Kaj klikne in pove Nal:
1. Na prijavni strani klikne spodaj **Registracija učenca** (`/registracija/`):
   * **Nal pove:** »Novi učenci se lahko sami registrirajo in si uredijo profil, za demonstracijo pa se bova prijavila z obstoječim računom dijaka.«
2. Klikne nazaj na **Prijava** in se prijavi kot učenec:
   * Uporabniško ime: `M.Jancic`
   * Geslo: `Ucenec123!`
3. **Pregled učenca:**
   * Pokaže statistiko (vpisani predmeti, oddane naloge, povprečna ocena) in zgoraj v meniju klikne na **zvonček (Obvestila)**, kjer sveti rdeča številka.
   * **Nal pove:** »Učenec takoj prejme neprebrano obvestilo, da mu je profesor Matic Holobar pravkar ocenil nalogo.«
4. V zgornjem meniju klikne **Moji predmeti** (`/ucenec/predmeti/`):
   * **Nal pove:** »Učenec si tukaj sam določa in popravlja seznam predmetov, ki jih obiskuje. Validacija zahteva, da obiskuje vsaj en predmet.«
   * Klikne **Prekliči** (ali **Shrani izbiro**).
5. Na pregledu učenca pri predmetu **Informatika** klikne **Učna gradiva predmeta**:
   * Klikne **Prenesi** pri enem gradivu.
   * **Nal pove:** »Učenec ima vpogled v gradiva vseh svojih predmetov. Datoteke niso javno dostopne v mapi `/media/`, ampak gre vsak prenos čez zaščiten Django pogled `/prenos/`, ki preveri, ali je učenec res vpisan v ta predmet.«
6. V zgornjem meniju klikne **Naloge** in odpre nalogo (npr. *»Normalizacija relacijske sheme (3NF)«* ali *»Načrtovanje podatkovne baze«*):
   * **Nal pove:** »Tukaj prideva do ključne zahteve navodil: oddaja naloge, avtomatsko preimenovanje datoteke in potrditev povozitve.«
   * **1. korak (Oddaja):** Če naloga še ni oddana, izbere datoteko z računalnika in klikne **Oddaj rešitev**.
   * Pokaže razdelek **Vaša trenutna oddaja**, kjer piše ime datoteke:  
     **`Jančič Mitja – Normalizacija relacijske sheme (3NF).pdf`**
   * **Nal pove:** »Ne glede na to, kako je učenec poimenoval datoteko na svojem računalniku, jo strežnik samodejno shrani točno v formatu **`Priimek Ime – Naslov naloge`** z ustrezno končnico.«
   * **2. korak (Ponovna oddaja brez potrditve):** Na desni strani v obrazcu *Ponovna oddaja rešitve* ponovno izbere datoteko, **NE označi** potrditvenega polja in klikne **Povozi in oddaj novo verzijo**.
   * Pokaže rdeče opozorilo: *»Za povozitev obstoječe oddaje označi potrditev.«*
   * **Nal pove:** »Sistem prepreči nenamerno povozitev datoteke, dokler učenec tega izrecno ne potrdi.«
   * **3. korak (Ponovna oddaja s potrditvijo):** Ponovno izbere datoteko, **označi kljukico** *»Potrjujem, da želim povoziti prejšnjo oddano datoteko«* in klikne gumb za oddajo.
   * Pokaže zeleno sporočilo, da je bila prejšnja datoteka uspešno nadomeščena.

---

## 5. DEL: Varnostni preizkus in zaključek (Skupaj — 1 min)

### 💻 Kaj naredi Nal (še vedno prijavljen kot učenec `M.Jancic`):
1. V naslovno vrstico brskalnika ročno vpiše: `http://localhost/predmeti/` (administratorski URL) ali `http://localhost/ucitelj/` in pritisne Enter.
2. Na zaslonu se izpiše **`403 Forbidden`**.
   * **Nal pove:** »Če učenec poskusi dostopati do učiteljskega ali administratorskega pogleda, ga avtorizacijski sistem na strežniku takoj ustavi s statusom `403 Forbidden`.«

### 💻 Kaj naredi Mitja za konec:
1. Preklopi na **Terminal** in požene:
   ```powershell
   docker compose exec aplikacija python manage.py test
   ```
2. Počaka nekaj sekund, da se izpiše **`Ran 26 tests ... OK`**.
   * **Mitja pove:** »Za zagotavljanje zanesljivosti sva napisala 26 avtomatiziranih testov, ki preverijo vse tri vloge, M:N relacije, poimenovanje datotek, potrditev povozitve in zaščito pred nepooblaščenim dostopom. Vseh 26 testov je uspešnih. Hvala za pozornost, z veseljem odgovoriva na vaša vprašanja.«
