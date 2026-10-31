import random

from django.core.management.base import BaseCommand
from django.db import transaction

from administracija.models import Predmet, Ucenec, UcenecPredmet, Ucitelj, UciteljPredmet

PREDMETI = [
    ("INF", "Informatika", "Programiranje, relacijske baze podatkov, omrežja in spletni sistemi."),
    ("MAT", "Matematika", "Algebra, funkcije, geometrija, računski postopki in verjetnost."),
    ("FIZ", "Fizika", "Mehanika, kinematika, gravitacija, elektromagnetizem in meritve."),
    ("SLO", "Slovenščina", "Slovenski jezik, književnost, pravopis, eseji in interpretacija besedil."),
    ("ZGO", "Zgodovina", "Slovenska in svetovna zgodovina od antike do sodobnosti."),
    ("KEM", "Kemija", "Splošna, anorganska in organska kemija, stehiometrija in laboratorijske vaje."),
    ("BIO", "Biologija", "Citologija, genetika, botanika, zoologija in ekologija."),
    ("ANG", "Angleščina", "Angleški jezik, slovnica, besedišče, komunikacija in esejistika."),
    ("GEO", "Geografija", "Fizična, družbena in regionalna geografija sveta in Slovenije."),
    ("SPO", "Šport", "Telesna vzgoja, motorične spretnosti, timski športi in zdrav življenjski slog."),
]

# 5 učiteljev - vsak poučuje različne predmete brez prekrivanja
UCITELJI = [
    ("Matic", "Holobar", "matic.holobar@solski-is.si", ["INF"]),
    ("Janez", "Novak", "janez.novak@solski-is.si", ["MAT", "FIZ"]),
    ("Maja", "Horvat", "maja.horvat@solski-is.si", ["SLO", "ZGO"]),
    ("Boris", "Jankovič", "boris.jankovic@solski-is.si", ["KEM", "BIO"]),
    ("Ana", "Kovačič", "ana.kovacic@solski-is.si", ["ANG", "GEO", "SPO"]),
]

# 3 razredi x 30 učencev = točno 90 učencev z resničnimi slovenskimi imeni
RAZREDI_UCENCI = {
    "3.A": [
        ("Mitja", "Jančič"),
        ("Nal", "Dobravc"),
        ("Luka", "Kovač"),
        ("Ana", "Novak"),
        ("Jan", "Zupančič"),
        ("Sara", "Hrovat"),
        ("Žiga", "Kralj"),
        ("Maja", "Turk"),
        ("Nejc", "Bizjak"),
        ("Eva", "Mlakar"),
        ("Anže", "Leban"),
        ("Klara", "Rozman"),
        ("Timotej", "Božič"),
        ("Nika", "Korošec"),
        ("David", "Rus"),
        ("Lara", "Zorko"),
        ("Matej", "Kastelic"),
        ("Nina", "Oblak"),
        ("Jaka", "Sever"),
        ("Pia", "Knez"),
        ("Matic", "Kotnik"),
        ("Tjaša", "Breznik"),
        ("Domen", "Petek"),
        ("Lucija", "Kos"),
        ("Filip", "Jagodnik"),
        ("Zoja", "Uršič"),
        ("Miha", "Perko"),
        ("Tina", "Dolenc"),
        ("Vid", "Pečnik"),
        ("Hana", "Močnik"),
    ],
    "2.A": [
        ("Rok", "Jeras"),
        ("Ema", "Podgoršek"),
        ("Urban", "Lesjak"),
        ("Lana", "Železnik"),
        ("Blaž", "Tratnik"),
        ("Zala", "Pavlič"),
        ("Gašper", "Hočevar"),
        ("Kaja", "Gale"),
        ("Tilen", "Ribič"),
        ("Lea", "Erjavec"),
        ("Aljaž", "Jerman"),
        ("Maša", "Jamnik"),
        ("Jakob", "Kočevar"),
        ("Mia", "Gregorič"),
        ("Gal", "Černe"),
        ("Ajda", "Čeh"),
        ("Lovro", "Kolar"),
        ("Laura", "Pintar"),
        ("Simon", "Primožič"),
        ("Teja", "Hribar"),
        ("Bor", "Marolt"),
        ("Patricija", "Kokalj"),
        ("Mark", "Rožič"),
        ("Neli", "Vovk"),
        ("Tadej", "Šinkovec"),
        ("Julija", "Kavčič"),
        ("Gregor", "Tavčar"),
        ("Veronika", "Čuk"),
        ("Peter", "Bele"),
        ("Nuša", "Logar"),
    ],
    "1.A": [
        ("Klemen", "Majcen"),
        ("Špela", "Humar"),
        ("Primož", "Jenko"),
        ("Danaja", "Kraljič"),
        ("Denis", "Skok"),
        ("Tinkara", "Blažič"),
        ("Martin", "Jereb"),
        ("Iris", "Zorman"),
        ("Aleksander", "Kumperger"),
        ("Brina", "Dolinar"),
        ("Leon", "Završnik"),
        ("Nastja", "Koželj"),
        ("Samo", "Češarek"),
        ("Ela", "Grobelnik"),
        ("Marcel", "Knez"),
        ("Tia", "Kladnik"),
        ("Goran", "Cestnik"),
        ("Karin", "Robnik"),
        ("Erik", "Verbič"),
        ("Iza", "Selan"),
        ("Andraž", "Cerar"),
        ("Gaja", "Kren"),
        ("Dejan", "Vrhovnik"),
        ("Živa", "Oprešnik"),
        ("Sandi", "Vidic"),
        ("Sandra", "Pirc"),
        ("Jernej", "Krajnc"),
        ("Rebeka", "Medvešek"),
        ("Boštjan", "Godec"),
        ("Tamara", "Brečko"),
    ],
}

