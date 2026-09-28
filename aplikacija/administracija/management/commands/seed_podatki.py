import random

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

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

PREVOD_CRK = str.maketrans("čšžĆŠŽ", "cszCSZ")


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
    help = "Napolni bazo s testnimi podatki: 10 predmetov, 20 učiteljev, 100 učencev in njihove povezave."

    def add_arguments(self, parser):
        parser.add_argument(
            "--brez-brisanja",
            action="store_true",
            help="Ne pobriši obstoječih podatkov pred vnosom novih.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        faker = Faker("sl_SI")
        Faker.seed(42)
        random.seed(42)

        if not options["brez_brisanja"]:
            UcenecPredmet.objects.all().delete()
            UciteljPredmet.objects.all().delete()
            Ucenec.objects.all().delete()
            Ucitelj.objects.all().delete()
            Predmet.objects.all().delete()

        predmeti = [Predmet.objects.create(sifra=sifra, ime=ime) for sifra, ime in PREDMETI]
        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih {len(predmeti)} predmetov."))

        zasedeni_emaili = set()
        ucitelji = []
        for _ in range(20):
            ime, priimek = faker.first_name(), faker.last_name()
            ucitelj = Ucitelj.objects.create(
                ime=ime,
                priimek=priimek,
                email=v_email(ime, priimek, "solski-is.si", zasedeni_emaili),
            )
            ucitelji.append(ucitelj)

        # Vsak učitelj poučuje 1-3 predmete; zagotovimo, da ima vsak predmet vsaj enega učitelja.
        for ucitelj in ucitelji:
            izbrani = random.sample(predmeti, k=random.randint(1, 3))
            for predmet in izbrani:
                UciteljPredmet.objects.get_or_create(ucitelj=ucitelj, predmet=predmet)

        for predmet in predmeti:
            if not UciteljPredmet.objects.filter(predmet=predmet).exists():
                UciteljPredmet.objects.create(ucitelj=random.choice(ucitelji), predmet=predmet)

        # Zagotovimo vsaj en predmet z več učitelji in vsaj enega učitelja z več predmeti.
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[0], predmet=predmeti[0])
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[1], predmet=predmeti[0])
        UciteljPredmet.objects.get_or_create(ucitelj=ucitelji[0], predmet=predmeti[1])

        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih {len(ucitelji)} učiteljev in njihove povezave s predmeti."))

        ucenci = []
        for _ in range(100):
            ime, priimek = faker.first_name(), faker.last_name()
            ucenec = Ucenec.objects.create(
                ime=ime,
                priimek=priimek,
                email=v_email(ime, priimek, "dijaki.solski-is.si", zasedeni_emaili),
            )
            ucenci.append(ucenec)

        # Vsak učenec obiskuje 2-5 predmetov (zahteva: več kot en predmet na učenca).
        for ucenec in ucenci:
            izbrani = random.sample(predmeti, k=random.randint(2, 5))
            for predmet in izbrani:
                UcenecPredmet.objects.get_or_create(ucenec=ucenec, predmet=predmet)

        self.stdout.write(self.style.SUCCESS(f"Ustvarjenih {len(ucenci)} učencev in njihove povezave s predmeti."))
        self.stdout.write(self.style.SUCCESS("Testni podatki uspešno vneseni."))
