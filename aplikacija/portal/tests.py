import shutil
import tempfile
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from administracija.models import (
    Predmet,
    Ucenec,
    UcenecPredmet,
    Ucitelj,
    UciteljPredmet,
)

from .models import Gradivo, Naloga, Obvestilo, Oddaja, Profil

MEDIA = tempfile.mkdtemp()


def dodaj_profil(username, geslo, vloga, ucitelj=None, ucenec=None, **extra):
    user = User.objects.create_user(username=username, password=geslo, **extra)
    Profil.objects.create(uporabnik=user, vloga=vloga, ucitelj=ucitelj, ucenec=ucenec)
    return user


def datoteka(ime="f.txt", vsebina=b"x"):
    return SimpleUploadedFile(ime, vsebina, content_type="text/plain")


@override_settings(MEDIA_ROOT=MEDIA)
class PortalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mat = Predmet.objects.create(sifra="MAT", ime="Matematika")
        cls.slo = Predmet.objects.create(sifra="SLO", ime="Slovenščina")

        cls.ucitelj = Ucitelj.objects.create(ime="Ana", priimek="Kovač", email="ana@solski-is.si")
        UciteljPredmet.objects.create(ucitelj=cls.ucitelj, predmet=cls.mat)  # poučuje MAT, ne SLO

        cls.ucenec = Ucenec.objects.create(ime="Bine", priimek="Novak", email="bine@dijaki.si")
        UcenecPredmet.objects.create(ucenec=cls.ucenec, predmet=cls.mat)

        cls.ucenec2 = Ucenec.objects.create(ime="Cilka", priimek="Zajc", email="cilka@dijaki.si")
        UcenecPredmet.objects.create(ucenec=cls.ucenec2, predmet=cls.mat)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def naloga(self, predmet=None, rok=None, ustvaril=None):
        return Naloga.objects.create(
            predmet=predmet or self.mat,
            naslov="1. domača",
            rok=rok or (timezone.now() + timedelta(days=5)),
            ustvaril=ustvaril or self.ucitelj,
        )

    # --- Avtorizacija ----------------------------------------------------

    def test_anonimni_preusmerjen_iz_admin_crud(self):
        odgovor = self.client.get(reverse("predmet_seznam"))
        self.assertEqual(odgovor.status_code, 302)
        self.assertIn("/prijava/", odgovor.url)

    def test_ucenec_ne_dostopa_do_admin_crud(self):
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("predmet_seznam")).status_code, 403)

    # --- Registracija / zgoščeno geslo -----------------------------------

    def test_registracija_in_zgosceno_geslo(self):
        odgovor = self.client.post(
            reverse("registracija"),
            {"username": "novi", "ime": "Dana", "priimek": "Horvat",
             "email": "dana@dijaki.si", "password1": "MocnoGeslo123", "password2": "MocnoGeslo123"},
        )
        self.assertEqual(odgovor.status_code, 302)
        user = User.objects.get(username="novi")
        self.assertNotEqual(user.password, "MocnoGeslo123")
        self.assertTrue(check_password("MocnoGeslo123", user.password))
        self.assertEqual(user.profil.vloga, Profil.Vloga.UCENEC)

    # --- Učenec: predmeti in gradiva -------------------------------------

    def test_ucenec_ureja_predmete(self):
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

    # --- Učitelj: naloge in gradiva --------------------------------------

    def test_ucitelj_ustvari_nalogo_le_za_svoj_predmet(self):
        student = dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        rok = (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M")
        odgovor = self.client.post(
            reverse("naloga_nova"),
            {"predmet": self.mat.pk, "naslov": "Ulomki", "opis": "navodila", "rok": rok},
        )
        self.assertEqual(odgovor.status_code, 302)
        self.assertTrue(Naloga.objects.filter(predmet=self.mat, naslov="Ulomki").exists())
        # vpisani učenec dobi obvestilo o novi nalogi
        self.assertTrue(Obvestilo.objects.filter(prejemnik=student, besedilo__contains="Ulomki").exists())

    def test_ucitelj_ne_ustvari_naloge_za_tuj_predmet(self):
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        rok = (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M")
        odgovor = self.client.post(
            reverse("naloga_nova"),
            {"predmet": self.slo.pk, "naslov": "Vrinjeno", "opis": "", "rok": rok},
        )
        self.assertEqual(odgovor.status_code, 200)  # obrazec zavrne izbiro
        self.assertFalse(Naloga.objects.filter(predmet=self.slo).exists())

    def test_ucitelj_vidi_le_svoje_naloge_predmet(self):
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("ucitelj_predmet", args=[self.slo.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse("ucitelj_predmet", args=[self.mat.pk])).status_code, 200)

    def test_ucitelj_nalozi_in_izbrise_gradivo(self):
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        self.client.post(reverse("gradivo_nalozi"), {"predmet": self.mat.pk, "naslov": "G", "datoteka": datoteka()})
        gradivo = Gradivo.objects.get(predmet=self.mat, naslov="G")
        self.assertEqual(self.client.post(reverse("gradivo_izbrisi", args=[gradivo.pk])).status_code, 302)
        self.assertFalse(Gradivo.objects.filter(pk=gradivo.pk).exists())

    # --- Oddaja naloge: poimenovanje, zamuda, povozitev ------------------

    def test_oddaja_poimenovanje_datoteke(self):
        naloga = self.naloga()
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        self.client.post(reverse("ucenec_naloga", args=[naloga.pk]),
                         {"datoteka": datoteka("moja.docx", b"v1")})
        oddaja = Oddaja.objects.get(naloga=naloga, ucenec=self.ucenec)
        self.assertTrue(oddaja.datoteka.name.endswith("Novak Bine – 1. domača.docx"))
        self.assertFalse(oddaja.prepozno)

    def test_oddaja_po_roku_je_prepozna(self):
        naloga = self.naloga(rok=timezone.now() - timedelta(days=1))
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        self.client.post(reverse("ucenec_naloga", args=[naloga.pk]), {"datoteka": datoteka()})
        self.assertTrue(Oddaja.objects.get(naloga=naloga, ucenec=self.ucenec).prepozno)

    def test_ponovna_oddaja_potrditev_in_razveljavi_oceno(self):
        naloga = self.naloga()
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        self.client.post(reverse("ucenec_naloga", args=[naloga.pk]), {"datoteka": datoteka("f.txt", b"prva")})
        oddaja = Oddaja.objects.get(naloga=naloga, ucenec=self.ucenec)
        oddaja.ocena = 4
        oddaja.ocenjeno = timezone.now()
        oddaja.save()

        # brez potrditve -> ne povozi
        odgovor = self.client.post(reverse("ucenec_naloga", args=[naloga.pk]), {"datoteka": datoteka("f.txt", b"druga")})
        self.assertEqual(odgovor.status_code, 200)
        self.assertContains(odgovor, "že obstaja oddaja")
        oddaja.refresh_from_db()
        self.assertEqual(oddaja.ocena, 4)

        # s potrditvijo -> povozi in razveljavi oceno
        self.client.post(reverse("ucenec_naloga", args=[naloga.pk]),
                         {"datoteka": datoteka("f.txt", b"tretja"), "potrdi_povozitev": "on"})
        self.assertEqual(Oddaja.objects.filter(naloga=naloga, ucenec=self.ucenec).count(), 1)
        oddaja.refresh_from_db()
        self.assertIsNone(oddaja.ocena)
        with oddaja.datoteka.open("rb") as f:
            self.assertEqual(f.read(), b"tretja")

    # --- Ocenjevanje -----------------------------------------------------

    def test_ucitelj_oceni_in_ucenec_obvescen(self):
        naloga = self.naloga()
        student = dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        oddaja = Oddaja.objects.create(naloga=naloga, ucenec=self.ucenec)
        oddaja.datoteka.save("o.txt", datoteka(), save=True)
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        odgovor = self.client.post(reverse("oddaja_oceni", args=[oddaja.pk]), {"ocena": 5, "komentar": "Odlično"})
        self.assertEqual(odgovor.status_code, 302)
        oddaja.refresh_from_db()
        self.assertEqual(oddaja.ocena, 5)
        self.assertIsNotNone(oddaja.ocenjeno)
        self.assertTrue(Obvestilo.objects.filter(prejemnik=student, besedilo__contains="Ocena").exists())

    def test_ucitelj_ne_oceni_oddaje_tujega_predmeta(self):
        # naloga pri SLO (ki je ta učitelj ne poučuje)
        naloga = Naloga.objects.create(predmet=self.slo, naslov="X", rok=timezone.now() + timedelta(days=1))
        oddaja = Oddaja.objects.create(naloga=naloga, ucenec=self.ucenec)
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("oddaja_oceni", args=[oddaja.pk])).status_code, 403)

    # --- Zaščiteni prenos ------------------------------------------------

    def test_ucenec_ne_prenese_tuje_oddaje(self):
        naloga = self.naloga()
        oddaja = Oddaja.objects.create(naloga=naloga, ucenec=self.ucenec2)
        oddaja.datoteka.save("t.txt", datoteka("t.txt", b"tajno"), save=True)
        dodaj_profil("u1", "geslo12345", Profil.Vloga.UCENEC, ucenec=self.ucenec)
        self.client.login(username="u1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("oddaja_prenos", args=[oddaja.pk])).status_code, 403)

    def test_ucitelj_predmeta_prenese_oddajo(self):
        naloga = self.naloga()
        oddaja = Oddaja.objects.create(naloga=naloga, ucenec=self.ucenec)
        oddaja.datoteka.save("y.txt", datoteka("y.txt", b"vsebina"), save=True)
        dodaj_profil("t1", "geslo12345", Profil.Vloga.UCITELJ, ucitelj=self.ucitelj)
        self.client.login(username="t1", password="geslo12345")
        self.assertEqual(self.client.get(reverse("oddaja_prenos", args=[oddaja.pk])).status_code, 200)

    # --- Regresija oblikovanja ------------------------------------------

    def test_oznaka_sporocila_o_napaki_je_danger(self):
        from django.contrib.messages import constants
        self.assertEqual(settings.MESSAGE_TAGS.get(constants.ERROR), "danger")
