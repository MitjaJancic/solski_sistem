# Pravila za delo v repozitoriju

## Veje
- `main` — stabilna različica; spremembe prihajajo izključno prek vlečnih zahtevkov (pull request)
- `develop` — integracijska veja za tekoče delo; sem se združujejo feature-veje
- `mitja`, `nal` — delovni veji posameznih članov (po potrebi tudi dodatne `feature/ime-funkcionalnosti` veje)

## Vlečni zahtevki (pull requests)
- vsak PR naj rešuje eno smiselno celoto (ena funkcionalnost/popravek)
- pred združitvijo v `develop` PR pregleda vsaj še en član skupine
- `main` se posodobi iz `develop` ob koncu tedna oz. ob mejnikih, ki jih potrdi mentor
- za sledenje napakam uporabljamo GitHub Issues

## Sporočila commit-ov
Kratek, jasen opis v nedoločniku/sedanjiku (npr. "dodaj CRUD za predmete", ne
"dodano CRUD za predmete včeraj").
