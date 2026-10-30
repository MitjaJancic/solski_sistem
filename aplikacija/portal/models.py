import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from administracija.models import Predmet, Ucenec, Ucitelj


class PovoznoShranjevanje(FileSystemStorage):
    """Shranjevanje za oddaje nalog:
    - ohrani natančno ime »Priimek Ime – Naslov naloge.ext« (privzeto Django
      pošlje ime skozi `get_valid_filename`, ki bi presledke in pomišljaj
      spremenil, zato tu ime ohranimo takšno, kot ga sestavi `pot_oddaje`);
    - ob istem imenu povozi obstoječo datoteko namesto dodajanja naključne
      pripone (ponovna oddaja iste naloge ohrani isto datoteko)."""

    def get_valid_name(self, name):
        return name

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name


povozno = PovoznoShranjevanje()


def _varno_ime(niz):
    """Odstrani znake, ki bi lahko sestavili pot (/, \\), da ime datoteke
    ostane le ime in ne poddirektorij."""
    return niz.replace("/", "-").replace("\\", "-").strip()


def pot_gradiva(instance, filename):
    return f"gradiva/predmet_{instance.predmet_id}/{_varno_ime(filename)}"


def pot_oddaje(instance, filename):
    """Datoteko shrani pod imenom »Priimek Ime – Naslov naloge« z izvorno
    končnico (zahteva 4. poglavja navodil); predmet določa naloga."""
    koncnica = os.path.splitext(filename)[1].lower()
    ucenec = instance.ucenec
    naslov = instance.naloga.naslov
    ime_datoteke = _varno_ime(f"{ucenec.priimek} {ucenec.ime} – {naslov}{koncnica}")
    return f"oddaje/predmet_{instance.naloga.predmet_id}/{ime_datoteke}"


class Profil(models.Model):
    """Poveže Djangovega uporabnika (prijava, zgoščeno geslo) z vlogo in po
    potrebi z zapisom učitelja ali učenca."""

    class Vloga(models.TextChoices):
        ADMIN = "admin", "administrator"
        UCITELJ = "ucitelj", "učitelj"
        UCENEC = "ucenec", "učenec"

    uporabnik = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profil",
        verbose_name="uporabnik",
    )
    vloga = models.CharField("vloga", max_length=10, choices=Vloga.choices)
    ucitelj = models.OneToOneField(
        Ucitelj, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="profil", verbose_name="povezan učitelj",
    )
    ucenec = models.OneToOneField(
        Ucenec, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="profil", verbose_name="povezan učenec",
    )

    class Meta:
        verbose_name = "profil"
        verbose_name_plural = "profili"

    def __str__(self):
        return f"{self.uporabnik.username} ({self.get_vloga_display()})"

    @property
    def je_admin(self):
        return self.vloga == self.Vloga.ADMIN

    @property
    def je_ucitelj(self):
        return self.vloga == self.Vloga.UCITELJ

    @property
    def je_ucenec(self):
        return self.vloga == self.Vloga.UCENEC


class Gradivo(models.Model):
    """Učno gradivo, ki ga učitelj naloži za predmet, ki ga poučuje."""

    predmet = models.ForeignKey(
        Predmet, on_delete=models.CASCADE, related_name="gradiva", verbose_name="predmet"
    )
    naslov = models.CharField("naslov", max_length=150)
    datoteka = models.FileField("datoteka", upload_to=pot_gradiva)
    nalozil = models.ForeignKey(
        Ucitelj, on_delete=models.SET_NULL, null=True,
        related_name="nalozena_gradiva", verbose_name="naložil",
    )
    ustvarjeno = models.DateTimeField("naloženo", auto_now_add=True)

    class Meta:
        verbose_name = "gradivo"
        verbose_name_plural = "gradiva"
        ordering = ["-ustvarjeno"]

    def __str__(self):
        return f"{self.naslov} ({self.predmet.sifra})"

    def ime_datoteke(self):
        return os.path.basename(self.datoteka.name)


