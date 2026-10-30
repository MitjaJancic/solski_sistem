# Dnevna poročila – Mitja Jančič (vzdrževalec IS + razvijalec)

## 2026-09-29

**Kaj sem delal:**
- natančna konfiguracija Nginx spletnega strežnika kot obrnjenega posrednika v `nginx/nginx.conf`
- konfiguracija preusmeritve celotnega nešifriranega prometa iz vrat 80 (HTTP) na varna vrata 443 (HTTPS) z odzivno kodo 301
- nastavitev posredovanja pravih odjemalčevih glav (`X-Forwarded-For`, `X-Forwarded-Proto`, `Host`) v aplikacijski vsebnik
- zagotovitev izolacije: Django vsebnik je dosegljiv izključno znotraj Docker omrežja (samo `expose: 8000`, brez neposrednega mapiranja na gostiteljski sistem)

**Kaj sem dokončal:**
- varno delujoč obrnjeni posrednik Nginx z lokalnim samopodpisanim certifikatom

**Kaj mi ni uspelo in zakaj:**
- pri lokalnem testiranju brskalnik prikaže varnostno opozorilo o nepreverjenem izdajatelju certifikata, kar je za samopodpisana potrdila v razvojnem okolju povsem običajno.

## 2026-10-01

**Kaj sem delal:**
- priprava podrobne dokumentacije namestitve in konfiguracije strežnika v `dokumentacija/streznik.md`
- opis delovanja obrnjenega posrednika, konfiguracije TLS potrdila ter postopka za zagon celotnega sistema
- testiranje samodejnega ponovnega zagona vsebnikov ob morebitnem izpadu (`restart: unless-stopped`)

**Kaj sem dokončal:**
- prvo in drugo poglavje strežniške dokumentacije z natančnimi navodili za vzdrževanje

**Kaj mi ni uspelo in zakaj:**
- vse je potekalo brez težav.

## 2026-10-02

**Kaj sem delal:**
- integracijsko testiranje administratorskega pogleda prek Nginxa na `https://localhost`
- preverjanje pravilnosti vseh odzivnih kod prek orodja `curl -k` za poti `/predmeti/`, `/ucitelji/`, `/ucenci/`
- pregled Nginx dnevniških zapisov (`access.log` in `error.log`) za zagotovitev, da ni neželenih napak ob posredovanju zahtevkov

**Kaj sem dokončal:**
- administratorski del aplikacije stabilno teče za Nginx posrednikom preko varne HTTPS povezave

**Kaj mi ni uspelo in zakaj:**
- vse predvidene zahteve 3. tedna so v celoti izpolnjene.
