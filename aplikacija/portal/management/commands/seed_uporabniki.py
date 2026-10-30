"""Ustvari obsežne testne podatke z dejanskimi imeni in priimki:
- Učitelji: Matic Holobar (mentor), Janez Novak, Maja Horvat, Peter Krajnc, Ana Kovačič ...
- Učenci: Mitja Jančič, Nal Dobravc, Luka Kovač, Ana Novak, Jan Zupančič ...
- Dejanska učna gradiva, naloge, oddaje in ocenjevanje s povratnimi informacijami
- Obvestila z rdečo značko neprebranih obvestil

Uporaba:
    python manage.py seed_podatki
    python manage.py seed_uporabniki
"""
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from administracija.models import Predmet, Ucenec, Ucitelj
from portal.models import Gradivo, Naloga, Obvestilo, Oddaja, Profil

GESLO_ADMIN = "Admin123!"
GESLO_UCITELJ = "Ucitelj123!"
GESLO_UCENEC = "Ucenec123!"


def ustvari_vzorcno_datoteko(ime, vsebina_tekst):
    """Vrne ContentFile za fizično shrambo datoteke ob testiranju prenosa."""
    glava = f"--- Šolski IS: {ime} ---\n\n"
    podatki = (glava + vsebina_tekst).encode("utf-8")
    return ContentFile(podatki, name=ime)


