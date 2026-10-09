# Tedensko poročilo – teden 5 (Testiranje, oblikovanje in dokumentacija)

**Povzetek napredka:** teden je bil namenjen sistematičnemu testiranju vseh treh
pogledov, odpravljanju napak, izboljšavam uporabniškega vmesnika ter
dokončanju dokumentacije in uporabniških navodil.

- **Sistematično testiranje:** pripravljen je seznam testnih primerov za vse tri
  poglede z opisom, pričakovanim in dejanskim rezultatom ter statusom
  ([`dokumentacija/testni-primeri.md`](../../dokumentacija/testni-primeri.md)).
  Večina primerov je pokrita z avtomatiziranimi testi
  ([`administracija/tests.py`](../../aplikacija/administracija/tests.py) in
  [`portal/tests.py`](../../aplikacija/portal/tests.py)). Zadnji zagon:
  **26 testov, vseh 26 uspešnih.**

  ```bash
  cd aplikacija
  DJANGO_TEST_SQLITE=1 python manage.py test
  ```

- **Izboljšave oblikovanja (odzivnost, doslednost):** tabele so ovite v
  `.table-responsive` (na telefonu vodoravno drsijo namesto preliva), dodana je
  noga (footer) s postavitvijo, ki jo pritisne na dno strani, poenoteni so
  slogi kartic in gumbov (`slog.css`).

- **Dokumentacija (vzdrževalec IS):** dokončana tehnična dokumentacija –
  dodan je diagram arhitekture in opis celotne rešitve
  ([`dokumentacija/arhitektura.md`](../../dokumentacija/arhitektura.md));
  dopolnjena sta `streznik.md` in `er-diagram.md`.

- **Uporabniška navodila (razvijalca):** pripravljena kratka navodila za vsako
  vlogo (administrator, učitelj, učenec)
  ([`dokumentacija/uporabniska-navodila.md`](../../dokumentacija/uporabniska-navodila.md)).

**Odkrite in odpravljene napake:** beležimo jih prek GitHub Issues; povzetek:

| BUG-ID | Opis | Resnost | Rešitev | Status |
|--------|------|---------|---------|--------|
| BUG-01 | Sporočila o napakah se izpišejo brez oblikovanja (Django oznaka `error` ni Bootstrap razred `danger`) | srednja | `MESSAGE_TAGS = {ERROR: "danger"}` v `settings.py`; dodan regresijski test | odpravljeno |
| BUG-02 | Tabele se na ozkih zaslonih (telefon) prelivajo čez rob strani | nizka | Ovoj `.table-responsive` okoli vseh tabel s seznami | odpravljeno |

> Povezava do GitHub Issues: _<vstavi povezavo na `Issues` v repozitoriju>_

**Stabilnost:** po odpravi zgornjih napak aplikacija deluje stabilno, brez
kritičnih napak; vsi avtomatizirani testi so uspešni.

**Manjka za dokončno oddajo tega tedna:** vpis konkretnih povezav na GitHub
Issues in morebitni zaslonski posnetki popravkov za mentorja.

**Načrt za naslednji teden (teden 6):** zaključno testiranje na javni domeni,
priprava predstavitve (diapozitivi + demonstracija), zaključno poročilo skupine,
označitev končne različice (tag/release) in ureditev repozitorija.
