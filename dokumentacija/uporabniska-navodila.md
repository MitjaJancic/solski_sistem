# Uporabniška navodila

Kratka navodila za vsako vlogo v sistemu Šolski IS. Do aplikacije dostopate prek
brskalnika (naslov vam sporoči šola/mentor; v razvoju `https://localhost`).

Prijava je na `/prijava/`, odjava prek gumba **Odjava** zgoraj desno.

---

## Administrator

Administrator upravlja šifrant predmetov, učiteljev in učencev.

1. **Prijava** z administratorskim računom → odpre se administratorski pregled
   s števci predmetov, učiteljev in učencev.
2. **Predmeti** (meni *Predmeti*):
   - *+ Nov predmet* → vnesi šifro (unikatna), ime, po želji opis → *Shrani*.
   - *Uredi* / *Izbriši* v vrstici tabele.
3. **Učitelji** (meni *Učitelji*):
   - *+ Nov učitelj* → ime, priimek, e-pošta (unikatna) in izbor predmetov,
     ki jih poučuje (izbereš lahko več).
4. **Učenci** (meni *Učenci*):
   - *+ Nov učenec* → ime, priimek, e-pošta in izbor predmetov (vsaj en).
5. Povezave učitelj–predmet in učenec–predmet urejaš na obrazcu učitelja/učenca.

> Namig: podatke je mogoče vnesti tudi neposredno v bazo (Adminer), a vsa
> opravila so na voljo tudi prek vmesnika.

---

## Učitelj

Učitelj skrbi za gradiva in pregleduje oddane naloge – **samo za predmete, ki
jih poučuje**.

1. **Prijava** z računom učitelja → odpre se *Moji predmeti*.
2. **Odpri predmet** (gumb *Odpri*) → vidiš seznam gradiv in oddanih nalog
   učencev.
3. **Naloži gradivo**: gumb *Naloži gradivo* → izberi predmet (na voljo so le
   tvoji), vnesi naslov in datoteko → *Naloži*.
4. **Izbriši gradivo**: v tabeli gradiv klikni *Izbriši* in potrdi.
5. **Pregled oddaj**: v tabeli *Oddane naloge učencev* klikni *Prenesi* za
   posamezno oddajo.

> Do predmetov, ki jih ne poučuješ, nimaš dostopa (sistem prepreči vpogled).

---

## Učenec

Učenec ureja svoj profil in predmete, prebira gradiva in oddaja naloge.

1. **Registracija**: na `/registracija/` ustvari račun (uporabniško ime, ime,
   priimek, e-pošta, geslo). Po registraciji te sistem prijavi.
2. **Izbira predmetov**: meni *Moji predmeti* → označi predmete, ki jih
   obiskuješ (vsaj enega) → *Shrani*.
3. **Profil**: *Uredi profil* → popravi ime, priimek, e-pošto.
4. **Gradiva**: na *Domov* klikni *Gradiva* pri predmetu → *Prenesi* za
   posamezno gradivo.
5. **Oddaja naloge**: *Oddaj nalogo* → izberi predmet (na voljo so le tvoji),
   vpiši naslov naloge in izberi datoteko → *Oddaj*.
   - Datoteka se shrani pod imenom **»Priimek Ime – Naslov naloge«** z ustrezno
     končnico.
   - Če za isto nalogo (isti predmet in naslov) že obstaja oddaja, moraš za
     povozitev prejšnje datoteke **označiti potrditev** – šele nato jo nova
     povozi.
6. **Moje oddaje**: meni *Moje oddaje* → pregled in prenos svojih oddaj.
