"""Ustvari obsežne demo testne podatke za vse zmogljivosti spletne strani:
- uporabniški računi (admin, ucitelj1..5, ucenec1..5)
- učna gradiva z resničnimi vzorčnimi datotekami (PDF/TXT) za prenos
- naloge z različnimi roki (potekle, bližajoče se, aktivne)
- oddaje nalog (ocenjene z ocenami 1-5, v pregledu, pravočasne, prepozne)
- obvestila z rdečo značko neprebranih obvestil za učence in učitelje

Uporaba:
    python manage.py seed_uporabniki
"""
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from administracija.models import Predmet, Ucenec, Ucitelj, UcenecPredmet, UciteljPredmet
from portal.models import Gradivo, Naloga, Obvestilo, Oddaja, Profil

GESLO_ADMIN = "Admin123!"
GESLO_UCITELJ = "Ucitelj123!"
GESLO_UCENEC = "Ucenec123!"


def ustvari_vzorcno_datoteko(ime, vsebina_tekst):
    """Vrne ContentFile z enostavno vsebino za testiranje prenosa datotek."""
    glava = f"--- Šolski IS: {ime} ---\n\n"
    podatki = (glava + vsebina_tekst).encode("utf-8")
    return ContentFile(podatki, name=ime)


class Command(BaseCommand):
    help = "Ustvari celovite testne podatke za vse zmogljivosti sistema (uporabniki, gradiva, naloge, ocene, obvestila)."

    @transaction.atomic
    def handle(self, *args, **options):
        zdaj = timezone.now()

        # -------------------------------------------------------------
        # 1. UPORABNIŠKI RAČUNI
        # -------------------------------------------------------------
        # Administrator
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@solski-is.si", "is_staff": True, "is_superuser": True},
        )
        admin.set_password(GESLO_ADMIN)
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        Profil.objects.update_or_create(uporabnik=admin, defaults={"vloga": Profil.Vloga.ADMIN})
        self.stdout.write(self.style.SUCCESS(f"Administrator: admin / {GESLO_ADMIN}"))

        # Pridobimo ali ustvarimo predmete, če jih še ni
        predmeti_seznam = list(Predmet.objects.all())
        if not predmeti_seznam:
            self.stdout.write(self.style.WARNING("Predmeti še niso bili vneseni, zaženite najprej seed_podatki."))
            return

        # Učitelji (prvih 5)
        ucitelji = list(Ucitelj.objects.all()[:5])
        ucitelji_racuni = []
        for i, ucitelj in enumerate(ucitelji, start=1):
            uporabnik, _ = User.objects.get_or_create(
                username=f"ucitelj{i}", defaults={"email": ucitelj.email}
            )
            uporabnik.set_password(GESLO_UCITELJ)
            uporabnik.save()
            Profil.objects.update_or_create(
                uporabnik=uporabnik,
                defaults={"vloga": Profil.Vloga.UCITELJ, "ucitelj": ucitelj},
            )
            ucitelji_racuni.append((uporabnik, ucitelj))
            self.stdout.write(self.style.SUCCESS(f"Učitelj: ucitelj{i} / {GESLO_UCITELJ} -> {ucitelj}"))

        # Učenci (prvih 5)
        ucenci = list(Ucenec.objects.all()[:5])
        ucenci_racuni = []
        for i, ucenec in enumerate(ucenci, start=1):
            uporabnik, _ = User.objects.get_or_create(
                username=f"ucenec{i}", defaults={"email": ucenec.email}
            )
            uporabnik.set_password(GESLO_UCENEC)
            uporabnik.save()
            Profil.objects.update_or_create(
                uporabnik=uporabnik,
                defaults={"vloga": Profil.Vloga.UCENEC, "ucenec": ucenec},
            )
            ucenci_racuni.append((uporabnik, ucenec))
            self.stdout.write(self.style.SUCCESS(f"Učenec: ucenec{i} / {GESLO_UCENEC} -> {ucenec} ({ucenec.email})"))

        # Zagotovimo, da imajo prvi učenci vpisane predmete prvih učiteljev
        ucitelj1 = ucitelji[0] if len(ucitelji) > 0 else None
        ucitelj2 = ucitelji[1] if len(ucitelji) > 1 else None
        ucitelj3 = ucitelji[2] if len(ucitelji) > 2 else None

        # Poskrbimo, da imata ucitelj1 in ucitelj2 dodeljene predmete
        predmet_mat = Predmet.objects.filter(sifra="MAT").first() or predmeti_seznam[0]
        predmet_fiz = Predmet.objects.filter(sifra="FIZ").first() or predmeti_seznam[1]
        predmet_slo = Predmet.objects.filter(sifra="SLO").first() or predmeti_seznam[2]
        predmet_inf = Predmet.objects.filter(sifra="INF").first() or predmeti_seznam[3]

        if ucitelj1:
            ucitelj1.predmeti.add(predmet_mat, predmet_fiz)
        if ucitelj2:
            ucitelj2.predmeti.add(predmet_slo)
        if ucitelj3:
            ucitelj3.predmeti.add(predmet_inf)

        # Učencem 1..5 vpišemo te predmete
        for ucenec in ucenci:
            ucenec.predmeti.add(predmet_mat, predmet_fiz, predmet_slo, predmet_inf)

        # -------------------------------------------------------------
        # 2. UČNA GRADIVA (z dejansko prenosljivimi datotekami)
        # -------------------------------------------------------------
        gradiva_podatki = [
            (predmet_mat, ucitelj1, "Zapiski – Kvadratna funkcija in parabola.pdf", "Vzorčno učno gradivo za razlago kvadratne funkcije, ničel ter temena parabole."),
            (predmet_mat, ucitelj1, "Zbirka vaj – Sistemi linearnih enačb.pdf", "Rešene vaje s postopki zamenjave in metodo nasprotnih koeficientov."),
            (predmet_fiz, ucitelj1, "Laboratorijska navodila – Merjenje pospeška.pdf", "Navodila za izvedbo fizikalnega eksperimenta in obdelavo meritev."),
            (predmet_slo, ucitelj2, "Slovenska romantika – France Prešeren.pdf", "Učna enota s poezijo in analizo Krsta pri Savici."),
            (predmet_inf, ucitelj3, "Navodila za vaje – Relacijske baze in SQL.pdf", "Priročnik za osnove SELECT stavkov, združevanj (JOIN) in tabel."),
        ]

        st_gradiv = 0
        for predmet, ucitelj, naslov, vsebina in gradiva_podatki:
            if not Gradivo.objects.filter(predmet=predmet, naslov=naslov).exists():
                gradivo = Gradivo(predmet=predmet, nalozil=ucitelj, naslov=naslov)
                gradivo.datoteka.save(naslov, ustvari_vzorcno_datoteko(naslov, vsebina), save=True)
                st_gradiv += 1
        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih {st_gradiv} učnih gradiv z veljavnimi datotekami."))

        # -------------------------------------------------------------
        # 3. NALOGE Z RAZLIČNIMI ROKI
        # -------------------------------------------------------------
        # 1. Potekla naloga (rok 5 dni nazaj)
        naloga_potekla, _ = Naloga.objects.get_or_create(
            predmet=predmet_mat,
            naslov=f"1. domača naloga: Kvadratne enačbe ({predmet_mat.sifra})",
            defaults={
                "opis": "Rešite naloge 1 do 10 na strani 45. Natančno izpišite postopek in diskriminanto.",
                "rok": zdaj - timedelta(days=5),
                "ustvaril": ucitelj1,
            },
        )

        # 2. Bližajoča se naloga (rok jutri)
        naloga_nujna, _ = Naloga.objects.get_or_create(
            predmet=predmet_fiz,
            naslov=f"Poročilo: Merjenje gravitacijskega pospeška ({predmet_fiz.sifra})",
            defaults={
                "opis": "Oddajte poročilo o meritvah nihanja nitnega nihala vključno z oceno napake.",
                "rok": zdaj + timedelta(days=1, hours=4),
                "ustvaril": ucitelj1,
            },
        )

        # 3. Odprta naloga (rok čez 7 dni)
        naloga_aktivna, _ = Naloga.objects.get_or_create(
            predmet=predmet_slo,
            naslov=f"Esej: Romantika na Slovenskem ({predmet_slo.sifra})",
            defaults={
                "opis": "Napišite primerjalni esej ob Prešernovem Krstu pri Savici. Obseg 600 do 800 besed.",
                "rok": zdaj + timedelta(days=7),
                "ustvaril": ucitelj2,
            },
        )

        # 4. Seminarska naloga (rok čez 14 dni)
        naloga_seminarska, _ = Naloga.objects.get_or_create(
            predmet=predmet_inf,
            naslov=f"Projekt: Načrtovanje podatkovne baze ({predmet_inf.sifra})",
            defaults={
                "opis": "Pripravite ER diagram in SQL stavke za model šolskega informacijskega sistema.",
                "rok": zdaj + timedelta(days=14),
                "ustvaril": ucitelj3,
            },
        )
        self.stdout.write(self.style.SUCCESS("Ustvarjene 4 raznolike naloge (pretečena, bližajoča, aktivna, projekt)."))

        # -------------------------------------------------------------
        # 4. ODDAJE NALOG IN OCENJEVANJE
        # -------------------------------------------------------------
        # Oddaje za nalogo 1 (potekla naloga iz matematike)
        oddaje_podatki = [
            # (naloga, ucenec, prepozno, ocena, komentar, vsebina)
            (
                naloga_potekla,
                ucenci[0],  # ucenec1
                False,
                5,
                "Odlično rešeno! Vsi postopki so pregledni, ničle funkcije in grafi so brezhibni.",
                "Resitev naloge 1 - kvadratne enacbe. x1 = 2, x2 = -3. Diskriminanta D = 25.",
            ),
            (
                naloga_potekla,
                ucenci[1],  # ucenec2
                False,
                4,
                "Zelo dobro. Pri 4. nalogi pazi na predznak pred oklepajem.",
                "Resitev nalog iz matematike. Vse naloge resene.",
            ),
            (
                naloga_potekla,
                ucenci[2],  # ucenec3
                True,  # prepozno!
                3,
                "Naloga je bila oddana po preteku roka. Vsebina je sicer ustrezna, ocena znižana za eno stopnjo.",
                "Resitve vaj iz matematike (oddano z zamudo zaradi tehnicnih tezav).",
            ),
            (
                naloga_potekla,
                ucenci[3],  # ucenec4
                False,
                None,  # NEOCENJENO - caka na pregled ucitelja!
                "",
                "Resitev domace naloge - caka na pregled.",
            ),
            (
                naloga_potekla,
                ucenci[4],  # ucenec5
                True,  # prepozno in NEOCENJENO!
                None,
                "",
                "Pozna oddaja naloge iz matematike.",
            ),
            # Oddaja za nalogo 2 (fizika, ucenec1)
            (
                naloga_nujna,
                ucenci[0],  # ucenec1
                False,
                None,  # Neocenjeno, caka na ucitelja
                "",
                "Porocilo o meritvah gravitacijskega pospeska: g = 9.81 m/s^2.",
            ),
            # Oddaja za nalogo 3 (slovenscina, ucenec2)
            (
                naloga_aktivna,
                ucenci[1],  # ucenec2
                False,
                5,
                "Izjemen esej z globokim razumevanjem romantičnega svetobolja in Prešernove poetike.",
                "Primerjalni esej: Romantika na Slovenskem in evropski vplivi.",
            ),
        ]

        st_oddaj = 0
        for naloga, ucenec, prepozno, ocena, komentar, vsebina in oddaje_podatki:
            ime_datoteke = f"{ucenec.priimek} {ucenec.ime} – {naloga.naslov}.pdf"
            oddaja, ustvarjena = Oddaja.objects.get_or_create(
                naloga=naloga,
                ucenec=ucenec,
                defaults={
                    "prepozno": prepozno,
                    "ocena": ocena,
                    "komentar": komentar,
                    "ocenjeno": zdaj - timedelta(days=1) if ocena else None,
                },
            )
            if ustvarjena:
                oddaja.datoteka.save(ime_datoteke, ustvari_vzorcno_datoteko(ime_datoteke, vsebina), save=True)
                st_oddaj += 1
            else:
                oddaja.prepozno = prepozno
                oddaja.ocena = ocena
                oddaja.komentar = komentar
                oddaja.ocenjeno = zdaj - timedelta(days=1) if ocena else None
                oddaja.save()

        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih/posodobljenih {len(oddaje_podatki)} oddaj z ocenami in komentarji."))

        # -------------------------------------------------------------
        # 5. OBVESTILA (Center za obvestila)
        # -------------------------------------------------------------
        # Za ucenec1 (račun Luka Kovač)
        u1_user = ucenci_racuni[0][0]
        Obvestilo.objects.filter(prejemnik=u1_user).delete()
        Obvestilo.objects.create(
            prejemnik=u1_user,
            besedilo="Vaša oddaja pri nalogi '1. domača naloga: Kvadratne enačbe' je bila ocenjena z oceno 5.",
            povezava=f"/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> rdeča značka 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u1_user,
            besedilo=f"Prof. {ucitelj3.priimek} je objavil novo nalogo: 'Projekt: Načrtovanje podatkovne baze'.",
            povezava=f"/portal/ucenec/naloga/{naloga_seminarska.pk}/",
            prebrano=False,  # Neprebrano -> rdeča značka 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u1_user,
            besedilo="Uspešno ste oddali nalogo 'Poročilo: Merjenje gravitacijskega pospeška'.",
            povezava=f"/portal/ucenec/naloge/",
            prebrano=True,
        )

        # Za ucenec2
        u2_user = ucenci_racuni[1][0]
        Obvestilo.objects.filter(prejemnik=u2_user).delete()
        Obvestilo.objects.create(
            prejemnik=u2_user,
            besedilo="Vaš esej pri Slovenščini je bil ocenjen z oceno 5. Odlično delo!",
            povezava=f"/portal/ucenec/naloge/",
            prebrano=False,
        )
        Obvestilo.objects.create(
            prejemnik=u2_user,
            besedilo="Opozorilo o roku: Rok za oddajo poročila pri Fiziki poteče jutri!",
            povezava=f"/portal/ucenec/naloga/{naloga_nujna.pk}/",
            prebrano=True,
        )

        # Za ucitelj1 (račun Janez Novak)
        t1_user = ucitelji_racuni[0][0]
        Obvestilo.objects.filter(prejemnik=t1_user).delete()
        Obvestilo.objects.create(
            prejemnik=t1_user,
            besedilo=f"Nova oddaja naloge: {ucenci[3].priimek} {ucenci[3].ime} je oddal rešitev pri nalogi '1. domača naloga'.",
            povezava=f"/portal/ucitelj/naloga/{naloga_potekla.pk}/",
            prebrano=False,  # Neprebrano!
        )
        Obvestilo.objects.create(
            prejemnik=t1_user,
            besedilo=f"Nova oddaja naloge: {ucenci[0].priimek} {ucenci[0].ime} je oddal poročilo pri Fiziki.",
            povezava=f"/portal/ucitelj/naloga/{naloga_nujna.pk}/",
            prebrano=False,  # Neprebrano!
        )
        Obvestilo.objects.create(
            prejemnik=t1_user,
            besedilo=f"Pozna oddaja: {ucenci[4].priimek} {ucenci[4].ime} je z zamudo oddal nalogo iz matematike.",
            povezava=f"/portal/ucitelj/naloga/{naloga_potekla.pk}/",
            prebrano=True,
        )

        self.stdout.write(self.style.SUCCESS("Center za obvestila napolnjen s testnimi obvestili (prebrana in neprebrana)."))
        self.stdout.write(self.style.SUCCESS("--- TESTNI PODATKI ZA VSE ZMOGLJIVOSTI SISTEMA SO PRIPRAVLJENI ---"))