class Command(BaseCommand):
    help = "Ustvari testne račune z dejanskimi imeni (Matic Holobar, Mitja Jančič, Nal Dobravc) ter gradiva, naloge in ocene."

    @transaction.atomic
    def handle(self, *args, **options):
        zdaj = timezone.now()

        # Počistimo stare demo profile in uporabnike zaradi OneToOne edinstvenosti
        Profil.objects.all().delete()
        User.objects.filter(username__startswith="ucitelj").delete()
        User.objects.filter(username__startswith="ucenec").delete()

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

        # Pridobimo predmete
        predmeti_seznam = list(Predmet.objects.all())
        if not predmeti_seznam:
            self.stdout.write(self.style.WARNING("Najprej zaženite seed_podatki."))
            return

        predmet_inf = Predmet.objects.filter(sifra="INF").first() or predmeti_seznam[0]
        predmet_mat = Predmet.objects.filter(sifra="MAT").first() or predmeti_seznam[1]
        predmet_fiz = Predmet.objects.filter(sifra="FIZ").first() or predmeti_seznam[2]
        predmet_slo = Predmet.objects.filter(sifra="SLO").first() or predmeti_seznam[3]
        predmet_ang = Predmet.objects.filter(sifra="ANG").first() or predmeti_seznam[4]

        # Ciljni učitelji z dejanskimi imeni
        ciljni_ucitelji = [
            ("Matic", "Holobar"),
            ("Janez", "Novak"),
            ("Maja", "Horvat"),
            ("Peter", "Krajnc"),
            ("Ana", "Kovačič"),
        ]
        ucitelji = []
        for ime, priimek in ciljni_ucitelji:
            u = Ucitelj.objects.filter(ime=ime, priimek=priimek).first()
            if not u:
                u = Ucitelj.objects.create(ime=ime, priimek=priimek, email=f"{ime.lower()}.{priimek.lower()}@solski-is.si")
            ucitelji.append(u)

        ucitelji_racuni = []
        for i, ucitelj in enumerate(ucitelji, start=1):
            uporabnik, _ = User.objects.get_or_create(
                username=f"ucitelj{i}", defaults={"email": ucitelj.email}
            )
            uporabnik.set_password(GESLO_UCITELJ)
            uporabnik.email = ucitelj.email
            uporabnik.save()
            Profil.objects.update_or_create(
                uporabnik=uporabnik,
                defaults={"vloga": Profil.Vloga.UCITELJ, "ucitelj": ucitelj},
            )
            ucitelji_racuni.append((uporabnik, ucitelj))
            self.stdout.write(self.style.SUCCESS(f"Učitelj: ucitelj{i} / {GESLO_UCITELJ} -> {ucitelj.ime} {ucitelj.priimek}"))

        # Ciljni učenci z dejanskimi imeni
        ciljni_ucenci = [
            ("Mitja", "Jančič"),
            ("Nal", "Dobravc"),
            ("Luka", "Kovač"),
            ("Ana", "Novak"),
            ("Jan", "Zupančič"),
        ]
        ucenci = []
        for ime, priimek in ciljni_ucenci:
            u = Ucenec.objects.filter(ime=ime, priimek=priimek).first()
            if not u:
                u = Ucenec.objects.create(ime=ime, priimek=priimek, email=f"{ime.lower()}.{priimek.lower()}@dijaki.solski-is.si")
            ucenci.append(u)

        ucenci_racuni = []
        for i, ucenec in enumerate(ucenci, start=1):
            uporabnik, _ = User.objects.get_or_create(
                username=f"ucenec{i}", defaults={"email": ucenec.email}
            )
            uporabnik.set_password(GESLO_UCENEC)
            uporabnik.email = ucenec.email
            uporabnik.save()
            Profil.objects.update_or_create(
                uporabnik=uporabnik,
                defaults={"vloga": Profil.Vloga.UCENEC, "ucenec": ucenec},
            )
            ucenci_racuni.append((uporabnik, ucenec))
            self.stdout.write(self.style.SUCCESS(f"Učenec: ucenec{i} / {GESLO_UCENEC} -> {ucenec.ime} {ucenec.priimek}"))

        # Zagotovimo pravilne predmete za učitelje
        mentor_holobar = ucitelji[0]  # Matic Holobar
        prof_novak = ucitelji[1]      # Janez Novak
        prof_horvat = ucitelji[2]     # Maja Horvat
        prof_krajnc = ucitelji[3]     # Peter Krajnc

        mentor_holobar.predmeti.add(predmet_inf, predmet_mat)
        prof_novak.predmeti.add(predmet_mat, predmet_fiz)
        prof_horvat.predmeti.add(predmet_slo)
        prof_krajnc.predmeti.add(predmet_inf, predmet_fiz)

        # Zagotovimo vpisane predmete za dijake
        dijak_mitja = ucenci[0]  # Mitja Jančič
        dijak_nal = ucenci[1]    # Nal Dobravc

        dijak_mitja.predmeti.add(predmet_inf, predmet_mat, predmet_fiz, predmet_slo, predmet_ang)
        dijak_nal.predmeti.add(predmet_inf, predmet_mat, predmet_slo, predmet_fiz)
        for u in ucenci[2:]:
            u.predmeti.add(predmet_inf, predmet_mat, predmet_fiz, predmet_slo)

        # -------------------------------------------------------------
        # 2. UČNA GRADIVA
        # -------------------------------------------------------------
        gradiva_podatki = [
            (predmet_inf, mentor_holobar, "Priročnik – Relacijske podatkovne baze in SQL.pdf", "Vzorčno učno gradivo za relacijske modele, tabele, primarne in tuje ključe ter poizvedbe SQL. Avtor: Matic Holobar."),
            (predmet_inf, mentor_holobar, "Navodila za vaje – ER diagrami in normalizacija.pdf", "Praktična navodila za načrtovanje ER diagramov v orodju Mermaid in normalizacijo relacij."),
            (predmet_mat, prof_novak, "Zapiski – Kvadratna funkcija in parabola.pdf", "Teoretična razlaga kvadratne funkcije, ničel ter risanja parabol z rešenimi zgledi."),
            (predmet_mat, prof_novak, "Zbirka nalog – Sistemi linearnih enačb.pdf", "Rešene vaje s postopki zamenjave in metodo nasprotnih koeficientov."),
            (predmet_fiz, prof_novak, "Laboratorijska navodila – Merjenje pospeška.pdf", "Navodila za izvedbo fizikalnega eksperimenta in obdelavo meritev."),
            (predmet_slo, prof_horvat, "Slovenska romantika – France Prešeren.pdf", "Učna enota s poezijo, analizo Krsta pri Savici in romantičnim svetoboljem."),
        ]

        st_gradiv = 0
        for predmet, ucitelj, naslov, vsebina in gradiva_podatki:
            gradivo = Gradivo.objects.filter(predmet=predmet, naslov=naslov).first()
            if not gradivo:
                gradivo = Gradivo(predmet=predmet, nalozil=ucitelj, naslov=naslov)
                gradivo.datoteka.save(naslov, ustvari_vzorcno_datoteko(naslov, vsebina), save=True)
                st_gradiv += 1
            else:
                gradivo.nalozil = ucitelj
                gradivo.save()
                st_gradiv += 1
        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih/posodobljenih {st_gradiv} gradiv z dejanskimi datotekami."))

        # -------------------------------------------------------------
        # 3. NALOGE Z RAZLIČNIMI ROKI
        # -------------------------------------------------------------
        # 1. Projekt pri Informatiki (Matic Holobar) - rok čez 14 dni
        naloga_inf_projekt, _ = Naloga.objects.get_or_create(
            predmet=predmet_inf,
            naslov="Projekt: Načrtovanje podatkovne baze",
            defaults={
                "opis": "Pripravite celovit ER diagram z najmanj 4 tabelami, opišite povezave M:N in priložite SQL skripte. Nalogo oddajte v formatu PDF.",
                "rok": zdaj + timedelta(days=14),
                "ustvaril": mentor_holobar,
            },
        )
        naloga_inf_projekt.ustvaril = mentor_holobar
        naloga_inf_projekt.save()

        # 2. Domača naloga pri Matematiki (Janez Novak) - potekla pred 5 dnevi
        naloga_mat_domaca, _ = Naloga.objects.get_or_create(
            predmet=predmet_mat,
            naslov="1. domača naloga: Kvadratne enačbe",
            defaults={
                "opis": "Rešite naloge 1 do 10 na strani 45. Natančno izpišite postopke in izračunajte diskriminanto.",
                "rok": zdaj - timedelta(days=5),
                "ustvaril": prof_novak,
            },
        )
        naloga_mat_domaca.ustvaril = prof_novak
        naloga_mat_domaca.save()

        # 3. Laboratorijsko poročilo pri Fiziki (Janez Novak) - rok jutri
        naloga_fiz_porocilo, _ = Naloga.objects.get_or_create(
            predmet=predmet_fiz,
            naslov="Poročilo: Merjenje gravitacijskega pospeška",
            defaults={
                "opis": "Oddajte poročilo o meritvah nihanja nitnega nihala vključno z oceno eksperimentalne napake.",
                "rok": zdaj + timedelta(days=1, hours=4),
                "ustvaril": prof_novak,
            },
        )
        naloga_fiz_porocilo.ustvaril = prof_novak
        naloga_fiz_porocilo.save()

        # 4. Esej pri Slovenščini (Maja Horvat) - rok čez 7 dni
        naloga_slo_esej, _ = Naloga.objects.get_or_create(
            predmet=predmet_slo,
            naslov="Esej: Romantika na Slovenskem",
            defaults={
                "opis": "Napišite primerjalni esej ob Prešernovem Krstu pri Savici. Obseg 600 do 800 besed.",
                "rok": zdaj + timedelta(days=7),
                "ustvaril": prof_horvat,
            },
        )
        naloga_slo_esej.ustvaril = prof_horvat
        naloga_slo_esej.save()
        self.stdout.write(self.style.SUCCESS("Ustvarjene 4 naloge z različnimi roki in mentorji."))

        # -------------------------------------------------------------
        # 4. ODDAJE NALOG Z DEJANSKIMI IMENI IN OCENAMI
        # -------------------------------------------------------------
        oddaje_podatki = [
            # 1. Mitja Jančič - Projekt podatkovne baze (INF) -> Ocena 5 od Matica Holobarja
            (
                naloga_inf_projekt,
                dijak_mitja,
                False,
                5,
                "Odlično zasnovan ER diagram in popolnoma normalizirane relacije. Izjemno natančno delo, Mitja!",
                "Porocilo o nacrtovanju podatkovne baze. Avtor: Mitja Jancic. Normalizacija do 3NF.",
            ),
            # 2. Nal Dobravc - Projekt podatkovne baze (INF) -> Ocena 5 od Matica Holobarja
            (
                naloga_inf_projekt,
                dijak_nal,
                False,
                5,
                "Zelo pregledno pripravljene SQL skripte in podrobna dokumentacija modela. Čestitke, Nal!",
                "Porocilo o nacrtovanju relacijskega modela. Avtor: Nal Dobravc. SQL skripte in poizvedbe.",
            ),
            # 3. Luka Kovač - Projekt podatkovne baze (INF) -> v pregledu
            (
                naloga_inf_projekt,
                ucenci[2],
                False,
                None,
                "",
                "Projektna naloga podatkovne baze. Oddal Luka Kovac - caka na pregled.",
            ),
            # 4. Mitja Jančič - 1. domača naloga: Kvadratne enačbe (MAT) -> Ocena 5 od Janeza Novaka
            (
                naloga_mat_domaca,
                dijak_mitja,
                False,
                5,
                "Brezhiben postopek izračuna ničel, diskriminante ter risanja parabole. Bravo, Mitja!",
                "Resitve 1. domace naloge iz matematike. Mitja Jancic.",
            ),
            # 5. Nal Dobravc - 1. domača naloga: Kvadratne enačbe (MAT) -> Ocena 4 od Janeza Novaka
            (
                naloga_mat_domaca,
                dijak_nal,
                False,
                4,
                "Zelo dobro rešeno, Nal. Pri 4. nalogi pazi na predznak pred oklepajem.",
                "Resitve vaj iz kvadratnih funkcij. Nal Dobravc.",
            ),
            # 6. Jan Zupančič - 1. domača naloga: Kvadratne enačbe (MAT) -> Prepozno, Ocena 3
            (
                naloga_mat_domaca,
                ucenci[4],
                True,  # prepozno!
                3,
                "Naloga je bila oddana z zamudo po preteku roka. Vsebina je sicer ustrezna, ocena znižana.",
                "Pozna oddaja domace naloge iz matematike. Jan Zupancic.",
            ),
            # 7. Ana Novak - 1. domača naloga (MAT) -> v pregledu
            (
                naloga_mat_domaca,
                ucenci[3],
                False,
                None,
                "",
                "Resitev domace naloge - caka na pregled ucitelja.",
            ),
            # 8. Mitja Jančič - Poročilo pri Fiziki -> v pregledu
            (
                naloga_fiz_porocilo,
                dijak_mitja,
                False,
                None,
                "",
                "Porocilo o meritvah gravitacijskega pospeska. Izmerjeno g = 9.81 m/s^2. Mitja Jancic.",
            ),
            # 9. Nal Dobravc - Esej pri Slovenščini -> Ocena 5 od Maje Horvat
            (
                naloga_slo_esej,
                dijak_nal,
                False,
                5,
                "Izjemen esej z globokim razumevanjem romantičnega svetobolja in Prešernove poetike. Bravo, Nal!",
                "Primerjalni esej o slovenski romantiki. Avtor: Nal Dobravc.",
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
        # Za Mitja Jančič (ucenec1)
        u1_user = ucenci_racuni[0][0]
        Obvestilo.objects.filter(prejemnik=u1_user).delete()
        Obvestilo.objects.create(
            prejemnik=u1_user,
            besedilo="Mentor Matic Holobar je vaš projekt pri Informatiki ocenil z oceno 5. Čestitke!",
            povezava=f"/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u1_user,
            besedilo="Profesor Janez Novak je vašo domačo nalogo pri Matematiki ocenil z oceno 5.",
            povezava=f"/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u1_user,
            besedilo="Uspešno ste oddali poročilo pri predmetu Fizika. Oddaja je v pregledu.",
            povezava=f"/portal/ucenec/naloge/",
            prebrano=True,
        )

        # Za Nal Dobravc (ucenec2)
        u2_user = ucenci_racuni[1][0]
        Obvestilo.objects.filter(prejemnik=u2_user).delete()
        Obvestilo.objects.create(
            prejemnik=u2_user,
            besedilo="Mentor Matic Holobar je vaš projekt pri Informatiki ocenil z oceno 5. Odlično delo!",
            povezava=f"/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano!
        )
        Obvestilo.objects.create(
            prejemnik=u2_user,
            besedilo="Profesorica Maja Horvat je vaš esej pri Slovenščini ocenila z oceno 5.",
            povezava=f"/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano!
        )
        Obvestilo.objects.create(
            prejemnik=u2_user,
            besedilo="Profesor Janez Novak je vašo domačo nalogo pri Matematiki ocenil z oceno 4.",
            povezava=f"/portal/ucenec/naloge/",
            prebrano=True,
        )

        # Za Matic Holobar (ucitelj1)
        t1_user = ucitelji_racuni[0][0]
        Obvestilo.objects.filter(prejemnik=t1_user).delete()
        Obvestilo.objects.create(
            prejemnik=t1_user,
            besedilo="Nova oddaja naloge: Luka Kovač je oddal rešitev pri projektu 'Načrtovanje podatkovne baze'.",
            povezava=f"/portal/ucitelj/naloga/{naloga_inf_projekt.pk}/",
            prebrano=False,  # Neprebrano!
        )
        Obvestilo.objects.create(
            prejemnik=t1_user,
            besedilo="Dijak Mitja Jančič je oddal projekt pri Informatiki.",
            povezava=f"/portal/ucitelj/naloga/{naloga_inf_projekt.pk}/",
            prebrano=True,
        )
        Obvestilo.objects.create(
            prejemnik=t1_user,
            besedilo="Dijak Nal Dobravc je oddal projekt pri Informatiki.",
            povezava=f"/portal/ucitelj/naloga/{naloga_inf_projekt.pk}/",
            prebrano=True,
        )

        self.stdout.write(self.style.SUCCESS("Center za obvestila uspešno posodobljen."))
        self.stdout.write(self.style.SUCCESS("=================================================================="))
        self.stdout.write(self.style.SUCCESS("  VSI TESTNI PODATKI Z DEJANSKIMI IMENI SO USPEŠNO VZPOSTAVLJENI: "))
        self.stdout.write(self.style.SUCCESS("  - Administrator: admin / Admin123!"))
        self.stdout.write(self.style.SUCCESS("  - Mentor/Učitelj: ucitelj1 (Matic Holobar) / Ucitelj123!"))
        self.stdout.write(self.style.SUCCESS("  - Učitelj 2: ucitelj2 (Janez Novak) / Ucitelj123!"))
        self.stdout.write(self.style.SUCCESS("  - Učenec 1: ucenec1 (Mitja Jančič) / Ucenec123!"))
        self.stdout.write(self.style.SUCCESS("  - Učenec 2: ucenec2 (Nal Dobravc) / Ucenec123!"))
        self.stdout.write(self.style.SUCCESS("=================================================================="))
