import random

from django.core.management.base import BaseCommand
from django.db import transaction

from administracija.models import Predmet, Ucenec, UcenecPredmet, Ucitelj, UciteljPredmet

PREDMETI = [
    ("MAT", "Matematika"),
    ("SLO", "Slovenščina"),
    ("ANG", "Angleščina"),
    ("ZGO", "Zgodovina"),
    ("GEO", "Geografija"),
    ("BIO", "Biologija"),
    ("KEM", "Kemija"),
    ("FIZ", "Fizika"),
    ("SPO", "Šport"),
    ("INF", "Informatika"),
]

UCITELJI_IMENA = [
    ("Matic", "Holobar"),
    ("Janez", "Novak"),
    ("Maja", "Horvat"),
    ("Peter", "Krajnc"),
    ("Ana", "Kovačič"),
    ("Luka", "Zupan"),
    ("Mojca", "Potočnik"),
    ("Andrej", "Vidmar"),
    ("Tanja", "Kos"),
    ("Robert", "Golob"),
    ("Irena", "Turk"),
    ("Aleš", "Mlakar"),
    ("Katarina", "Hrovat"),
    ("Tomaž", "Kralj"),
    ("Simona", "Leban"),
    ("Gregor", "Rozman"),
    ("Vesna", "Korošec"),
    ("Bojan", "Rus"),
    ("Nataša", "Zorko"),
    ("Marko", "Kastelic"),
]

UCENCI_IMENA = [
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
    ("Jakob", "Pavlič"),
    ("Hana", "Zalar"),
    ("Gal", "Vidic"),
    ("Zala", "Pečnik"),
    ("Rok", "Močnik"),
    ("Maša", "Dolenc"),
    ("Aljaž", "Erjavec"),
    ("Teja", "Hočevar"),
    ("Miha", "Jamnik"),
    ("Tinkara", "Kovač"),
    ("Lan", "Medved"),
    ("Lea", "Pirc"),
    ("Urban", "Šturm"),
    ("Lana", "Žagar"),
    ("Lovro", "Kalan"),
    ("Ela", "Ravnikar"),
    ("Tilen", "Čeh"),
    ("Ema", "Debeljak"),
    ("Gašper", "Kočevar"),
    ("Julija", "Jerman"),
    ("Vid", "Ribič"),
    ("Neža", "Primožič"),
    ("Blaž", "Rožič"),
    ("Veronika", "Cvelbar"),
    ("Aleksander", "Gregorič"),
    ("Karin", "Suhadolc"),
    ("Marcel", "Pintar"),
    ("Patricija", "Kolar"),
    ("Leon", "Gomboc"),
    ("Danaja", "Marolt"),
    ("Bor", "Vovk"),
    ("Iris", "Trček"),
    ("Nik", "Grošelj"),
    ("Ajda", "Oprešnik"),
    ("Martin", "Šuštar"),
    ("Rebeka", "Tavčar"),
    ("Erik", "Vindiš"),
    ("Gaja", "Prah"),
    ("Maj", "Jenko"),
    ("Stella", "Zadravec"),
    ("Val", "Cerar"),
    ("Tara", "Černe"),
    ("Liam", "Gradišar"),
    ("Iza", "Kastelec"),
    ("Maks", "Lipovec"),
    ("Vita", "Ostanek"),
    ("Oskar", "Bele"),
    ("Zarja", "Perko"),
    ("Rene", "Sitar"),
    ("Brina", "Starič"),
    ("Teo", "Štucin"),
    ("Loti", "Tomšič"),
    ("Jon", "Valentinčič"),
    ("Lina", "Zadnik"),
    ("Ian", "Žitnik"),
    ("Mia", "Arko"),
    ("Sven", "Dolenec"),
    ("Tia", "Fras"),
    ("Noel", "Gregorc"),
    ("Alina", "Hribar"),
    ("Lev", "Jerič"),
    ("Mila", "Kopač"),
    ("Tristan", "Lukić"),
    ("Rubi", "Maver"),
    ("Oliver", "Pevec"),
    ("Ela", "Smole"),
    ("Liam", "Šolar"),
    ("Lili", "Tratnik"),
    ("Noel", "Vovko"),
    ("Zoja", "Zabukovec"),
    ("Tim", "Železnik"),
    ("Kaja", "Zupan"),
    ("Jan", "Žibert"),
    ("Hana", "Žnidaršič"),
]

