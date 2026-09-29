from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from administracija.models import Predmet, Ucenec, UcenecPredmet, Ucitelj

from .dovoljenja import je_admin, je_ucenec, je_ucitelj
from .forms import (
    GradivoForm,
    MojiPredmetiForm,
    OddajaForm,
    ProfilUcencaForm,
    RegistracijaUcencaForm,
)
from .models import Gradivo, Oddaja, Profil


def zacetna(request):
    """Razcep glede na vlogo: administratorja pošljemo na njegovo nadzorno
    ploščo, prijavljenega učitelja/učenca na njun portal, neprijavljene na
    pristajalno stran s prijavo/registracijo."""
    uporabnik = request.user
    if je_admin(uporabnik):
        kontekst = {
            "stevilo_predmetov": Predmet.objects.count(),
            "stevilo_uciteljev": Ucitelj.objects.count(),
            "stevilo_ucencev": Ucenec.objects.count(),
        }
        return render(request, "administracija/zacetna.html", kontekst)
    if je_ucitelj(uporabnik):
        return redirect("ucitelj_predmeti")
    if je_ucenec(uporabnik):
        return redirect("ucenec_domov")
    return render(request, "portal/pristajalna.html")


# --- Registracija in profil učenca --------------------------------------

def registracija(request):
    if request.user.is_authenticated:
        return redirect("zacetna")
    if request.method == "POST":
        form = RegistracijaUcencaForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                uporabnik = form.save()
                ucenec = Ucenec.objects.create(
                    ime=form.cleaned_data["ime"],
                    priimek=form.cleaned_data["priimek"],
                    email=form.cleaned_data["email"],
                )
                Profil.objects.create(
                    uporabnik=uporabnik, vloga=Profil.Vloga.UCENEC, ucenec=ucenec
                )
            login(request, uporabnik)
            messages.success(request, "Registracija uspešna. Dobrodošel/a!")
            return redirect("moji_predmeti")
    else:
        form = RegistracijaUcencaForm()
    return render(request, "registration/registracija.html", {"form": form})


def _zahtevaj_ucenca(request):
    if not je_ucenec(request.user):
        raise PermissionDenied
    return request.user.profil.ucenec


@login_required
def ucenec_domov(request):
    ucenec = _zahtevaj_ucenca(request)
    predmeti = Predmet.objects.filter(ucenci=ucenec).order_by("ime")
    return render(request, "portal/ucenec_domov.html", {"ucenec": ucenec, "predmeti": predmeti})


@login_required
def profil_uredi(request):
    ucenec = _zahtevaj_ucenca(request)
    if request.method == "POST":
        form = ProfilUcencaForm(request.POST, instance=ucenec)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil je bil posodobljen.")
            return redirect("ucenec_domov")
    else:
        form = ProfilUcencaForm(instance=ucenec)
    return render(request, "portal/profil_uredi.html", {"form": form})


@login_required
def moji_predmeti(request):
    ucenec = _zahtevaj_ucenca(request)
    if request.method == "POST":
        form = MojiPredmetiForm(request.POST)
        if form.is_valid():
            izbrani = set(form.cleaned_data["predmeti"])
            trenutni = set(Predmet.objects.filter(ucenci=ucenec))
            for predmet in izbrani - trenutni:
                UcenecPredmet.objects.get_or_create(ucenec=ucenec, predmet=predmet)
            UcenecPredmet.objects.filter(ucenec=ucenec).exclude(
                predmet__in=izbrani
            ).delete()
            messages.success(request, "Seznam predmetov je bil posodobljen.")
            return redirect("ucenec_domov")
    else:
        form = MojiPredmetiForm(initial={"predmeti": Predmet.objects.filter(ucenci=ucenec)})
    return render(request, "portal/moji_predmeti.html", {"form": form})


@login_required
def ucenec_gradiva(request, predmet_id):
    """Vpogled v gradiva predmeta, ki ga učenec obiskuje."""
    ucenec = _zahtevaj_ucenca(request)
    predmet = get_object_or_404(Predmet, pk=predmet_id)
    if not Predmet.objects.filter(pk=predmet_id, ucenci=ucenec).exists():
        raise PermissionDenied
    gradiva = predmet.gradiva.all()
    return render(request, "portal/ucenec_gradiva.html", {"predmet": predmet, "gradiva": gradiva})


@login_required
def moje_oddaje(request):
    ucenec = _zahtevaj_ucenca(request)
    oddaje = Oddaja.objects.filter(ucenec=ucenec).select_related("predmet")
    return render(request, "portal/moje_oddaje.html", {"oddaje": oddaje})


@login_required
def oddaja_nova(request):
    ucenec = _zahtevaj_ucenca(request)
    predmeti = Predmet.objects.filter(ucenci=ucenec)
    if request.method == "POST":
        form = OddajaForm(request.POST, request.FILES, dovoljeni_predmeti=predmeti)
        if form.is_valid():
            predmet = form.cleaned_data["predmet"]
            naslov = form.cleaned_data["naslov"]
            obstojeca = Oddaja.objects.filter(
                ucenec=ucenec, predmet=predmet, naslov=naslov
            ).first()
            potrjeno = form.cleaned_data.get("potrdi_povozitev")
            if obstojeca and not potrjeno:
                # Ponovna oddaja povozi prejšnjo šele po izrecni potrditvi učenca.
                form.add_error(
                    "potrdi_povozitev",
                    "Za to nalogo že obstaja oddaja. Označi potrditev, da povoziš "
                    "prejšnjo datoteko (novo datoteko izberi ponovno).",
                )
            else:
                if obstojeca:
                    obstojeca.datoteka.delete(save=False)
                    obstojeca.datoteka = form.cleaned_data["datoteka"]
                    obstojeca.save()
                    messages.success(request, "Prejšnja oddaja je bila povožena z novo datoteko.")
                else:
                    oddaja = form.save(commit=False)
                    oddaja.ucenec = ucenec
                    oddaja.save()
                    messages.success(request, "Naloga je bila oddana.")
                return redirect("moje_oddaje")
    else:
        form = OddajaForm(dovoljeni_predmeti=predmeti)
    return render(request, "portal/oddaja_obrazec.html", {"form": form})


