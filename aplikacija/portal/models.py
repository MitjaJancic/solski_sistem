import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

from administracija.models import Predmet, Ucenec, Ucitelj


class PovoznoShranjevanje(FileSystemStorage):
    """Shranjevanje za oddaje nalog:
    - ohrani natančno ime »Priimek Ime – Naslov naloge.ext« (privzeto Django
      pošlje ime skozi `get_valid_filename`, ki bi presledke in pomišljaj
      spremenil, zato tu ime ohranimo takšno, kot ga sestavi `pot_oddaje`);
    - ob istem imenu povozi obstoječo datoteko namesto dodajanja naključne
      pripone (ponovna oddaja iste naloge ohrani isto datoteko)."""

    def get_valid_name(self, name):
        # Ime je že sestavljeno in očiščeno v `pot_oddaje` (brez ločil poti),
        # zato ga ne spreminjamo dodatno.
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
    končnico (zahteva 4. poglavja navodil)."""
    koncnica = os.path.splitext(filename)[1].lower()
    ucenec = instance.ucenec
    ime_datoteke = _varno_ime(f"{ucenec.priimek} {ucenec.ime} – {instance.naslov}{koncnica}")
    return f"oddaje/predmet_{instance.predmet_id}/{ime_datoteke}"


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
        Ucitelj,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profil",
        verbose_name="povezan učitelj",
    )
    ucenec = models.OneToOneField(
        Ucenec,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profil",
        verbose_name="povezan učenec",
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
        Ucitelj,
        on_delete=models.SET_NULL,
        null=True,
        related_name="nalozena_gradiva",
        verbose_name="naložil",
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


class Oddaja(models.Model):
    """Naloga, ki jo učenec odda pri predmetu. Ponovna oddaja iste naloge
    (isti učenec, predmet in naslov) povozi prejšnjo datoteko."""

    predmet = models.ForeignKey(
        Predmet, on_delete=models.CASCADE, related_name="oddaje", verbose_name="predmet"
    )
    ucenec = models.ForeignKey(
        Ucenec, on_delete=models.CASCADE, related_name="oddaje", verbose_name="učenec"
    )
    naslov = models.CharField("naslov naloge", max_length=150)
    datoteka = models.FileField("datoteka", upload_to=pot_oddaje, storage=povozno)
    oddano = models.DateTimeField("zadnja oddaja", auto_now=True)

    class Meta:
        verbose_name = "oddaja naloge"
        verbose_name_plural = "oddaje nalog"
        ordering = ["-oddano"]
        constraints = [
            models.UniqueConstraint(
                fields=["ucenec", "predmet", "naslov"], name="unikatna_oddaja_na_nalogo"
            )
        ]

    def __str__(self):
        return f"{self.ucenec} – {self.naslov} ({self.predmet.sifra})"

    def ime_datoteke(self):
        return os.path.basename(self.datoteka.name)
