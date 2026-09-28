from django import forms

from .models import Predmet, Ucenec, Ucitelj


def _dodaj_bootstrap_razrede(form):
    for polje in form.fields.values():
        if isinstance(polje.widget, (forms.SelectMultiple, forms.Select)):
            polje.widget.attrs.setdefault("class", "form-select")
        else:
            polje.widget.attrs.setdefault("class", "form-control")


class PredmetForm(forms.ModelForm):
    class Meta:
        model = Predmet
        fields = ["sifra", "ime", "opis"]
        widgets = {
            "opis": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _dodaj_bootstrap_razrede(self)


class UciteljForm(forms.ModelForm):
    predmeti = forms.ModelMultipleChoiceField(
        queryset=Predmet.objects.all(),
        widget=forms.SelectMultiple(attrs={"size": 8}),
        required=False,
        label="predmeti, ki jih poučuje",
    )

    class Meta:
        model = Ucitelj
        fields = ["ime", "priimek", "email", "predmeti"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _dodaj_bootstrap_razrede(self)


class UcenecForm(forms.ModelForm):
    predmeti = forms.ModelMultipleChoiceField(
        queryset=Predmet.objects.all(),
        widget=forms.SelectMultiple(attrs={"size": 8}),
        required=False,
        label="predmeti, ki jih obiskuje",
    )

    class Meta:
        model = Ucenec
        fields = ["ime", "priimek", "email", "predmeti"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _dodaj_bootstrap_razrede(self)

    def clean_predmeti(self):
        predmeti = self.cleaned_data["predmeti"]
        if len(predmeti) < 1:
            raise forms.ValidationError("Učenec mora obiskovati vsaj en predmet.")
        return predmeti