PREVOD_CRK = str.maketrans("čšžćđČŠŽĆĐ", "cszcdCSZCD")


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
    help = "Napolni bazo z dejanskimi testnimi podatki: 10 predmetov, 20 učiteljev, 100 učencev in njihove relacije."

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

        predmeti = [Predmet.objects.create(sifra=sifra, ime=ime) for sifra, ime in PREDMETI]
        predmet_po_sifri = {p.sifra: p for p in predmeti}
        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih {len(predmeti)} predmetov."))

        zasedeni_emaili = set()
        ucitelji = []
        for ime, priimek in UCITELJI_IMENA:
            ucitelj = Ucitelj.objects.create(
                ime=ime,
                priimek=priimek,
                email=v_email(ime, priimek, "solski-is.si", zasedeni_emaili),
            )
            ucitelji.append(ucitelj)

        # Matic Holobar (mentor) poučuje Informatiko in Matematiko
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[0], predmet=predmet_po_sifri["INF"])
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[0], predmet=predmet_po_sifri["MAT"])

        # Janez Novak poučuje Matematiko in Fiziko
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[1], predmet=predmet_po_sifri["MAT"])
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[1], predmet=predmet_po_sifri["FIZ"])

        # Maja Horvat poučuje Slovenščino in Zgodovino
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[2], predmet=predmet_po_sifri["SLO"])
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[2], predmet=predmet_po_sifri["ZGO"])

        # Peter Krajnc poučuje Informatiko in Fiziko
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[3], predmet=predmet_po_sifri["INF"])
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[3], predmet=predmet_po_sifri["FIZ"])

        # Ana Kovačič poučuje Angleščino
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[4], predmet=predmet_po_sifri["ANG"])

        # Preostali učitelji poučujejo 1-3 naključne predmete
        for ucitelj in ucitelji[5:]:
            izbrani = random.sample(predmeti, k=random.randint(1, 3))
            for predmet in izbrani:
                UciteljPredmet.objects.get_or_create(ucitelj=ucitelj, predmet=predmet)

        # Zagotovimo, da ima vsak predmet vsaj enega učitelja
        for predmet in predmeti:
            if not UciteljPredmet.objects.filter(predmet=predmet).exists():
                UciteljPredmet.objects.create(ucitelj=random.choice(ucitelji), predmet=predmet)

        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih {len(ucitelji)} učiteljev (prvi: {ucitelji[0]}) in njihove povezave."))

        ucenci = []
        for ime, priimek in UCENCI_IMENA:
            ucenec = Ucenec.objects.create(
                ime=ime,
                priimek=priimek,
                email=v_email(ime, priimek, "dijaki.solski-is.si", zasedeni_emaili),
            )
            ucenci.append(ucenec)

        # Mitja Jančič (učenec 1) obiskuje MAT, FIZ, SLO, INF, ANG
        for s in ["MAT", "FIZ", "SLO", "INF", "ANG"]:
            UcenecPredmet.objects.get_or_create(ucenec=ucenci[0], predmet=predmet_po_sifri[s])

        # Nal Dobravc (učenec 2) obiskuje MAT, SLO, INF, ZGO, SPO
        for s in ["MAT", "SLO", "INF", "ZGO", "SPO"]:
            UcenecPredmet.objects.get_or_create(ucenec=ucenci[1], predmet=predmet_po_sifri[s])

        # Preostali učenci obiskujejo med 2 in 5 predmetov (zahteva: vsak >1 predmet)
        for ucenec in ucenci[2:]:
            izbrani = random.sample(predmeti, k=random.randint(2, 5))
            for predmet in izbrani:
                UcenecPredmet.objects.get_or_create(ucenec=ucenec, predmet=predmet)

        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih {len(ucenci)} učencev (prva: {ucenci[0]}, {ucenci[1]}) in relacije."))
        self.stdout.write(self.style.SUCCESS("--- TESTNI PODATKI Z DEJANSKIMI IMENI IN PRIIMKI USPEŠNO VNESENI ---"))
