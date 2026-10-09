"""Sistematični testi administratorskega pogleda (5. teden).

Pokrivajo CRUD in validacijo za predmete, učitelje in učence ter relacije
učitelj–predmet in učenec–predmet prek uporabniškega vmesnika.
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from portal.models import Profil

from .models import Predmet, Ucenec, Ucitelj


def prijavi_admina(client):
    user = User.objects.create_user("admin", password="Admin12345", is_staff=True, is_superuser=True)
    Profil.objects.create(uporabnik=user, vloga=Profil.Vloga.ADMIN)
    client.login(username="admin", password="Admin12345")
    return user


class AdminPredmetTest(TestCase):
    def setUp(self):
        prijavi_admina(self.client)

    def test_seznam(self):
        Predmet.objects.create(sifra="MAT", ime="Matematika")
        odgovor = self.client.get(reverse("predmet_seznam"))
        self.assertEqual(odgovor.status_code, 200)
        self.assertContains(odgovor, "Matematika")

    def test_dodaj(self):
        odgovor = self.client.post(
            reverse("predmet_dodaj"), {"sifra": "FIZ", "ime": "Fizika", "opis": ""}
        )
        self.assertEqual(odgovor.status_code, 302)
        self.assertTrue(Predmet.objects.filter(sifra="FIZ").exists())

    def test_uredi(self):
        p = Predmet.objects.create(sifra="KEM", ime="Kemija")
        self.client.post(reverse("predmet_uredi", args=[p.pk]), {"sifra": "KEM", "ime": "Kemija II", "opis": ""})
        p.refresh_from_db()
        self.assertEqual(p.ime, "Kemija II")

    def test_izbrisi(self):
        p = Predmet.objects.create(sifra="BIO", ime="Biologija")
        self.client.post(reverse("predmet_izbrisi", args=[p.pk]))
        self.assertFalse(Predmet.objects.filter(pk=p.pk).exists())

    def test_podvojena_sifra_zavrnjena(self):
        Predmet.objects.create(sifra="MAT", ime="Matematika")
        odgovor = self.client.post(reverse("predmet_dodaj"), {"sifra": "MAT", "ime": "Druga", "opis": ""})
        self.assertEqual(odgovor.status_code, 200)  # ostane na obrazcu z napako
        self.assertEqual(Predmet.objects.filter(sifra="MAT").count(), 1)


class AdminUciteljUcenecTest(TestCase):
    def setUp(self):
        prijavi_admina(self.client)
        self.mat = Predmet.objects.create(sifra="MAT", ime="Matematika")
        self.slo = Predmet.objects.create(sifra="SLO", ime="Slovenščina")

    def test_dodaj_ucitelja_z_vec_predmeti(self):
        odgovor = self.client.post(
            reverse("ucitelj_dodaj"),
            {"ime": "Ana", "priimek": "Kovač", "email": "ana@solski-is.si",
             "predmeti": [self.mat.pk, self.slo.pk]},
        )
        self.assertEqual(odgovor.status_code, 302)
        u = Ucitelj.objects.get(email="ana@solski-is.si")
        self.assertEqual(u.predmeti.count(), 2)

    def test_dodaj_ucenca_zahteva_vsaj_en_predmet(self):
        # Brez predmeta -> validacijska napaka, učenec ni ustvarjen.
        odgovor = self.client.post(
            reverse("ucenec_dodaj"),
            {"ime": "Bine", "priimek": "Novak", "email": "bine@dijaki.si", "predmeti": []},
        )
        self.assertEqual(odgovor.status_code, 200)
        self.assertFalse(Ucenec.objects.filter(email="bine@dijaki.si").exists())

    def test_dodaj_ucenca_z_enim_predmetom(self):
        odgovor = self.client.post(
            reverse("ucenec_dodaj"),
            {"ime": "Cilka", "priimek": "Zajc", "email": "cilka@dijaki.si", "predmeti": [self.mat.pk]},
        )
        self.assertEqual(odgovor.status_code, 302)
        self.assertTrue(Ucenec.objects.filter(email="cilka@dijaki.si").exists())

    def test_uredi_ucencu_predmete(self):
        u = Ucenec.objects.create(ime="Dana", priimek="Horvat", email="dana@dijaki.si")
        u.predmeti.add(self.mat)
        self.client.post(
            reverse("ucenec_uredi", args=[u.pk]),
            {"ime": "Dana", "priimek": "Horvat", "email": "dana@dijaki.si", "predmeti": [self.slo.pk]},
        )
        self.assertEqual(list(u.predmeti.values_list("sifra", flat=True)), ["SLO"])