# Predmetnik po letnikih (smiselna razporeditev)
PREDMETNIK_PO_RAZREDIH = {
    "1.A": ["SLO", "MAT", "ANG", "INF", "BIO", "GEO", "SPO"],
    "2.A": ["SLO", "MAT", "ANG", "INF", "FIZ", "KEM", "ZGO", "SPO"],
    "3.A": ["SLO", "MAT", "ANG", "INF", "FIZ", "KEM", "BIO", "ZGO"],
}

PREVOD_CRK = str.maketrans("čžšČŽŠ", "czsCZS")


def v_email(ime, priimek, domena, zasedeni):
    osnova = f"{ime}.{priimek}".lower().translate(PREVOD_CRK)
    email = f"{osnova}@{domena}"
    stevec = 1
    while email in zasedeni:
        stevec += 1
        email = f"{osnova}{stevec}@{domena}"
    zasedeni.add(email)
    return email


class Command(BaseCommand):
    help = (
        "Vnese strukturirane testne podatke: 10 predmetov, natanko 5 učiteljev z različnimi predmeti, "
        "3 razrede (1.A, 2.A, 3.A) z natanko 30 učenci vsak (skupaj 90 učencev) ter ustrezne relacije."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--brez-brisanja",
            action="store_true",
            help="Ne pobriši obstoječih podatkov pred vnosom novih.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)

        if not options["brez_brisanja"]:
            UcenecPredmet.objects.all().delete()
            UciteljPredmet.objects.all().delete()
            Ucenec.objects.all().delete()
            Ucitelj.objects.all().delete()
            Predmet.objects.all().delete()

        # 1. Predmeti
        predmeti = [
            Predmet.objects.create(sifra=sifra, ime=ime, opis=opis)
            for sifra, ime, opis in PREDMETI
        ]
        predmet_po_sifri = {p.sifra: p for p in predmeti}
        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih {len(predmeti)} predmetov."))

        # 2. Točno 5 učiteljev z različnimi predmeti
        zasedeni_emaili = set()
        ucitelji = []
        for ime, priimek, email, dodeljeni_predmeti in UCITELJI:
            zasedeni_emaili.add(email)
            ucitelj = Ucitelj.objects.create(
                ime=ime,
                priimek=priimek,
                email=email,
            )
            for sifra in dodeljeni_predmeti:
                UciteljPredmet.objects.create(ucitelj=ucitelj, predmet=predmet_po_sifri[sifra])
            ucitelji.append(ucitelj)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Učitelj: {ucitelj.ime} {ucitelj.priimek} ({ucitelj.email}) -> predmeti: {', '.join(dodeljeni_predmeti)}"
                )
            )

        # 3. Točno 3 razredi po 30 učencev (skupaj 90)
        skupaj_ucencev = 0
        skupaj_vpisov = 0
        for razred, ucenci_seznam in RAZREDI_UCENCI.items():
            predmeti_razreda = PREDMETNIK_PO_RAZREDIH[razred]
            for ime, priimek in ucenci_seznam:
                email = v_email(ime, priimek, "dijaki.solski-is.si", zasedeni_emaili)
                ucenec = Ucenec.objects.create(
                    ime=ime,
                    priimek=priimek,
                    email=email,
                    razred=razred,
                )
                skupaj_ucencev += 1
                for sifra in predmeti_razreda:
                    UcenecPredmet.objects.create(ucenec=ucenec, predmet=predmet_po_sifri[sifra])
                    skupaj_vpisov += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Razred {razred}: ustvarjenih {len(ucenci_seznam)} učencev, vpisani v: {', '.join(predmeti_razreda)}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nTestni podatki uspešno vneseni:\n"
                f"- Predmetov: {len(predmeti)}\n"
                f"- Učiteljev: {len(ucitelji)} (vsak uči različne predmete)\n"
                f"- Razredov: {len(RAZREDI_UCENCI)} (1.A, 2.A, 3.A)\n"
                f"- Učencev: {skupaj_ucencev} (30 na razred)\n"
                f"- Vpisov v predmete: {skupaj_vpisov}"
            )
        )
