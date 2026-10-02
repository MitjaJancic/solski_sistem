"""Ustvari demo uporabniške račune za prijavo (4. teden).

Poveže Djangove uporabnike (z zgoščenimi gesli) z obstoječimi zapisi učiteljev
in učencev iz `seed_podatki`. Namenjeno predstavitvi in testiranju avtorizacije.

Uporaba:
    python manage.py seed_podatki
    python manage.py seed_uporabniki

Ustvari:
    - administratorja:  admin / Admin123!
    - 3 učitelje:       ucitelj1..3 / Ucitelj123!  (povezani s prvimi 3 učitelji)
    - 3 učence:         ucenec1..3 / Ucenec123!    (povezani s prvimi 3 učenci)
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from administracija.models import Ucenec, Ucitelj
from portal.models import Profil

GESLO_ADMIN = "Admin123!"
GESLO_UCITELJ = "Ucitelj123!"
GESLO_UCENEC = "Ucenec123!"


class Command(BaseCommand):
    help = "Ustvari demo račune (admin, učitelji, učenci) za prijavo in avtorizacijo."

    @transaction.atomic
    def handle(self, *args, **options):
        # Administrator
        admin, ustvarjen = User.objects.get_or_create(
            username="admin", defaults={"email": "admin@solski-is.si", "is_staff": True, "is_superuser": True}
        )
        admin.set_password(GESLO_ADMIN)
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        Profil.objects.update_or_create(uporabnik=admin, defaults={"vloga": Profil.Vloga.ADMIN})
        self.stdout.write(self.style.SUCCESS("Administrator: admin / " + GESLO_ADMIN))

        # Učitelji (prvi 3 iz baze)
        for i, ucitelj in enumerate(Ucitelj.objects.all()[:3], start=1):
            uporabnik, _ = User.objects.get_or_create(
                username=f"ucitelj{i}", defaults={"email": ucitelj.email}
            )
            uporabnik.set_password(GESLO_UCITELJ)
            uporabnik.save()
            Profil.objects.update_or_create(
                uporabnik=uporabnik,
                defaults={"vloga": Profil.Vloga.UCITELJ, "ucitelj": ucitelj},
            )
            self.stdout.write(self.style.SUCCESS(f"Učitelj: ucitelj{i} / {GESLO_UCITELJ} -> {ucitelj}"))

        # Učenci (prvi 3 iz baze)
        for i, ucenec in enumerate(Ucenec.objects.all()[:3], start=1):
            uporabnik, _ = User.objects.get_or_create(
                username=f"ucenec{i}", defaults={"email": ucenec.email}
            )
            uporabnik.set_password(GESLO_UCENEC)
            uporabnik.save()
            Profil.objects.update_or_create(
                uporabnik=uporabnik,
                defaults={"vloga": Profil.Vloga.UCENEC, "ucenec": ucenec},
            )
            self.stdout.write(self.style.SUCCESS(f"Učenec: ucenec{i} / {GESLO_UCENEC} -> {ucenec}"))

        self.stdout.write(self.style.SUCCESS("Demo računi uspešno ustvarjeni."))
