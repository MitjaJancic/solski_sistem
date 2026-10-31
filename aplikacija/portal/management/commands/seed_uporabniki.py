"""Ustvari obsežne testne podatke z dejanskimi slovenskimi imeni:
- 5 Učiteljev:
    1. Matic Holobar (mentor) -> Informatika (INF)
    2. Janez Novak -> Matematika (MAT), Fizika (FIZ)
    3. Maja Horvat -> Slovenščina (SLO), Zgodovina (ZGO)
    4. Boris Jankovič -> Kemija (KEM), Biologija (BIO)
    5. Ana Kovačič -> Angleščina (ANG), Geografija (GEO), Šport (SPO)
- Učenci:
    Mitja Jančič, Nal Dobravc (oba 3.A), Luka Kovač (3.A), Ema Podgoršek (2.A), Klemen Majcen (1.A)
- Učna gradiva z dejanskimi datotekami za vse predmete
- Domače naloge z različnimi roki (prihodnji roki, potekli roki)
- Oddaje nalog z avtomatskim poimenovanjem »Priimek Ime – Naslov naloge.pdf«
- Ocenjene oddaje (ocene 1–5 s strokovnimi komentarji profesorjev), zamujene oddaje (prepozno=True) ter oddaje v pregledu
- Center za obvestila (rdeča značka neprebranih obvestil za učence in učitelje)

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
    glava = f"--- Šolski IS+: {ime} ---\n\n"
    podatki = (glava + vsebina_tekst).encode("utf-8")
    return ContentFile(podatki, name=ime)


class Command(BaseCommand):
    help = (
        "Ustvari uporabniške račune za 5 učiteljev (vsak z različnimi predmeti), "
        "reprezentativne učence iz vseh 3 razredov ter učna gradiva, naloge, oddaje in ocene."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        zdaj = timezone.now()

        # Počistimo stare demo profile in uporabnike
        Profil.objects.all().delete()
        User.objects.filter(username__startswith="ucitelj").delete()
        User.objects.filter(username__startswith="ucenec").delete()

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

        if not predmet_inf or not predmet_mat:
            self.stdout.write(self.style.WARNING("Najprej zaženite seed_podatki."))
            return

        # -------------------------------------------------------------
        # 2. TOČNO 5 UČITELJEV Z RAZLIČNIMI PREDMETI
        # -------------------------------------------------------------
        ucitelji_definicije = [
            ("Matic", "Holobar", "matic.holobar@solski-is.si", [predmet_inf]),
            ("Janez", "Novak", "janez.novak@solski-is.si", [predmet_mat, predmet_fiz]),
            ("Maja", "Horvat", "maja.horvat@solski-is.si", [predmet_slo, predmet_zgo]),
            ("Boris", "Jankovič", "boris.jankovic@solski-is.si", [predmet_kem, predmet_bio]),
            ("Ana", "Kovačič", "ana.kovacic@solski-is.si", [predmet_ang, predmet_geo, predmet_spo]),
        ]

        ucitelji_racuni = []
        ucitelji_obj = []
        for i, (ime, priimek, email, predmeti) in enumerate(ucitelji_definicije, start=1):
            ucitelj, _ = Ucitelj.objects.get_or_create(
                ime=ime, priimek=priimek,
                defaults={"email": email}
            )
            ucitelj.predmeti.set(predmeti)
            ucitelji_obj.append(ucitelj)

            username = f"ucitelj{i}"
            uporabnik, _ = User.objects.get_or_create(username=username, defaults={"email": email})
            uporabnik.set_password(GESLO_UCITELJ)
            uporabnik.email = email
            uporabnik.save()

            Profil.objects.update_or_create(
                uporabnik=uporabnik,
                defaults={"vloga": Profil.Vloga.UCITELJ, "ucitelj": ucitelj},
            )
            ucitelji_racuni.append((uporabnik, ucitelj))
            predmeti_str = ", ".join(p.sifra for p in predmeti)
            self.stdout.write(
                self.style.SUCCESS(f"Učitelj {i}: {username} / {GESLO_UCITELJ} -> {ucitelj.priimek} {ucitelj.ime} ({predmeti_str})")
            )

        prof_holobar = ucitelji_obj[0]
        prof_novak = ucitelji_obj[1]
        prof_horvat = ucitelji_obj[2]
        prof_jankovic = ucitelji_obj[3]
        prof_kovacic = ucitelji_obj[4]

        # -------------------------------------------------------------
        # 3. UČENCI IN UPORABNIŠKI RAČUNI
        # -------------------------------------------------------------
        ucenci_definicije = [
            ("Mitja", "Jančič", "3.A"),
            ("Nal", "Dobravc", "3.A"),
            ("Luka", "Kovač", "3.A"),
            ("Ema", "Podgoršek", "2.A"),
            ("Klemen", "Majcen", "1.A"),
        ]

        ucenci_racuni = []
        ucenci_obj = []
        for i, (ime, priimek, razred) in enumerate(ucenci_definicije, start=1):
            ucenec = Ucenec.objects.filter(ime=ime, priimek=priimek).first()
            if not ucenec:
                ucenec = Ucenec.objects.create(
                    ime=ime,
                    priimek=priimek,
                    email=f"{ime.lower()}.{priimek.lower()}@dijaki.solski-is.si",
                    razred=razred,
                )
            ucenci_obj.append(ucenec)

            username = f"ucenec{i}"
            uporabnik, _ = User.objects.get_or_create(
                username=username, defaults={"email": ucenec.email}
            )
            uporabnik.set_password(GESLO_UCENEC)
            uporabnik.email = ucenec.email
            uporabnik.save()

            Profil.objects.update_or_create(
                uporabnik=uporabnik,
                defaults={"vloga": Profil.Vloga.UCENEC, "ucenec": ucenec},
            )
            ucenci_racuni.append((uporabnik, ucenec))
            self.stdout.write(
                self.style.SUCCESS(f"Učenec {i}: {username} / {GESLO_UCENEC} -> {ucenec.priimek} {ucenec.ime} ({ucenec.razred})")
            )

        dijak_mitja = ucenci_obj[0]
        dijak_nal = ucenci_obj[1]
        dijak_luka = ucenci_obj[2]
        dijak_ema = ucenci_obj[3]
        dijak_klemen = ucenci_obj[4]

        # -------------------------------------------------------------
        # 4. UČNA GRADIVA
        # -------------------------------------------------------------
        gradiva_podatki = [
            # Informatika - Matic Holobar
            (predmet_inf, prof_holobar, "Priročnik – Relacijske podatkovne baze in SQL.pdf", "Vzorčno učno gradivo za relacijske modele, tabele, primarne in tuje ključe ter poizvedbe SQL. Avtor: Matic Holobar."),
            (predmet_inf, prof_holobar, "Navodila za vaje – ER diagrami in normalizacija.pdf", "Praktična navodila za načrtovanje ER diagramov in normalizacijo relacijskih tabel do 3NF."),
            # Matematika - Janez Novak
            (predmet_mat, prof_novak, "Zapiski – Kvadratna funkcija in parabola.pdf", "Teoretična razlaga kvadratne funkcije, ničel, diskriminante ter risanja parabol z rešenimi zgledi."),
            (predmet_mat, prof_novak, "Zbirka nalog – Sistemi linearnih enačb.pdf", "Rešene vaje s postopki zamenjave in metodo nasprotnih koeficientov."),
            # Fizika - Janez Novak
            (predmet_fiz, prof_novak, "Laboratorijska navodila – Merjenje pospeška.pdf", "Navodila za izvedbo fizikalnega eksperimenta in obdelavo meritev nihanja nitnega nihala."),
            # Slovenščina - Maja Horvat
            (predmet_slo, prof_horvat, "Slovenska romantika – France Prešeren.pdf", "Učna enota s poezijo, analizo Krsta pri Savici in romantičnim svetoboljem."),
            # Zgodovina - Maja Horvat
            (predmet_zgo, prof_horvat, "Gradivo – Soška fronta v prvi svetovni vojni.pdf", "Zgodovinski pregled vojskovanja v slovenskih gorah 1915–1917 s slikovnim gradivom."),
            # Kemija - Boris Jankovič
            (predmet_kem, prof_jankovic, "Laboratorijski protokol – Titracija kislin in baz.pdf", "Navodila za volumetrično analizo z nevtralizacijsko titracijo in uporabo indikatorjev."),
            (predmet_kem, prof_jankovic, "Preglednica – Periodni sistem in kemijske vezi.pdf", "Razlaga kovalentnih, ionskih in kovinskih vezi ter elektronegativnosti."),
            # Biologija - Boris Jankovič
            (predmet_bio, prof_jankovic, "Zapiski – Citologija in zgradba celice.pdf", "Zgradba evkariontske rastlinske in živalske celice ter celičnih organelov."),
            # Angleščina - Ana Kovačič
            (predmet_ang, prof_kovacic, "Academic Writing – Essay Structure and Vocabulary.pdf", "Navodila za strukturiranje argumentativnega eseja in akademsko besedišče."),
            # Geografija - Ana Kovačič
            (predmet_geo, prof_kovacic, "Geomorfološke enote Slovenije – Pregled regij.pdf", "Karakteristike alpskega, dinarskega, panonskega in sredozemskega sveta Slovenije."),
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
        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih/posodobljenih {st_gradiv} gradiv za vseh 5 učiteljev."))

        # -------------------------------------------------------------
        # 5. NALOGE Z RAZLIČNIMI ROKI
        # -------------------------------------------------------------
        # 1. INF (Matic Holobar) - rok čez 14 dni
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

        # 2. INF (Matic Holobar) - rok čez 5 dni
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

        # 3. MAT (Janez Novak) - potekla pred 5 dnevi
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

        # 4. FIZ (Janez Novak) - rok jutri
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

        # 5. SLO (Maja Horvat) - rok čez 7 dni
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

        # 6. KEM (Boris Jankovič) - potekla pred 2 dnevoma
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

        # 7. BIO (Boris Jankovič) - rok čez 10 dni
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

        # 8. ANG (Ana Kovačič) - rok čez 8 dni
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

        self.stdout.write(self.style.SUCCESS("Ustvarjenih 8 nalog pri vseh 5 učiteljih."))

        # -------------------------------------------------------------
        # 6. ODDAJE NALOG Z REALNIMI IMENI, OCENAMI IN DATOTEKAMI
        # -------------------------------------------------------------
        # Format datoteke po navodilih: "Priimek Ime – Naslov naloge.pdf"
        oddaje_podatki = [
            # Mitja Jančič (3.A)
            (
                naloga_inf_projekt, dijak_mitja, False, 5,
                "Odlično zasnovan ER diagram in popolnoma normalizirane relacije do 3NF. Izjemno natančno delo, Mitja!",
                "Porocilo o nacrtovanju podatkovne baze. Avtor: Mitja Jancic (3.A). ER diagram in SQL koda.",
            ),
            (
                naloga_mat_domaca, dijak_mitja, False, 5,
                "Brezhiben postopek izračuna ničel, diskriminante ter risanja parabole. Bravo, Mitja!",
                "Resitve 1. domace naloge iz kvadratnih enacb. Mitja Jancic (3.A).",
            ),
            (
                naloga_kem_titracija, dijak_mitja, False, 5,
                "Zelo natančno izvedena titracija z minimalnim odstopanjem od teoretične vrednosti. Izvrstno!",
                "Porocilo o titraciji HCl z NaOH. Avtor: Mitja Jancic (3.A).",
            ),
            (
                naloga_fiz_porocilo, dijak_mitja, False, None,
                "",  # V pregledu!
                "Porocilo o meritvah gravitacijskega pospeska g = 9.81 m/s^2. Mitja Jancic (3.A).",
            ),
            (
                naloga_ang_esej, dijak_mitja, False, None,
                "",  # V pregledu!
                "Argumentative essay on Artificial Intelligence in Modern Education. By Mitja Jancic (3.A).",
            ),

            # Nal Dobravc (3.A)
            (
                naloga_inf_projekt, dijak_nal, False, 5,
                "Zelo pregledno pripravljene SQL skripte in podrobna dokumentacija podatkovnega modela. Čestitke, Nal!",
                "Porocilo o nacrtovanju relacijskega modela. Avtor: Nal Dobravc (3.A). SQL skripte in poizvedbe.",
            ),
            (
                naloga_mat_domaca, dijak_nal, False, 4,
                "Zelo dobro rešeno, Nal. Pri 4. nalogi bodi bolj pozoren na predznak pred oklepajem.",
                "Resitve vaj iz kvadratnih funkcij. Nal Dobravc (3.A).",
            ),
            (
                naloga_slo_esej, dijak_nal, False, 5,
                "Izjemen esej z globokim razumevanjem romantičnega svetobolja in Prešernove poetike. Bravo, Nal!",
                "Primerjalni esej o slovenski romantiki in Krstu pri Savici. Avtor: Nal Dobravc (3.A).",
            ),
            (
                naloga_kem_titracija, dijak_nal, True, 3,  # Prepozno oddano!
                "Naloga je bila oddana po preteku roka. Vsebina laboratorijskega protokola je ustrezna, ocena znižana zaradi zamude.",
                "Pozna oddaja laboratorijskega porocila o titraciji. Nal Dobravc (3.A).",
            ),

            # Luka Kovač (3.A)
            (
                naloga_inf_projekt, dijak_luka, False, None,
                "",  # V pregledu pri Maticu Holobarju!
                "Projektna naloga podatkovne baze: Model knjigarne. Luka Kovac (3.A) - caka na pregled.",
            ),
            (
                naloga_mat_domaca, dijak_luka, False, 3,
                "Naloge so delno rešene, manjkajo postopki pri nalogah 7 in 8.",
                "Domaca naloga kvadratne enacbe. Luka Kovac (3.A).",
            ),
            (
                naloga_kem_titracija, dijak_luka, False, None,
                "",  # V pregledu pri Borisu Jankoviču!
                "Laboratorijski zapiski titracije. Luka Kovac (3.A).",
            ),

            # Ema Podgoršek (2.A)
            (
                naloga_mat_domaca, dijak_ema, False, 5,
                "Vzorčno rešene vaje s preglednim postopkom in grafi kvadratnih funkcij.",
                "Resitve domace naloge iz matematike. Ema Podgorsek (2.A).",
            ),
            (
                naloga_fiz_porocilo, dijak_ema, False, None,
                "",  # V pregledu pri Janezu Novaku!
                "Meritve nihanja nitnega nihala. Ema Podgorsek (2.A).",
            ),
            (
                naloga_kem_titracija, dijak_ema, False, 4,
                "Lepo pripravljeno poročilo, natančni izračuni.",
                "Titracija kisline in baze. Ema Podgorsek (2.A).",
            ),

            # Klemen Majcen (1.A)
            (
                naloga_inf_vaje, dijak_klemen, False, None,
                "",  # V pregledu pri Maticu Holobarju!
                "Vaje SQL poizvedb. Klemen Majcen (1.A).",
            ),
            (
                naloga_ang_esej, dijak_klemen, False, 5,
                "Well structured essay with excellent grammar and compelling arguments. Well done, Klemen!",
                "Essay on Artificial Intelligence. Klemen Majcen (1.A).",
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

        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih/posodobljenih {st_oddaj} oddaj nalog (ocene 1–5, opombe, zamude)."))

        # -------------------------------------------------------------
        # 7. CENTER ZA OBVESTILA
        # -------------------------------------------------------------
        # Za Mitjo Jančiča (ucenec1)
        u1_user = ucenci_racuni[0][0]
        Obvestilo.objects.filter(prejemnik=u1_user).delete()
        Obvestilo.objects.create(
            prejemnik=u1_user,
            besedilo="Mentor Matic Holobar je vaš projekt pri Informatiki ocenil z oceno 5. Čestitke!",
            povezava="/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u1_user,
            besedilo="Profesor Boris Jankovič je vaše laboratorijsko poročilo pri Kemiji ocenil z oceno 5.",
            povezava="/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u1_user,
            besedilo="Profesor Janez Novak je vašo domačo nalogo pri Matematiki ocenil z oceno 5.",
            povezava="/portal/ucenec/naloge/",
            prebrano=True,
        )

        # Za Nala Dobravca (ucenec2)
        u2_user = ucenci_racuni[1][0]
        Obvestilo.objects.filter(prejemnik=u2_user).delete()
        Obvestilo.objects.create(
            prejemnik=u2_user,
            besedilo="Mentor Matic Holobar je vaš projekt pri Informatiki ocenil z oceno 5. Odlično delo!",
            povezava="/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u2_user,
            besedilo="Profesorica Maja Horvat je vaš esej pri Slovenščini ocenila z oceno 5.",
            povezava="/portal/ucenec/naloge/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=u2_user,
            besedilo="Profesor Boris Jankovič je ocenil vaše laboratorijsko poročilo pri Kemiji z oceno 3 (oddano z zamudo).",
            povezava="/portal/ucenec/naloge/",
            prebrano=True,
        )

        # Za Matica Holobarja (ucitelj1)
        t1_user = ucitelji_racuni[0][0]
        Obvestilo.objects.filter(prejemnik=t1_user).delete()
        Obvestilo.objects.create(
            prejemnik=t1_user,
            besedilo="Nova oddaja naloge: Luka Kovač (3.A) je oddal projekt 'Načrtovanje podatkovne baze'.",
            povezava=f"/portal/ucitelj/naloga/{naloga_inf_projekt.pk}/",
            prebrano=False,  # Neprebrano -> 🔔!
        )
        Obvestilo.objects.create(
            prejemnik=t1_user,
            besedilo="Nova oddaja naloge: Klemen Majcen (1.A) je oddal vajo 'Poizvedbe SQL z združevanjem tabel'.",
            povezava=f"/portal/ucitelj/naloga/{naloga_inf_vaje.pk}/",
            prebrano=False,  # Neprebrano -> 🔔!
        )

        # Za Borisa Jankoviča (ucitelj4)
        t4_user = ucitelji_racuni[3][0]
        Obvestilo.objects.filter(prejemnik=t4_user).delete()
        Obvestilo.objects.create(
            prejemnik=t4_user,
            besedilo="Nova oddaja naloge: Luka Kovač (3.A) je oddal poročilo 'Titracija klorovodikove kisline'.",
            povezava=f"/portal/ucitelj/naloga/{naloga_kem_titracija.pk}/",
            prebrano=False,  # Neprebrano -> 🔔!
        )

        self.stdout.write(self.style.SUCCESS("Center za obvestila uspešno posodobljen."))
        self.stdout.write(self.style.SUCCESS("=================================================================="))
        self.stdout.write(self.style.SUCCESS("  VSI TESTNI PODATKI Z DEJANSKIMI IMENI IN 3 RAZREDI SO VZPOSTAVLJENI:"))
        self.stdout.write(self.style.SUCCESS("  - Administrator: admin / Admin123!"))
        self.stdout.write(self.style.SUCCESS("  - Učitelj 1 (Mentor): ucitelj1 (Matic Holobar) / Ucitelj123! [INF]"))
        self.stdout.write(self.style.SUCCESS("  - Učitelj 2: ucitelj2 (Janez Novak) / Ucitelj123! [MAT, FIZ]"))
        self.stdout.write(self.style.SUCCESS("  - Učitelj 3: ucitelj3 (Maja Horvat) / Ucitelj123! [SLO, ZGO]"))
        self.stdout.write(self.style.SUCCESS("  - Učitelj 4: ucitelj4 (Boris Jankovič) / Ucitelj123! [KEM, BIO]"))
        self.stdout.write(self.style.SUCCESS("  - Učitelj 5: ucitelj5 (Ana Kovačič) / Ucitelj123! [ANG, GEO, SPO]"))
        self.stdout.write(self.style.SUCCESS("  - Učenec 1: ucenec1 (Mitja Jančič - 3.A) / Ucenec123!"))
        self.stdout.write(self.style.SUCCESS("  - Učenec 2: ucenec2 (Nal Dobravc - 3.A) / Ucenec123!"))
        self.stdout.write(self.style.SUCCESS("  - Učenec 3: ucenec3 (Luka Kovač - 3.A) / Ucenec123!"))
        self.stdout.write(self.style.SUCCESS("  - Učenec 4: ucenec4 (Ema Podgoršek - 2.A) / Ucenec123!"))
        self.stdout.write(self.style.SUCCESS("  - Učenec 5: ucenec5 (Klemen Majcen - 1.A) / Ucenec123!"))
        self.stdout.write(self.style.SUCCESS("=================================================================="))
