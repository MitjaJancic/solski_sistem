"""Pomožne funkcije in mešalniki (mixins) za preverjanje pravic (avtorizacija).

Pravilo iz navodil (4. teden): noben uporabnik ne dostopa do funkcij, ki mu ne
pripadajo. Vloge: administrator, učitelj, učenec.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def _vloga(user):
    profil = getattr(user, "profil", None)
    return profil.vloga if profil else None


def je_admin(user):
    return user.is_authenticated and (user.is_superuser or _vloga(user) == "admin")


def je_ucitelj(user):
    return user.is_authenticated and _vloga(user) == "ucitelj"


def je_ucenec(user):
    return user.is_authenticated and _vloga(user) == "ucenec"


class AdminZahtevanMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return je_admin(self.request.user)


class UciteljZahtevanMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return je_ucitelj(self.request.user)


class UcenecZahtevanMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return je_ucenec(self.request.user)
