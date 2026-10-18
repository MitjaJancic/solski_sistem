# Tedensko poročilo – teden 6 (Zaključno testiranje, predstavitev in oddaja)

**Povzetek napredka:**

- **Zaključni pregled kode (razvijalca):** pregled izvorne kode, preverjanje z
  `pyflakes` (brez neuporabljenih uvozov/mrtve kode), brez testnih/nepotrebnih
  ostankov v aplikaciji.
- **Produkcijska sestava (vzdrževalec IS):** aplikacija se v produkciji streže z
  **gunicorn**, statične datoteke prek **WhiteNoise** (`collectstatic` ob
  zagonu). Razvojne dodatke (Adminer, priklop kode, `runserver`) smo prestavili
  v `docker-compose.override.yml`, tako da produkcijska sestava ostane čista
  (`docker compose -f docker-compose.yml up`). V produkciji (`DJANGO_DEBUG=0`)
  se vklopijo varni piškotki in HSTS.
- **Zadnja preverba stabilnosti in varnostnih kopij:** kontrolni seznam v
  [`dokumentacija/streznik.md`](../../dokumentacija/streznik.md) (8. poglavje).
- **Zaključno testiranje:** vseh **26 avtomatiziranih testov** je uspešnih;
  ročni testni primeri (glej `testni-primeri.md`) so preverjeni.
- **Predstavitev:** pripravljeni diapozitivi
  ([`predstavitev/predstavitev.md`](../../predstavitev/predstavitev.md)) in
  scenarij praktične demonstracije
  ([`predstavitev/demo-scenarij.md`](../../predstavitev/demo-scenarij.md)).
- **Ureditev repozitorija:** urejen README, končna različica označena z oznako
  (tag) `v1.0`.

**Zaključno poročilo skupine:** [`porocila/zakljucno-porocilo.md`](../zakljucno-porocilo.md)
(povzetek po tednih, izzivi in rešitve, delitev dela; s povezavo do repozitorija
in delujoče aplikacije).

**Manjka za oddajo:** vpis konkretnih povezav (repozitorij in URL javne domene)
v zaključno poročilo in na zadnji diapozitiv.
