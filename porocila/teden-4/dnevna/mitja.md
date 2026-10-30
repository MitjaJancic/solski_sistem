# Dnevna poročila – Mitja Jančič (vzdrževalec IS + razvijalec)

## 2026-10-06

**Kaj sem delal:**
- vzpostavitev zaščite naloženih datotek na ravni spletnega strežnika: v Nginx konfiguraciji smo odstranili javno mapo `/media/`, kar pomeni, da datoteke niso neposredno dostopne prek statičnih URL-jev
- priprava zaščitenega toka za prenos gradiv in oddanih nalog prek Djangovega pogleda z avtorizacijo (dostop samo za prijavljene upravičene uporabnike)
- preverjanje varnosti hranjenja gesel v MariaDB bazi: potrditev, da Django uporablja zgoščevanje z algoritmom PBKDF2-SHA256 z naključno soljo in da gesla niso shranjena v berljivi obliki

**Kaj sem dokončal:**
- celovita zaščita naloženih datotek in potrjeno varno zgoščevanje vseh uporabniških gesel

**Kaj mi ni uspelo in zakaj:**
- vse je teklo po načrtu.

## 2026-10-08

**Kaj sem delal:**
- načrtovanje in izdelava skripte za avtomatizirano izdelavo varnostnih kopij podatkovne baze (`scripts/varnostna-kopija.sh`)
- uporaba orodja `mariadb-dump` znotraj MariaDB vsebnika, stiskanje arhiva z `gzip` in shranjevanje v mapo `backup/` na gostitelju
- implementacija rotacije varnostnih kopij (ohranjanje zadnjih 7 varnostnih kopij, starejše se samodejno zbrišejo)
- priprava navodil za periodični zagon prek sistemskega opravila (cron / Task Scheduler)

**Kaj sem dokončal:**
- zanesljiva in preizkušena skripta za varnostne kopije z rotacijo

**Kaj mi ni uspelo in zakaj:**
- pri prvem testu je bilo treba urediti pravice pisanja v mapo `backup/`, kar je bilo takoj popravljeno.

## 2026-10-09

**Kaj sem delal:**
- vzpostavitev rešitve za javno dostopnost aplikacije brez zapletenega odpiranja portov na domačem usmerjevalniku: vključitev Cloudflare tunela (`tunel` vsebnik z uradno sliko `cloudflare/cloudflared`) v `docker-compose.yml`
- konfiguracija tunela, ki Nginx promet posreduje na internetno domeno z veljavnim javnim TLS certifikatom
- izdelava skripte `scripts/pokazi-javni-url.ps1` in `scripts/pokazi-javni-url.sh` za enostaven izpis trenutnega javnega naslova

**Kaj sem dokončal:**
- aplikacija je stabilno dosegljiva na javni domeni preko HTTPS, testirana dostopnost z mobilnega omrežja

**Kaj mi ni uspelo in zakaj:**
- brezplačni hitri tuneli ob ponovnem zagonu vsebnika zamenjajo poddomeno, kar je rešeno z avtomatsko skripto za pridobivanje URL-ja iz dnevniških zapisov.
