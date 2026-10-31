from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

PREVOD_CRK = str.maketrans("čžšČŽŠ", "czsCZS")


class CaseAndDiacriticInsensitiveBackend(ModelBackend):
    """Omogoča prijavo ne glede na velikost črk (M.Horvat / m.horvat)
    in ne glede na to, ali uporabnik vnese šumnike (M.Jančič / M.Jancic)."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        # 1. Poskusi neposredno (case-insensitive)
        user = User.objects.filter(username__iexact=username).first()

        # 2. Poskusi z zamenjavo šumnikov (npr. M.Jančič -> M.Jancic)
        if not user:
            cist_vnos = username.translate(PREVOD_CRK)
            user = User.objects.filter(username__iexact=cist_vnos).first()

        # 3. Če uporabnik v bazi morda vsebuje šumnike
        if not user:
            cist_vnos = username.translate(PREVOD_CRK).lower()
            for u in User.objects.all():
                if u.username.translate(PREVOD_CRK).lower() == cist_vnos:
                    user = u
                    break

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
