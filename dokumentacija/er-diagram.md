# ER diagram podatkovne baze

## Trenutna shema (implementirana do 3. tedna)

```mermaid
erDiagram
    PREDMET ||--o{ UCITELJ_PREDMET : ima
    UCITELJ ||--o{ UCITELJ_PREDMET : poucuje
    PREDMET ||--o{ UCENEC_PREDMET : ima
    UCENEC ||--o{ UCENEC_PREDMET : obiskuje

    PREDMET {
        int id PK
        string sifra UK
        string ime
        text opis
    }
    UCITELJ {
        int id PK
        string ime
        string priimek
        string email UK
    }
    UCENEC {
        int id PK
        string ime
        string priimek
        string email UK
    }
    UCITELJ_PREDMET {
        int id PK
        int ucitelj_id FK
        int predmet_id FK
    }
    UCENEC_PREDMET {
        int id PK
        int ucenec_id FK
        int predmet_id FK
    }
```

`UCITELJ_PREDMET` in `UCENEC_PREDMET` sta eksplicitni presečni (M:N) tabeli z
unikatno omejitvijo na paru tujih ključev (`(ucitelj_id, predmet_id)` in
`(ucenec_id, predmet_id)`), kar preprečuje podvojene povezave. Skupaj je to
**5 tabel**, kar presega zahtevanih najmanj 4.

## Razširitev v 4. tednu (prijava, gradiva, oddaje) – implementirano

```mermaid
erDiagram
    AUTH_USER ||--|| PROFIL : ima
    PROFIL }o--o| UCITELJ : povezan
    PROFIL }o--o| UCENEC : povezan
    PREDMET ||--o{ GRADIVO : vsebuje
    UCITELJ ||--o{ GRADIVO : nalozi
    PREDMET ||--o{ ODDAJA : prejme
    UCENEC ||--o{ ODDAJA : odda

    PROFIL {
        int id PK
        int uporabnik_id FK "OneToOne auth_user"
        string vloga "admin | ucitelj | ucenec"
        int ucitelj_id FK "null"
        int ucenec_id FK "null"
    }
    GRADIVO {
        int id PK
        int predmet_id FK
        string naslov
        string datoteka
        int nalozil_id FK "Ucitelj, null"
        datetime ustvarjeno
    }
    ODDAJA {
        int id PK
        int predmet_id FK
        int ucenec_id FK
        string naslov "naslov naloge"
        string datoteka "Priimek Ime – Naslov naloge.ext"
        datetime oddano
    }
```

Ključne odločitve:

- **`PROFIL`** povezuje Djangov vgrajeni model uporabnikov
  (`django.contrib.auth.User`, ki hrani zgoščeno geslo) z vlogo in – po potrebi –
  z zapisom `UCITELJ` ali `UCENEC`. Dve vrsti prijavljenih uporabnikov po
  zahtevi sta učitelj in učenec; administrator je tretja vloga
  (`is_staff`/`is_superuser`).
- **`ODDAJA`** je vezana neposredno na `PREDMET` (in ne na ločeno tabelo nalog),
  saj navodila od učitelja ne zahtevajo vnaprejšnjega ustvarjanja nalog –
  učenec odda nalogo z naslovom. Unikatna omejitev `(ucenec, predmet, naslov)`
  poskrbi, da ima ista naloga učenca eno oddajo; ponovna oddaja jo povozi (po
  potrditvi).
- Skupno je zdaj **8 tabel** (5 iz 3. tedna + `PROFIL`, `GRADIVO`, `ODDAJA`).
