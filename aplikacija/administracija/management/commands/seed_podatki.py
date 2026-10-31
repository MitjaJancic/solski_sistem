import random

from django.core.management.base import BaseCommand
from django.db import transaction

from administracija.models import Predmet, Ucenec, UcenecPredmet, Ucitelj, UciteljPredmet

# 10 predmetov (zahteva: najmanj 10)
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

# 20 učiteljev (zahteva: najmanj 20; nekateri predmeti več učiteljev, nekateri učitelji več predmetov)
UCITELJI = [
    ("Matic", "Holobar", "matic.holobar@solski-is.si", ["INF", "MAT"]),
    ("Janez", "Novak", "janez.novak@solski-is.si", ["MAT", "FIZ"]),
    ("Maja", "Horvat", "maja.horvat@solski-is.si", ["SLO", "ZGO"]),
    ("Boris", "Jankovič", "boris.jankovic@solski-is.si", ["KEM", "BIO"]),
    ("Ana", "Kovačič", "ana.kovacic@solski-is.si", ["ANG", "GEO"]),
    ("Peter", "Krajnc", "peter.krajnc@solski-is.si", ["INF", "FIZ"]),
    ("Luka", "Zupan", "luka.zupan@solski-is.si", ["MAT", "INF"]),
    ("Mojca", "Potočnik", "mojca.potocnik@solski-is.si", ["SLO", "ANG"]),
    ("Andrej", "Vidmar", "andrej.vidmar@solski-is.si", ["ZGO", "GEO"]),
    ("Tanja", "Kos", "tanja.kos@solski-is.si", ["BIO", "KEM"]),
    ("Robert", "Golob", "robert.golob@solski-is.si", ["FIZ", "MAT"]),
    ("Irena", "Turk", "irena.turk@solski-is.si", ["SLO", "SPO"]),
    ("Aleš", "Mlakar", "ales.mlakar@solski-is.si", ["SPO", "GEO"]),
    ("Katarina", "Hrovat", "katarina.hrovat@solski-is.si", ["ANG", "ZGO"]),
    ("Tomaž", "Kralj", "tomaz.kralj@solski-is.si", ["INF", "MAT"]),
    ("Simona", "Leban", "simona.leban@solski-is.si", ["BIO", "KEM"]),
    ("Gregor", "Rozman", "gregor.rozman@solski-is.si", ["FIZ", "INF"]),
    ("Vesna", "Korošec", "vesna.korosec@solski-is.si", ["SLO", "ANG"]),
    ("Bojan", "Rus", "bojan.rus@solski-is.si", ["SPO", "BIO"]),
    ("Nataša", "Zorko", "natasa.zorko@solski-is.si", ["KEM", "GEO"]),
]

# 120 učencev razporejenih v 4 razrede po 30 učencev (zahteva: najmanj 100)
RAZREDI_UCENCI = {
    "4.A": [
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
    "3.A": [
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
    "2.A": [
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
        ("Marcel", "Kladnik"),
        ("Tia", "Robnik"),
        ("Goran", "Cestnik"),
        ("Karin", "Verbič"),
        ("Erik", "Selan"),
        ("Iza", "Cerar"),
        ("Andraž", "Kren"),
        ("Gaja", "Vrhovnik"),
        ("Dejan", "Oprešnik"),
        ("Živa", "Vidic"),
        ("Sandi", "Pirc"),
        ("Sandra", "Krajnc"),
        ("Jernej", "Medvešek"),
        ("Rebeka", "Godec"),
        ("Boštjan", "Brečko"),
        ("Tamara", "Kregar"),
    ],
    "1.A": [
        ("Alen", "Potočnik"),
        ("Barbara", "Vidmar"),
        ("Ciril", "Kos"),
        ("Darja", "Golob"),
        ("Emil", "Turk"),
        ("Franja", "Kralj"),
        ("Gorazd", "Božič"),
        ("Helena", "Korošec"),
        ("Igor", "Zupan"),
        ("Jasna", "Bizjak"),
        ("Kristjan", "Horvat"),
        ("Lucija", "Rus"),
        ("Marko", "Rozman"),
        ("Nada", "Kastelic"),
        ("Ožbej", "Kotnik"),
        ("Polona", "Sever"),
        ("Rado", "Petek"),
        ("Sonja", "Oblak"),
        ("Tomi", "Uršič"),
        ("Urška", "Jagodnik"),
        ("Val", "Leban"),
        ("Zarja", "Breznik"),
        ("Anja", "Močnik"),
        ("Boris", "Perko"),
        ("Cene", "Pečnik"),
        ("Daša", "Dolenc"),
        ("Edvard", "Jeras"),
        ("Flora", "Podgoršek"),
        ("Gašper", "Lesjak"),
        ("Heda", "Tratnik"),
    ],
}

PREDMETNIK_PO_RAZREDIH = {
    "1.A": ["SLO", "MAT", "ANG", "INF", "BIO", "GEO", "SPO"],
    "2.A": ["SLO", "MAT", "ANG", "INF", "FIZ", "KEM", "ZGO", "SPO"],
    "3.A": ["SLO", "MAT", "ANG", "INF", "FIZ", "KEM", "BIO", "ZGO"],
    "4.A": ["SLO", "MAT", "ANG", "INF", "FIZ", "KEM", "BIO", "ZGO"],
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
        "Napolni bazo z natanko zahtevanimi podatki: 10 predmetov, 20 učiteljev (z večpredmetnimi "
        "relacijami) in 120 učenci v 4 razredih (vsak z več predmeti)."
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

        # 1. 10 Predmetov
        predmeti = [
            Predmet.objects.create(sifra=sifra, ime=ime, opis=opis)
            for sifra, ime, opis in PREDMETI
        ]
        predmet_po_sifri = {p.sifra: p for p in predmeti}
        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih {len(predmeti)} predmetov."))

        # 2. 20 Učiteljev z relacijami učitelj-predmet
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
                f"Ustvarjenih {len(ucitelji)} učiteljev (vsak uči 2-3 predmete, vsak predmet ima več učiteljev)."
            )
        )

        # 3. 120 Učencev (4 razredi po 30) z relacijami učenec-predmet (>1 predmet)
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
                    f"Razred {razred}: {len(ucenci_seznam)} učencev vpisanih v {len(predmeti_razreda)} predmetov."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nTestni podatki administracije uspešno vneseni:\n"
                f"- Predmetov: {len(predmeti)} (zahteva >= 10)\n"
                f"- Učiteljev: {len(ucitelji)} (zahteva >= 20, z večpredmetnimi povezavami)\n"
                f"- Učencev: {skupaj_ucencev} (zahteva >= 100, vsak obiskuje >1 predmet)\n"
                f"- Skupaj vpisov v predmete: {skupaj_vpisov}"
            )
        )
