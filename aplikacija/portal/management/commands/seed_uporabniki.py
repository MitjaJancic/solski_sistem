"""Ustvari uporabniške račune z uporabniškimi imeni v formatu »I.Priimek« (npr. M.Horvat):
- Administrator: admin / Admin123!
- Vseh 20 učiteljev: M.Holobar, J.Novak, M.Horvat, B.Jankovic, A.Kovacic ... / Ucitelj123!
- Vseh 120 učencev: M.Jancic, N.Dobravc, L.Kovac, A.Novak ... / Ucenec123!
- Učna gradiva z dejanskimi PDF datotekami
- Naloge z različnimi roki pri različnih učiteljih
- Oddaje nalog (format datoteke »Priimek Ime – Naslov naloge.pdf«)
- Ocenjene oddaje (ocene 1–5 s komentarji), zamujene oddaje (prepozno) ter oddaje v pregledu
- Center za obvestila (značka 🔔 za učence in učitelje)

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

PREVOD_CRK = str.maketrans("čžšČŽŠ", "czsCZS")


def generiraj_uporabnisko_ime(ime, priimek, zasedeni):
    """Ustvari uporabniško ime v formatu »I.Priimek« (npr. M.Horvat),
    brez šumnikov in zagotovi enoličnost."""
    prva = ime[0].upper()
    priimek_cist = priimek.translate(PREVOD_CRK)
    osnova = f"{prva}.{priimek_cist}"
    u = osnova
    stevec = 1
    while u.lower() in zasedeni:
        stevec += 1
        u = f"{osnova}{stevec}"
    zasedeni.add(u.lower())
    return u


def ustvari_vzorcno_datoteko(ime, vsebina_tekst):
    """Vrne ContentFile za fizično shrambo datoteke ob testiranju prenosa."""
    glava = f"--- Šolski IS+: {ime} ---\n\n"
    podatki = (glava + vsebina_tekst).encode("utf-8")
    return ContentFile(podatki, name=ime)


class Command(BaseCommand):
    help = (
        "Ustvari uporabniške račune z uporabniškimi imeni v obliki »I.Priimek« (npr. M.Horvat) "
        "za vseh 20 učiteljev in vseh 120 učencev ter gradiva, naloge, oddaje in ocene."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        zdaj = timezone.now()

        # Počistimo obstoječe profile in uporabnike razen morebitnega superuserja, ki ga bomo posodobili
        Profil.objects.all().delete()
        User.objects.exclude(username="admin").delete()

        zasedeni_uporabniki = {"admin"}

        # -------------------------------------------------------------
        # 1. ADMINISTRATOR
        # -------------------------------------------------------------
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
        predmeti = list(Predmet.objects.all())
        if not predmeti:
            self.stdout.write(self.style.WARNING("Najprej zaženite: python manage.py seed_podatki"))
            return

        predmet_inf = Predmet.objects.filter(sifra="INF").first()
        predmet_mat = Predmet.objects.filter(sifra="MAT").first()
        predmet_fiz = Predmet.objects.filter(sifra="FIZ").first()
        predmet_slo = Predmet.objects.filter(sifra="SLO").first()
        predmet_zgo = Predmet.objects.filter(sifra="ZGO").first()
        predmet_kem = Predmet.objects.filter(sifra="KEM").first()
        predmet_bio = Predmet.objects.filter(sifra="BIO").first()
        predmet_ang = Predmet.objects.filter(sifra="ANG").first()
        predmet_geo = Predmet.objects.filter(sifra="GEO").first()
        predmet_spo = Predmet.objects.filter(sifra="SPO").first()

        # -------------------------------------------------------------
        # 2. VSEH 20 UČITELJEV Z UPORABNIŠKIMI IMENI I.Priimek
        # -------------------------------------------------------------
        ucitelji = list(Ucitelj.objects.all().order_by("id"))
        ucitelji_racuni = {}  # ucitelj.id -> (user, username)

        for ucitelj in ucitelji:
            username = generiraj_uporabnisko_ime(ucitelj.ime, ucitelj.priimek, zasedeni_uporabniki)
            user = User.objects.create(
                username=username,
                email=ucitelj.email,
                first_name=ucitelj.ime,
                last_name=ucitelj.priimek,
            )
            user.set_password(GESLO_UCITELJ)
            user.save()

            Profil.objects.create(
                uporabnik=user,
                vloga=Profil.Vloga.UCITELJ,
                ucitelj=ucitelj,
            )
            ucitelji_racuni[ucitelj.id] = (user, username)

        self.stdout.write(
            self.style.SUCCESS(
                f"Ustvarjenih {len(ucitelji)} računov učiteljev v obliki I.Priimek (geslo: {GESLO_UCITELJ})."
            )
        )

        # -------------------------------------------------------------
        # 3. VSEH 120 UČENCEV Z UPORABNIŠKIMI IMENI I.Priimek
        # -------------------------------------------------------------
        ucenci = list(Ucenec.objects.all().order_by("id"))
        ucenci_racuni = {}  # ucenec.id -> (user, username)

        for ucenec in ucenci:
            username = generiraj_uporabnisko_ime(ucenec.ime, ucenec.priimek, zasedeni_uporabniki)
            user = User.objects.create(
                username=username,
                email=ucenec.email,
                first_name=ucenec.ime,
                last_name=ucenec.priimek,
            )
            user.set_password(GESLO_UCENEC)
            user.save()

            Profil.objects.create(
                uporabnik=user,
                vloga=Profil.Vloga.UCENEC,
                ucenec=ucenec,
            )
            ucenci_racuni[ucenec.id] = (user, username)

        self.stdout.write(
            self.style.SUCCESS(
                f"Ustvarjenih {len(ucenci)} računov učencev v obliki I.Priimek (geslo: {GESLO_UCENEC})."
            )
        )

        # Ključni učitelji za vzorčne vsebine
        prof_holobar = Ucitelj.objects.filter(ime="Matic", priimek="Holobar").first() or ucitelji[0]
        prof_novak = Ucitelj.objects.filter(ime="Janez", priimek="Novak").first() or ucitelji[1]
        prof_horvat = Ucitelj.objects.filter(ime="Maja", priimek="Horvat").first() or ucitelji[2]
        prof_jankovic = Ucitelj.objects.filter(ime="Boris", priimek="Jankovič").first() or ucitelji[3]
        prof_kovacic = Ucitelj.objects.filter(ime="Ana", priimek="Kovačič").first() or ucitelji[4]

        # Ključni učenci za vzorčne oddaje
        dijak_mitja = Ucenec.objects.filter(ime="Mitja", priimek="Jančič").first() or ucenci[0]
        dijak_nal = Ucenec.objects.filter(ime="Nal", priimek="Dobravc").first() or ucenci[1]
        dijak_luka = Ucenec.objects.filter(ime="Luka", priimek="Kovač").first() or ucenci[2]
        dijak_ana = Ucenec.objects.filter(ime="Ana", priimek="Novak").first() or ucenci[3]
        dijak_ema = Ucenec.objects.filter(ime="Ema", priimek="Podgoršek").first() or ucenci[31]

        # -------------------------------------------------------------
        # 4. UČNA GRADIVA
        # -------------------------------------------------------------
        gradiva_podatki = [
            (predmet_inf, prof_holobar, "Priročnik – Relacijske podatkovne baze in SQL.pdf", "Vzorčno gradivo za relacijske modele, tabele, ključe in poizvedbe SQL. Avtor: Matic Holobar."),
            (predmet_inf, prof_holobar, "Navodila za vaje – ER diagrami in normalizacija.pdf", "Praktična navodila za načrtovanje podatkovnih baz in 3NF normalizacijo."),
            (predmet_mat, prof_novak, "Zapiski – Kvadratna funkcija in parabola.pdf", "Teoretična razlaga kvadratne funkcije, ničel, diskriminante ter risanja parabol."),
            (predmet_mat, prof_novak, "Zbirka nalog – Sistemi linearnih enačb.pdf", "Rešene vaje s postopki zamenjave in metodo nasprotnih koeficientov."),
            (predmet_fiz, prof_novak, "Laboratorijska navodila – Merjenje pospeška.pdf", "Navodila za izvedbo fizikalnega eksperimenta nihanja nitnega nihala."),
            (predmet_slo, prof_horvat, "Slovenska romantika – France Prešeren.pdf", "Učna enota s poezijo in analizo Krsta pri Savici."),
            (predmet_zgo, prof_horvat, "Gradivo – Soška fronta v prvi svetovni vojni.pdf", "Zgodovinski viri in pričevanja o bojih ob Soči 1915–1917."),
            (predmet_kem, prof_jankovic, "Laboratorijski protokol – Titracija kislin in baz.pdf", "Navodila za volumetrično analizo z nevtralizacijo in barvnimi indikatorji."),
            (predmet_kem, prof_jankovic, "Preglednica – Periodni sistem in kemijske vezi.pdf", "Pregled periodnih lastnosti ter kovalentnih in ionskih vezi."),
            (predmet_bio, prof_jankovic, "Zapiski – Citologija in celična zgradba.pdf", "Zgradba evkariontske celice, celičnih organelov in transportne funkcije."),
            (predmet_ang, prof_kovacic, "Academic Writing – Essay Structure and Vocabulary.pdf", "Strukturiranje akademskega eseja in napredno besedišče."),
            (predmet_geo, prof_kovacic, "Geomorfološke enote Slovenije – Pregled regij.pdf", "Reliefne značilnosti alpskega, dinarskega in panonskega sveta Slovenije."),
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
        # 5. NALOGE Z RAZLIČNIMI ROKI
        # -------------------------------------------------------------
        naloga_inf_projekt, _ = Naloga.objects.get_or_create(
            predmet=predmet_inf,
            naslov="Projekt: Načrtovanje podatkovne baze",
            defaults={
                "opis": "Pripravite celovit ER diagram z najmanj 4 tabelami, opišite povezave M:N in priložite SQL skripte. Nalogo oddajte v formatu PDF.",
                "rok": zdaj + timedelta(days=14),
                "ustvaril": prof_holobar,
            },
        )
        naloga_inf_projekt.ustvaril = prof_holobar
        naloga_inf_projekt.save()

        naloga_inf_vaje, _ = Naloga.objects.get_or_create(
            predmet=predmet_inf,
            naslov="Vaja: Poizvedbe SQL z združevanjem tabel (JOIN)",
            defaults={
                "opis": "Napišite SQL poizvedbe z INNER JOIN, LEFT JOIN ter agregatnimi funkcijami COUNT in AVG.",
                "rok": zdaj + timedelta(days=5),
                "ustvaril": prof_holobar,
            },
        )
        naloga_inf_vaje.ustvaril = prof_holobar
        naloga_inf_vaje.save()

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

        naloga_kem_titracija, _ = Naloga.objects.get_or_create(
            predmet=predmet_kem,
            naslov="Laboratorijsko poročilo: Titracija klorovodikove kisline",
            defaults={
                "opis": "V poročilu prikažite postopek titracije HCl z 0.1 M raztopino NaOH ter izračunajte neznano koncentracijo.",
                "rok": zdaj - timedelta(days=2),
                "ustvaril": prof_jankovic,
            },
        )
        naloga_kem_titracija.ustvaril = prof_jankovic
        naloga_kem_titracija.save()

        naloga_bio_celica, _ = Naloga.objects.get_or_create(
            predmet=predmet_bio,
            naslov="Poročilo o vajah: Mikroskopiranje celic čebule",
            defaults={
                "opis": "Narišite opazovano tkivo povrhnjice čebulnega lista ter označite jedro, vakuolo in celično steno.",
                "rok": zdaj + timedelta(days=10),
                "ustvaril": prof_jankovic,
            },
        )
        naloga_bio_celica.ustvaril = prof_jankovic
        naloga_bio_celica.save()

        naloga_ang_esej, _ = Naloga.objects.get_or_create(
            predmet=predmet_ang,
            naslov="Essay: Artificial Intelligence in Education",
            defaults={
                "opis": "Write a 400-500 word argumentative essay discussing the benefits and ethical concerns of AI in schools.",
                "rok": zdaj + timedelta(days=8),
                "ustvaril": prof_kovacic,
            },
        )
        naloga_ang_esej.ustvaril = prof_kovacic
        naloga_ang_esej.save()

        self.stdout.write(self.style.SUCCESS("Ustvarjenih 8 nalog pri različnih učiteljih."))

        # -------------------------------------------------------------
        # 6. ODDAJE NALOG (Format »Priimek Ime – Naslov naloge.pdf«)
        # -------------------------------------------------------------
        oddaje_podatki = [
            # Mitja Jančič (4.A) -> Uporabnik: M.Jancic
            (
                naloga_inf_projekt, dijak_mitja, False, 5,
                "Odlično zasnovan ER diagram in popolnoma normalizirane relacije do 3NF. Izjemno natančno delo, Mitja!",
                "Porocilo o nacrtovanju podatkovne baze. Avtor: Mitja Jancic (4.A). ER diagram in SQL skripte.",
            ),
            (
                naloga_mat_domaca, dijak_mitja, False, 5,
                "Brezhiben postopek izračuna ničel, diskriminante ter risanja parabole. Bravo, Mitja!",
                "Resitve 1. domace naloge iz kvadratnih enacb. Mitja Jancic (4.A).",
            ),
            (
                naloga_kem_titracija, dijak_mitja, False, 5,
                "Zelo natančno izvedena titracija z minimalnim odstopanjem od teoretične vrednosti. Izvrstno!",
                "Porocilo o titraciji HCl z NaOH. Avtor: Mitja Jancic (4.A).",
            ),
            (
                naloga_fiz_porocilo, dijak_mitja, False, None,
                "",  # V pregledu!
                "Porocilo o meritvah gravitacijskega pospeska g = 9.81 m/s^2. Mitja Jancic (4.A).",
            ),
            (
                naloga_ang_esej, dijak_mitja, False, None,
                "",  # V pregledu!
                "Argumentative essay on Artificial Intelligence in Education. By Mitja Jancic (4.A).",
            ),

            # Nal Dobravc (4.A) -> Uporabnik: N.Dobravc
            (
                naloga_inf_projekt, dijak_nal, False, 5,
                "Zelo pregledno pripravljene SQL skripte in podrobna dokumentacija modela. Čestitke, Nal!",
                "Porocilo o nacrtovanju relacijskega modela. Avtor: Nal Dobravc (4.A). SQL skripte in poizvedbe.",
            ),
            (
                naloga_mat_domaca, dijak_nal, False, 4,
                "Zelo dobro rešeno, Nal. Pri 4. nalogi bodi bolj pozoren na predznak pred oklepajem.",
                "Resitve vaj iz kvadratnih funkcij. Nal Dobravc (4.A).",
            ),
            (
                naloga_slo_esej, dijak_nal, False, 5,
                "Izjemen esej z globokim razumevanjem romantičnega svetobolja in Prešernove poetike. Bravo, Nal!",
                "Primerjalni esej o slovenski romantiki in Krstu pri Savici. Avtor: Nal Dobravc (4.A).",
            ),
            (
                naloga_kem_titracija, dijak_nal, True, 3,  # Prepozno oddano!
                "Naloga je bila oddana po preteku roka. Vsebina laboratorijskega protokola je ustrezna, ocena znižana zaradi zamude.",
                "Pozna oddaja laboratorijskega porocila o titraciji. Nal Dobravc (4.A).",
            ),

            # Luka Kovač (4.A) -> Uporabnik: L.Kovac
            (
                naloga_inf_projekt, dijak_luka, False, None,
                "",  # V pregledu pri Maticu Holobarju
                "Projektna naloga podatkovne baze: Model knjigarne. Luka Kovac (4.A) - caka na pregled.",
            ),
            (
                naloga_mat_domaca, dijak_luka, False, 3,
                "Naloge so delno rešene, manjkajo postopki pri nalogah 7 in 8.",
                "Domaca naloga kvadratne enacbe. Luka Kovac (4.A).",
            ),
            (
                naloga_kem_titracija, dijak_luka, False, None,
                "",  # V pregledu pri Borisu Jankoviču
                "Laboratorijski zapiski titracije. Luka Kovac (4.A).",
            ),

            # Ana Novak (4.A) -> Uporabnik: A.Novak
            (
                naloga_slo_esej, dijak_ana, False, 5,
                "Odlična zgradba eseja, prepričljiva argumentacija in bogat besedni zaklad.",
                "Esej o pesnitvi Krst pri Savici. Ana Novak (4.A).",
            ),

            # Ema Podgoršek (3.A) -> Uporabnik: E.Podgorsek
            (
                naloga_mat_domaca, dijak_ema, False, 5,
                "Vzorčno rešene vaje s preglednim postopkom in grafi kvadratnih funkcij.",
                "Resitve domace naloge iz matematike. Ema Podgorsek (3.A).",
            ),
            (
                naloga_fiz_porocilo, dijak_ema, False, None,
                "",  # V pregledu pri Janezu Novaku
                "Meritve nihanja nitnega nihala. Ema Podgorsek (3.A).",
            ),
            (
                naloga_kem_titracija, dijak_ema, False, 4,
                "Lepo pripravljeno poročilo, natančni izračuni.",
                "Titracija kisline in baze. Ema Podgorsek (3.A).",
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
                st_oddaj += 1

        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih/posodobljenih {st_oddaj} oddaj nalog z ocenami in komentarji."))

        # -------------------------------------------------------------
        # 7. CENTER ZA OBVESTILA
        # -------------------------------------------------------------
        # Mitja Jančič (M.Jancic)
        u_mitja = ucenci_racuni[dijak_mitja.id][0]
        Obvestilo.objects.filter(prejemnik=u_mitja).delete()
        Obvestilo.objects.create(
            prejemnik=u_mitja,
            besedilo="Mentor Matic Holobar (M.Holobar) je vaš projekt pri Informatiki ocenil z oceno 5. Čestitke!",
            povezava="/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u_mitja,
            besedilo="Profesor Boris Jankovič (B.Jankovic) je vaše poročilo pri Kemiji ocenil z oceno 5.",
            povezava="/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u_mitja,
            besedilo="Profesor Janez Novak (J.Novak) je vašo domačo nalogo pri Matematiki ocenil z oceno 5.",
            povezava="/portal/ucenec/naloge/",
            prebrano=True,
        )

        # Nal Dobravc (N.Dobravc)
        u_nal = ucenci_racuni[dijak_nal.id][0]
        Obvestilo.objects.filter(prejemnik=u_nal).delete()
        Obvestilo.objects.create(
            prejemnik=u_nal,
            besedilo="Mentor Matic Holobar (M.Holobar) je vaš projekt pri Informatiki ocenil z oceno 5. Odlično delo!",
            povezava="/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u_nal,
            besedilo="Profesorica Maja Horvat (M.Horvat) je vaš esej pri Slovenščini ocenila z oceno 5.",
            povezava="/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u_nal,
            besedilo="Profesor Boris Jankovič (B.Jankovic) je ocenil vaše poročilo pri Kemiji z oceno 3 (oddano z zamudo).",
            povezava="/portal/ucenec/naloge/",
            prebrano=True,
        )

        # Matic Holobar (M.Holobar)
        u_holobar = ucitelji_racuni[prof_holobar.id][0]
        Obvestilo.objects.filter(prejemnik=u_holobar).delete()
        Obvestilo.objects.create(
            prejemnik=u_holobar,
            besedilo="Nova oddaja naloge: Luka Kovač (4.A) je oddal projekt 'Načrtovanje podatkovne baze'.",
            povezava=f"/portal/ucitelj/naloga/{naloga_inf_projekt.pk}/",
            prebrano=False,  # Neprebrano -> 🔔!
        )

        # Boris Jankovič (B.Jankovic)
        u_jankovic = ucitelji_racuni[prof_jankovic.id][0]
        Obvestilo.objects.filter(prejemnik=u_jankovic).delete()
        Obvestilo.objects.create(
            prejemnik=u_jankovic,
            besedilo="Nova oddaja naloge: Luka Kovač (4.A) je oddal poročilo 'Titracija klorovodikove kisline'.",
            povezava=f"/portal/ucitelj/naloga/{naloga_kem_titracija.pk}/",
            prebrano=False,  # Neprebrano -> 🔔!
        )

        # Janez Novak (J.Novak)
        u_novak = ucitelji_racuni[prof_novak.id][0]
        Obvestilo.objects.filter(prejemnik=u_novak).delete()
        Obvestilo.objects.create(
            prejemnik=u_novak,
            besedilo="Nova oddaja naloge: Mitja Jančič (4.A) je oddal poročilo pri Fiziki.",
            povezava=f"/portal/ucitelj/naloga/{naloga_fiz_porocilo.pk}/",
            prebrano=False,  # Neprebrano -> 🔔!
        )

        self.stdout.write(self.style.SUCCESS("Center za obvestila uspešno posodobljen."))
        self.stdout.write(self.style.SUCCESS("=================================================================="))
        self.stdout.write(self.style.SUCCESS("  VSI UPORABNIŠKI RAČUNI SO V FORMATU »I.Priimek« (npr. M.Horvat):"))
        self.stdout.write(self.style.SUCCESS(f"  - Administrator: admin / {GESLO_ADMIN}"))
        self.stdout.write(self.style.SUCCESS(f"  - Učitelji ({len(ucitelji)} računov, geslo: {GESLO_UCITELJ}):"))
        for u in ucitelji[:5]:
            uname = ucitelji_racuni[u.id][1]
            predmeti_str = ", ".join(p.sifra for p in u.predmeti.all())
            self.stdout.write(self.style.SUCCESS(f"      • {uname} ({u.priimek} {u.ime}) [{predmeti_str}]"))
        self.stdout.write(self.style.SUCCESS(f"      • ... in še {len(ucitelji) - 5} ostalih učiteljev v istem formatu"))
        self.stdout.write(self.style.SUCCESS(f"  - Učenci ({len(ucenci)} računov, geslo: {GESLO_UCENEC}):"))
        for u in ucenci[:5]:
            uname = ucenci_racuni[u.id][1]
            self.stdout.write(self.style.SUCCESS(f"      • {uname} ({u.priimek} {u.ime} - {u.razred})"))
        self.stdout.write(self.style.SUCCESS(f"      • ... in še {len(ucenci) - 5} ostalih učencev v istem formatu"))
        self.stdout.write(self.style.SUCCESS("=================================================================="))
