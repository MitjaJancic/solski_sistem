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

## Načrtovana razširitev (4. teden – prijava, gradiva, naloge)

```mermaid
erDiagram
    UCITELJ ||--o| AUTH_USER : prijava
    UCENEC ||--o| AUTH_USER : prijava
    PREDMET ||--o{ GRADIVO : vsebuje
    PREDMET ||--o{ NALOGA : vsebuje
    UCENEC ||--o{ ODDAJA : odda
    NALOGA ||--o{ ODDAJA : prejme

    GRADIVO {
        int id PK
        int predmet_id FK
        string naslov
        string datoteka
    }
    NALOGA {
        int id PK
        int predmet_id FK
        string naslov
        text opis
    }
    ODDAJA {
        int id PK
        int naloga_id FK
        int ucenec_id FK
        string datoteka
        datetime cas_oddaje
    }
```

`AUTH_USER` je Djangov vgrajeni model uporabnikov (`django.contrib.auth.User`);
`UCITELJ`/`UCENEC` bosta v 4. tednu dobila neobvezen `OneToOne` na ta model za
prijavo in avtorizacijo (dve vrsti uporabnikov: učitelj, učenec — administrator
je Djangov `is_staff`/`is_superuser`).
