from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from administracija.models import Predmet, Ucenec

from .models import Gradivo, Oddaja


def _bootstrap(form):
    for polje in form.fields.values():
        widget = polje.widget
        if isinstance(widget, (forms.SelectMultiple, forms.CheckboxSelectMultiple)):
            continue
        if isinstance(widget, forms.Select):
            widget.attrs.setdefault("class", "form-select")
        elif isinstance(widget, forms.FileInput):
            widget.attrs.setdefault("class", "form-control")
        else:
            widget.attrs.setdefault("class", "form-control")


class RegistracijaUcencaForm(UserCreationForm):
    """Samoregistracija učenca: ustvari Django uporabnika (zgoščeno geslo) in
    povezan zapis Ucenec."""

    ime = forms.CharField(label="ime", max_length=50)
    priimek = forms.CharField(label="priimek", max_length=50)
    email = forms.EmailField(label="e-pošta")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "ime", "priimek", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrap(self)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Ucenec.objects.filter(email=email).exists():
            raise forms.ValidationError("Učenec s to e-pošto že obstaja.")
        return email


class ProfilUcencaForm(forms.ModelForm):
    """Urejanje lastnih osebnih podatkov učenca."""

    class Meta:
        model = Ucenec
        fields = ["ime", "priimek", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrap(self)


class MojiPredmetiForm(forms.Form):
    """Učenec izbere/popravi seznam predmetov, ki jih obiskuje."""

    predmeti = forms.ModelMultipleChoiceField(
        queryset=Predmet.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="predmeti, ki jih obiskujem",
    )

    def clean_predmeti(self):
        predmeti = self.cleaned_data["predmeti"]
        if len(predmeti) < 1:
            raise forms.ValidationError("Obiskovati moraš vsaj en predmet.")
        return predmeti


class GradivoForm(forms.ModelForm):
    """Nalaganje gradiva; izbor predmeta je omejen na predmete, ki jih učitelj
    dejansko poučuje (queryset nastavi pogled)."""

    class Meta:
        model = Gradivo
        fields = ["predmet", "naslov", "datoteka"]

    def __init__(self, *args, dovoljeni_predmeti=None, **kwargs):
        super().__init__(*args, **kwargs)
        if dovoljeni_predmeti is not None:
            self.fields["predmet"].queryset = dovoljeni_predmeti
        _bootstrap(self)


class OddajaForm(forms.ModelForm):
    """Oddaja naloge; izbor predmeta je omejen na predmete, ki jih učenec
    obiskuje (queryset nastavi pogled). Polje `potrdi_povozitev` uporabnik
    označi, kadar želi povoziti obstoječo oddajo iste naloge."""

    potrdi_povozitev = forms.BooleanField(
        required=False,
        label="Potrjujem, da želim povoziti prejšnjo oddajo te naloge.",
    )

    class Meta:
        model = Oddaja
        fields = ["predmet", "naslov", "datoteka"]

    def __init__(self, *args, dovoljeni_predmeti=None, **kwargs):
        super().__init__(*args, **kwargs)
        if dovoljeni_predmeti is not None:
            self.fields["predmet"].queryset = dovoljeni_predmeti
        _bootstrap(self)
