from django.db import models


class Predmet(models.Model):
    sifra = models.CharField("šifra", max_length=10, unique=True)
    ime = models.CharField("ime predmeta", max_length=100)
    opis = models.TextField("opis", blank=True)

    class Meta:
        verbose_name = "predmet"
        verbose_name_plural = "predmeti"
        ordering = ["ime"]

    def __str__(self):
        return f"{self.sifra} – {self.ime}"


class Ucitelj(models.Model):
    ime = models.CharField("ime", max_length=50)
    priimek = models.CharField("priimek", max_length=50)
    email = models.EmailField("e-pošta", unique=True)
    predmeti = models.ManyToManyField(
        Predmet,
        through="UciteljPredmet",
        related_name="ucitelji",
        verbose_name="predmeti, ki jih poučuje",
        blank=True,
    )

    class Meta:
        verbose_name = "učitelj"
        verbose_name_plural = "učitelji"
        ordering = ["priimek", "ime"]

    def __str__(self):
        return f"{self.priimek} {self.ime}"


class Ucenec(models.Model):
    ime = models.CharField("ime", max_length=50)
    priimek = models.CharField("priimek", max_length=50)
    email = models.EmailField("e-pošta", unique=True)
    predmeti = models.ManyToManyField(
        Predmet,
        through="UcenecPredmet",
        related_name="ucenci",
        verbose_name="predmeti, ki jih obiskuje",
        blank=True,
    )

    class Meta:
        verbose_name = "učenec"
        verbose_name_plural = "učenci"
        ordering = ["priimek", "ime"]

    def __str__(self):
        return f"{self.priimek} {self.ime}"


class UciteljPredmet(models.Model):
    ucitelj = models.ForeignKey(Ucitelj, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmet, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "povezava učitelj–predmet"
        verbose_name_plural = "povezave učitelj–predmet"
        constraints = [
            models.UniqueConstraint(fields=["ucitelj", "predmet"], name="unikatna_povezava_ucitelj_predmet")
        ]

    def __str__(self):
        return f"{self.ucitelj} → {self.predmet}"


class UcenecPredmet(models.Model):
    ucenec = models.ForeignKey(Ucenec, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmet, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "povezava učenec–predmet"
        verbose_name_plural = "povezave učenec–predmet"
        constraints = [
            models.UniqueConstraint(fields=["ucenec", "predmet"], name="unikatna_povezava_ucenec_predmet")
        ]

    def __str__(self):
        return f"{self.ucenec} → {self.predmet}"