class Naloga(models.Model):
    """NADGRADNJA: naloga kot samostojna entiteta z rokom oddaje. Učitelj jo
    ustvari pri predmetu, ki ga poučuje; učenci oddajo svojo rešitev (Oddaja)."""

    predmet = models.ForeignKey(
        Predmet, on_delete=models.CASCADE, related_name="naloge", verbose_name="predmet"
    )
    naslov = models.CharField("naslov", max_length=150)
    opis = models.TextField("opis / navodila", blank=True)
    rok = models.DateTimeField("rok oddaje")
    ustvaril = models.ForeignKey(
        Ucitelj, on_delete=models.SET_NULL, null=True,
        related_name="ustvarjene_naloge", verbose_name="ustvaril",
    )
    ustvarjeno = models.DateTimeField("ustvarjeno", auto_now_add=True)

    class Meta:
        verbose_name = "naloga"
        verbose_name_plural = "naloge"
        ordering = ["rok"]

    def __str__(self):
        return f"{self.naslov} ({self.predmet.sifra})"

    @property
    def je_potekla(self):
        return timezone.now() > self.rok

    def stanje(self):
        return "potekla" if self.je_potekla else "odprta"


class Oddaja(models.Model):
    """Rešitev naloge, ki jo odda učenec. NADGRADNJA: vezana na Nalogo,
    označi zamudo in omogoča učiteljevo ocenjevanje (ocena + komentar).
    Ponovna oddaja povozi prejšnjo datoteko po potrditvi učenca."""

    naloga = models.ForeignKey(
        Naloga, on_delete=models.CASCADE, related_name="oddaje", verbose_name="naloga"
    )
    ucenec = models.ForeignKey(
        Ucenec, on_delete=models.CASCADE, related_name="oddaje", verbose_name="učenec"
    )
    datoteka = models.FileField("datoteka", upload_to=pot_oddaje, storage=povozno)
    oddano = models.DateTimeField("zadnja oddaja", auto_now=True)
    prepozno = models.BooleanField("oddano po roku", default=False)
    # Ocenjevanje (učitelj)
    ocena = models.PositiveSmallIntegerField(
        "ocena", null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    komentar = models.TextField("povratna informacija", blank=True)
    ocenjeno = models.DateTimeField("ocenjeno", null=True, blank=True)

    class Meta:
        verbose_name = "oddaja naloge"
        verbose_name_plural = "oddaje nalog"
        ordering = ["-oddano"]
        constraints = [
            models.UniqueConstraint(fields=["ucenec", "naloga"], name="unikatna_oddaja_na_nalogo")
        ]

    def __str__(self):
        return f"{self.ucenec} – {self.naloga.naslov}"

    def ime_datoteke(self):
        return os.path.basename(self.datoteka.name)

    @property
    def je_ocenjena(self):
        return self.ocena is not None


class Obvestilo(models.Model):
    """NADGRADNJA: preprosta obvestila (nova naloga, prejeta ocena) s prikazom
    neprebranih v navigaciji."""

    prejemnik = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="obvestila", verbose_name="prejemnik",
    )
    besedilo = models.CharField("besedilo", max_length=255)
    povezava = models.CharField("povezava", max_length=200, blank=True)
    prebrano = models.BooleanField("prebrano", default=False)
    ustvarjeno = models.DateTimeField("ustvarjeno", auto_now_add=True)

    class Meta:
        verbose_name = "obvestilo"
        verbose_name_plural = "obvestila"
        ordering = ["-ustvarjeno"]

    def __str__(self):
        return f"{self.prejemnik}: {self.besedilo[:40]}"

    @staticmethod
    def obvesti(uporabnik, besedilo, povezava=""):
        """Ustvari obvestilo, če uporabnik obstaja (varno tudi za None)."""
        if uporabnik is not None:
            Obvestilo.objects.create(prejemnik=uporabnik, besedilo=besedilo, povezava=povezava)
