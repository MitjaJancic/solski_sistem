import shutil
import tempfile

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from administracija.models import (
    Predmet,
    Ucenec,
    UcenecPredmet,
    Ucitelj,
    UciteljPredmet,
)

from .models import Gradivo, Oddaja, Profil

MEDIA = tempfile.mkdtemp()


def dodaj_profil(username, geslo, vloga, ucitelj=None, ucenec=None, **extra):
    user = User.objects.create_user(username=username, password=geslo, **extra)
    Profil.objects.create(uporabnik=user, vloga=vloga, ucitelj=ucitelj, ucenec=ucenec)
    return user


@override_settings(MEDIA_ROOT=MEDIA)
class PortalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mat = Predmet.objects.create(sifra="MAT", ime="Matematika")
        cls.slo = Predmet.objects.create(sifra="SLO", ime="Slovenščina")

        cls.ucitelj = Ucitelj.objects.create(ime="Ana", priimek="Kovač", email="ana@solski-is.si")
        UciteljPredmet.objects.create(ucitelj=cls.ucitelj, predmet=cls.mat)  # poučuje MAT, ne SLO

        cls.ucenec = Ucenec.objects.create(ime="Bine", priimek="Novak", email="bine@dijaki.si")
        UcenecPredmet.objects.create(ucenec=cls.ucenec, predmet=cls.mat)  # obiskuje MAT, ne SLO

        cls.ucenec2 = Ucenec.objects.create(ime="Cilka", priimek="Zajc", email="cilka@dijaki.si")
        UcenecPredmet.objects.create(ucenec=cls.ucenec2, predmet=cls.mat)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    # --- Avtentikacija / avtorizacija -----------------------------------

    def test_anonimni_preusmerjen_iz_admin_crud(self):
        odgovor = self.client.get(reverse("predmet_seznam"))
        self.assertEqual(odgovor.status_code, 302)
        self.assertIn("/prijava/", odgovor.url)

    def test_ucenec_ne_dostopa_do_admin_crud(self):
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        odgovor = self.client.get(reverse("predmet_seznam"))
        self.assertEqual(odgovor.status_code, 403)

    def test_admin_dostopa_do_crud(self):
        dodaj_profil("a1", "geslo12345", Profil.Vloga.ADMIN, is_staff=True, is_superuser=True)
        self.client.login(username="a1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("predmet_seznam")).status_code, 200)

    # --- Registracija in zgoščevanje gesla ------------------------------

    def test_registracija_ucenca_in_zgosceno_geslo(self):
        odgovor = self.client.post(
            reverse("registracija"),
            {
                "username": "novi",
                "ime": "Dana",
                "priimek": "Horvat",
                "email": "dana@dijaki.si",
                "password1": "MocnoGeslo123",
                "password2": "MocnoGeslo123",
            },
        )
        self.assertEqual(odgovor.status_code, 302)
        user = User.objects.get(username="novi")
        # Geslo je shranjeno zgoščeno (nikoli v čistem besedilu).
        self.assertNotEqual(user.password, "MocnoGeslo123")
        self.assertTrue(user.password.startswith(("pbkdf2_", "argon2")))
        self.assertTrue(check_password("MocnoGeslo123", user.password))
        self.assertTrue(Ucenec.objects.filter(email="dana@dijaki.si").exists())
        self.assertEqual(user.profil.vloga, Profil.Vloga.UCENEC)

    # --- Učenec: predmeti in gradiva ------------------------------------

    def test_ucenec_ureja_svoje_predmete(self):
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        self.client.post(reverse("moji_predmeti"), {"predmeti": [self.slo.pk]})
        self.assertTrue(UcenecPredmet.objects.filter(ucenec=self.ucenec, predmet=self.slo).exists())
        self.assertFalse(UcenecPredmet.objects.filter(ucenec=self.ucenec, predmet=self.mat).exists())

    def test_ucenec_ne_vidi_gradiv_nevpisanega_predmeta(self):
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("ucenec_gradiva", args=[self.mat.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("ucenec_gradiva", args=[self.slo.pk])).status_code, 403)

    # --- Učitelj: gradiva samo za svoje predmete ------------------------

    def test_ucitelj_nalozi_gradivo_le_za_svoj_predmet(self):
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        datoteka = SimpleUploadedFile("g.txt", b"vsebina", content_type="text/plain")
        odgovor = self.client.post(
            reverse("gradivo_nalozi"),
            {"predmet": self.mat.pk, "naslov": "Ulomki", "datoteka": datoteka},
        )
        self.assertEqual(odgovor.status_code, 302)
        self.assertTrue(Gradivo.objects.filter(predmet=self.mat, naslov="Ulomki").exists())

    def test_ucitelj_ne_more_nalagati_za_tuj_predmet(self):
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        datoteka = SimpleUploadedFile("g.txt", b"vsebina", content_type="text/plain")
        # SLO ni med predmeti tega učitelja → obrazec zavrne izbiro (ostane na strani).
        odgovor = self.client.post(
            reverse("gradivo_nalozi"),
            {"predmet": self.slo.pk, "naslov": "Vrinjeno", "datoteka": datoteka},
        )
        self.assertEqual(odgovor.status_code, 200)
        self.assertFalse(Gradivo.objects.filter(predmet=self.slo).exists())

    def test_ucitelj_vidi_le_svoje_predmete(self):
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        vsebina = self.client.get(reverse("ucitelj_predmeti")).content.decode()
        self.assertIn("Matematika", vsebina)
        self.assertNotIn("Slovenščina", vsebina)
        self.assertEqual(self.client.get(reverse("ucitelj_predmet", args=[self.slo.pk])).status_code, 403)

    # --- Oddaja nalog: poimenovanje + potrditev povozitve ----------------

    def test_oddaja_poimenovanje_datoteke(self):
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        datoteka = SimpleUploadedFile("moja.docx", b"v1", content_type="application/octet-stream")
        self.client.post(
            reverse("oddaja_nova"),
            {"predmet": self.mat.pk, "naslov": "1. domača", "datoteka": datoteka},
        )
        oddaja = Oddaja.objects.get(ucenec=self.ucenec, predmet=self.mat, naslov="1. domača")
        # Datoteka shranjena kot "Priimek Ime – Naslov naloge.ext"
        self.assertTrue(oddaja.datoteka.name.endswith("Novak Bine – 1. domača.docx"))

    def test_ponovna_oddaja_zahteva_potrditev_nato_povozi(self):
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        podatki = lambda vsebina: {
            "predmet": self.mat.pk,
            "naslov": "1. domača",
            "datoteka": SimpleUploadedFile("f.txt", vsebina, content_type="text/plain"),
        }
        self.client.post(reverse("oddaja_nova"), podatki(b"prva"))
        self.assertEqual(Oddaja.objects.filter(ucenec=self.ucenec, naslov="1. domača").count(), 1)
        stara_pot = Oddaja.objects.get(ucenec=self.ucenec, naslov="1. domača").datoteka.name

        # Brez potrditve: ne povozi (obrazec vrne napako, ostane 1 oddaja z isto vsebino).
        odgovor = self.client.post(reverse("oddaja_nova"), podatki(b"druga-brez-potrditve"))
        self.assertEqual(odgovor.status_code, 200)
        self.assertContains(odgovor, "že obstaja oddaja")
        oddaja = Oddaja.objects.get(ucenec=self.ucenec, naslov="1. domača")
        with oddaja.datoteka.open("rb") as f:
            self.assertEqual(f.read(), b"prva")

        # S potrditvijo: povozi, ostane 1 oddaja z novo vsebino.
        p = podatki(b"tretja-s-potrditvijo")
        p["potrdi_povozitev"] = "on"
        odgovor = self.client.post(reverse("oddaja_nova"), p)
        self.assertEqual(odgovor.status_code, 302)
        self.assertEqual(Oddaja.objects.filter(ucenec=self.ucenec, naslov="1. domača").count(), 1)
        oddaja = Oddaja.objects.get(ucenec=self.ucenec, naslov="1. domača")
        with oddaja.datoteka.open("rb") as f:
            self.assertEqual(f.read(), b"tretja-s-potrditvijo")
        # Ime datoteke ostane isto (ista naloga).
        self.assertEqual(oddaja.datoteka.name, stara_pot)

    # --- Zaščiteni prenos: brez pravic ni dostopa -----------------------

    def test_ucenec_ne_prenese_tuje_oddaje(self):
        # ucenec2 odda nalogo
        oddaja = Oddaja.objects.create(ucenec=self.ucenec2, predmet=self.mat, naslov="X")
        oddaja.datoteka.save("test.txt", SimpleUploadedFile("test.txt", b"tajno"), save=True)
        # ucenec (drug učenec) poskuša prenesti
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("oddaja_prenos", args=[oddaja.pk])).status_code, 403)

    def test_ucitelj_predmeta_prenese_oddajo(self):
        oddaja = Oddaja.objects.create(ucenec=self.ucenec, predmet=self.mat, naslov="Y")
        oddaja.datoteka.save("y.txt", SimpleUploadedFile("y.txt", b"vsebina"), save=True)
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("oddaja_prenos", args=[oddaja.pk])).status_code, 200)

    # --- Dodatni testi (5. teden) ---------------------------------------

    def test_ucenec_uredi_profil(self):
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        odgovor = self.client.post(
            reverse("profil_uredi"),
            {"ime": "Bine", "priimek": "Novak-Kovač", "email": "bine@dijaki.si"},
        )
        self.assertEqual(odgovor.status_code, 302)
        self.ucenec.refresh_from_db()
        self.assertEqual(self.ucenec.priimek, "Novak-Kovač")

    def test_ucitelj_izbrise_svoje_gradivo(self):
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        gradivo = Gradivo.objects.create(predmet=self.mat, naslov="G", nalozil=self.ucitelj)
        gradivo.datoteka.save("g.txt", SimpleUploadedFile("g.txt", b"x"), save=True)
        odgovor = self.client.post(reverse("gradivo_izbrisi", args=[gradivo.pk]))
        self.assertEqual(odgovor.status_code, 302)
        self.assertFalse(Gradivo.objects.filter(pk=gradivo.pk).exists())

    def test_ucitelj_ne_izbrise_tujega_gradiva(self):
        # Gradivo pri predmetu SLO, ki ga učitelj (samo MAT) ne poučuje.
        tuj = Gradivo.objects.create(predmet=self.slo, naslov="Tuje")
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("gradivo_izbrisi", args=[tuj.pk])).status_code, 403)

    def test_oznaka_sporocila_o_napaki_je_danger(self):
        # BUG-01 (5. teden): Django oznako ERROR "error" preslikamo v Bootstrap "danger".
        from django.contrib.messages import constants
        from django.conf import settings
        self.assertEqual(settings.MESSAGE_TAGS.get(constants.ERROR), "danger")
