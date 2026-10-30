from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from administracija.models import Predmet, Ucenec

from .models import Gradivo, Naloga, Oddaja


def _bootstrap(form):
    for polje in form.fields.values():
        widget = polje.widget
        if isinstance(widget, (forms.SelectMultiple, forms.CheckboxSelectMultiple, forms.CheckboxInput)):
            continue
        if isinstance(widget, forms.Select):
            widget.attrs.setdefault("class", "form-select")
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
    class Meta:
        model = Ucenec
        fields = ["ime", "priimek", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrap(self)


class MojiPredmetiForm(forms.Form):
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
    class Meta:
        model = Gradivo
        fields = ["predmet", "naslov", "datoteka"]

    def __init__(self, *args, dovoljeni_predmeti=None, **kwargs):
        super().__init__(*args, **kwargs)
        if dovoljeni_predmeti is not None:
            self.fields["predmet"].queryset = dovoljeni_predmeti
        _bootstrap(self)


class NalogaForm(forms.ModelForm):
    """NADGRADNJA: učitelj ustvari/uredi nalogo z rokom za svoj predmet."""

    class Meta:
        model = Naloga
        fields = ["predmet", "naslov", "opis", "rok"]
        widgets = {
            "opis": forms.Textarea(attrs={"rows": 3}),
            "rok": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, dovoljeni_predmeti=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rok"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
        if dovoljeni_predmeti is not None:
            self.fields["predmet"].queryset = dovoljeni_predmeti
        _bootstrap(self)


class OddajaForm(forms.ModelForm):
    """Oddaja rešitve naloge (naloga in učenec se določita v pogledu).
    `potrdi_povozitev` uporabnik označi za povozitev obstoječe oddaje."""

    potrdi_povozitev = forms.BooleanField(
        required=False,
        label="Potrjujem, da želim povoziti prejšnjo oddajo te naloge.",
    )

    class Meta:
        model = Oddaja
        fields = ["datoteka"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrap(self)


class OcenaForm(forms.ModelForm):
    """NADGRADNJA: učitelj oceni oddajo in doda povratno informacijo."""

    class Meta:
        model = Oddaja
        fields = ["ocena", "komentar"]
        widgets = {
            "ocena": forms.Select(choices=[(i, i) for i in range(1, 6)]),
            "komentar": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ocena"].required = True
        _bootstrap(self)