# --- Pogled učitelja ----------------------------------------------------

def _zahtevaj_ucitelja(request):
    if not je_ucitelj(request.user):
        raise PermissionDenied
    return request.user.profil.ucitelj


@login_required
def ucitelj_predmeti(request):
    ucitelj = _zahtevaj_ucitelja(request)
    predmeti = Predmet.objects.filter(ucitelji=ucitelj).order_by("ime")
    return render(request, "portal/ucitelj_predmeti.html", {"ucitelj": ucitelj, "predmeti": predmeti})


def _predmet_ucitelja_ali_403(ucitelj, predmet_id):
    predmet = get_object_or_404(Predmet, pk=predmet_id)
    if not Predmet.objects.filter(pk=predmet_id, ucitelji=ucitelj).exists():
        raise PermissionDenied
    return predmet


@login_required
def ucitelj_predmet(request, predmet_id):
    """Podrobnosti predmeta za učitelja: gradiva + oddane naloge učencev."""
    ucitelj = _zahtevaj_ucitelja(request)
    predmet = _predmet_ucitelja_ali_403(ucitelj, predmet_id)
    return render(
        request,
        "portal/ucitelj_predmet.html",
        {
            "predmet": predmet,
            "gradiva": predmet.gradiva.all(),
            "oddaje": predmet.oddaje.select_related("ucenec"),
        },
    )


@login_required
def gradivo_nalozi(request):
    ucitelj = _zahtevaj_ucitelja(request)
    predmeti = Predmet.objects.filter(ucitelji=ucitelj)
    if request.method == "POST":
        form = GradivoForm(request.POST, request.FILES, dovoljeni_predmeti=predmeti)
        if form.is_valid():
            gradivo = form.save(commit=False)
            # Dodatna zaščita: predmet mora biti med predmeti tega učitelja.
            if not predmeti.filter(pk=gradivo.predmet_id).exists():
                raise PermissionDenied
            gradivo.nalozil = ucitelj
            gradivo.save()
            messages.success(request, "Gradivo je bilo naloženo.")
            return redirect("ucitelj_predmet", predmet_id=gradivo.predmet_id)
    else:
        form = GradivoForm(dovoljeni_predmeti=predmeti)
    return render(request, "portal/gradivo_obrazec.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def gradivo_izbrisi(request, pk):
    ucitelj = _zahtevaj_ucitelja(request)
    gradivo = get_object_or_404(Gradivo, pk=pk)
    if not Predmet.objects.filter(pk=gradivo.predmet_id, ucitelji=ucitelj).exists():
        raise PermissionDenied
    if request.method == "POST":
        predmet_id = gradivo.predmet_id
        gradivo.datoteka.delete(save=False)
        gradivo.delete()
        messages.success(request, "Gradivo je bilo izbrisano.")
        return redirect("ucitelj_predmet", predmet_id=predmet_id)
    return render(request, "portal/gradivo_potrdi_brisanje.html", {"gradivo": gradivo})


# --- Zaščiteni prenos datotek -------------------------------------------

def _sme_do_gradiva(user, gradivo):
    if je_admin(user):
        return True
    if je_ucitelj(user):
        return Predmet.objects.filter(pk=gradivo.predmet_id, ucitelji=user.profil.ucitelj).exists()
    if je_ucenec(user):
        return Predmet.objects.filter(pk=gradivo.predmet_id, ucenci=user.profil.ucenec).exists()
    return False


def _sme_do_oddaje(user, oddaja):
    if je_admin(user):
        return True
    if je_ucitelj(user):
        return Predmet.objects.filter(pk=oddaja.predmet_id, ucitelji=user.profil.ucitelj).exists()
    if je_ucenec(user):
        return oddaja.ucenec_id == user.profil.ucenec_id
    return False


@login_required
def gradivo_prenos(request, pk):
    """Datoteke niso javno dostopne — postrežemo jih le prek te preverjene poti."""
    gradivo = get_object_or_404(Gradivo, pk=pk)
    if not _sme_do_gradiva(request.user, gradivo):
        raise PermissionDenied
    try:
        return FileResponse(gradivo.datoteka.open("rb"), as_attachment=True, filename=gradivo.ime_datoteke())
    except FileNotFoundError:
        raise Http404("Datoteka ne obstaja.")


@login_required
def oddaja_prenos(request, pk):
    oddaja = get_object_or_404(Oddaja, pk=pk)
    if not _sme_do_oddaje(request.user, oddaja):
        raise PermissionDenied
    try:
        return FileResponse(oddaja.datoteka.open("rb"), as_attachment=True, filename=oddaja.ime_datoteke())
    except FileNotFoundError:
        raise Http404("Datoteka ne obstaja.")
