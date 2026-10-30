# Dnevna poročila – Mitja Jančič (vzdrževalec IS + razvijalec)

## 2026-10-13

**Kaj sem delal:**
- izdelava podrobnega diagrama arhitekture sistema v Mermaid formatu (`dokumentacija/arhitektura.md`)
- vizualizacija povezav med uporabnikom, internetom, Cloudflare tunelom, Nginx posrednikom, Django aplikacijo in MariaDB bazo podatkov z obstojnimi volumni
- posodobitev in razširitev dokumentacije strežnika (`dokumentacija/streznik.md`) ter ER diagrama (`dokumentacija/er-diagram.md`)

**Kaj sem dokončal:**
- celovita tehnična dokumentacija arhitekture in strežniške infrastrukture

**Kaj mi ni uspelo in zakaj:**
- vse je teklo po načrtu.

## 2026-10-15

**Kaj sem delal:**
- skupno sistematično testiranje delovanja celotnega sistema z Nalom na podlagi pripravljenega seznama testnih primerov (`dokumentacija/testni-primeri.md`)
- testiranje odzivnosti spletnega vmesnika na različnih ločljivostih zaslona (namizni računalnik, prenosnik, tablica, pametni telefon)
- beleženje odkritih napak prek GitHub Issues:
  - **BUG-01**: Sporočila o napakah se izpišejo brez primernega Bootstrap oblikovanja (oznaka `error` ni `danger`)
  - **BUG-02**: Široke tabele se na majhnih zaslonih prelivajo čez rob strani

**Kaj sem dokončal:**
- vsi odkriti problemi so bili natančno dokumentirani in odprti kot sledljivi Issues na GitHubu

**Kaj mi ni uspelo in zakaj:**
- vse je bilo uspešno zabeleženo.

## 2026-10-16

**Kaj sem delal:**
- odprava napake **BUG-01**: v `aplikacija/solski_sistem/settings.py` smo dodali nastavitev `MESSAGE_TAGS = {messages.ERROR: "danger"}`, s čimer se Djangova opozorila o napakah pravilno obarvajo rdeče v Bootstrapu
- dodajanje regresijskega testa za preverjanje pravilnih oznak sporočil
- priprava zbirnega tedenskega poročila za 5. teden

**Kaj sem dokončal:**
- hrošč BUG-01 uspešno odpravljen in zaprt na GitHubu, aplikacija deluje zanesljivo

**Kaj mi ni uspelo in zakaj:**
- vse načrtovano za 5. teden je bilo pravočasno zaključeno.
