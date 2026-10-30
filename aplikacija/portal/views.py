import csv
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from administracija.models import Predmet, Ucenec, UcenecPredmet, Ucitelj

from .dovoljenja import je_admin, je_ucenec, je_ucitelj
from .forms import (
    GradivoForm,
    MojiPredmetiForm,
    NalogaForm,
    OcenaForm,
    OddajaForm,
    ProfilUcencaForm,
    RegistracijaUcencaForm,
)
from .models import Gradivo, Naloga, Obvestilo, Oddaja, Profil


def _uporabnik_ucitelja(ucitelj):
    profil = getattr(ucitelj, "profil", None)
    return getattr(profil, "uporabnik", None)


def _uporabnik_ucenca(ucenec):
    profil = getattr(ucenec, "profil", None)
    return getattr(profil, "uporabnik", None)


def zacetna(request):
    uporabnik = request.user
    if je_admin(uporabnik):
        kontekst = {
            "stevilo_predmetov": Predmet.objects.count(),
            "stevilo_uciteljev": Ucitelj.objects.count(),
            "stevilo_ucencev": Ucenec.objects.count(),
        }
        return render(request, "administracija/zacetna.html", kontekst)
    if je_ucitelj(uporabnik):
        return redirect("ucitelj_domov")
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
                Profil.objects.create(uporabnik=uporabnik, vloga=Profil.Vloga.UCENEC, ucenec=ucenec)
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


def _zahtevaj_ucitelja(request):
    if not je_ucitelj(request.user):
        raise PermissionDenied
    return request.user.profil.ucitelj


# --- Nadzorna plošča in strani učenca -----------------------------------

@login_required
def ucenec_domov(request):
    ucenec = _zahtevaj_ucenca(request)
    predmeti = Predmet.objects.filter(ucenci=ucenec).order_by("ime")
    oddane_naloge_ids = Oddaja.objects.filter(ucenec=ucenec).values_list("naloga_id", flat=True)
    prihajajoce = (
        Naloga.objects.filter(predmet__ucenci=ucenec, rok__gte=timezone.now())
        .exclude(id__in=list(oddane_naloge_ids))
        .select_related("predmet")[:5]
    )
    oddaje = Oddaja.objects.filter(ucenec=ucenec)
    statistika = {
        "stevilo_predmetov": predmeti.count(),
        "stevilo_oddaj": oddaje.count(),
        "stevilo_ocen": oddaje.filter(ocena__isnull=False).count(),
        "povprecje": oddaje.filter(ocena__isnull=False).aggregate(p=Avg("ocena"))["p"],
    }
    return render(
        request,
        "portal/ucenec_domov.html",
        {"ucenec": ucenec, "predmeti": predmeti, "prihajajoce": prihajajoce, "statistika": statistika},
    )


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
            UcenecPredmet.objects.filter(ucenec=ucenec).exclude(predmet__in=izbrani).delete()
            messages.success(request, "Seznam predmetov je bil posodobljen.")
            return redirect("ucenec_domov")
    else:
        form = MojiPredmetiForm(initial={"predmeti": Predmet.objects.filter(ucenci=ucenec)})
    return render(request, "portal/moji_predmeti.html", {"form": form})


@login_required
def ucenec_gradiva(request, predmet_id):
    ucenec = _zahtevaj_ucenca(request)
    predmet = get_object_or_404(Predmet, pk=predmet_id)
    if not Predmet.objects.filter(pk=predmet_id, ucenci=ucenec).exists():
        raise PermissionDenied
    return render(request, "portal/ucenec_gradiva.html", {"predmet": predmet, "gradiva": predmet.gradiva.all()})


@login_required
def ucenec_naloge(request):
    ucenec = _zahtevaj_ucenca(request)
    naloge = list(
        Naloga.objects.filter(predmet__ucenci=ucenec).select_related("predmet")
    )
    oddaje_map = {o.naloga_id: o for o in Oddaja.objects.filter(ucenec=ucenec)}
    for naloga in naloge:
        naloga.moja_oddaja = oddaje_map.get(naloga.id)
    return render(request, "portal/ucenec_naloge.html", {"naloge": naloge, "zdaj": timezone.now()})


@login_required
def ucenec_naloga(request, pk):
    ucenec = _zahtevaj_ucenca(request)
    naloga = get_object_or_404(Naloga.objects.select_related("predmet"), pk=pk)
    if not Predmet.objects.filter(pk=naloga.predmet_id, ucenci=ucenec).exists():
        raise PermissionDenied
    oddaja = Oddaja.objects.filter(naloga=naloga, ucenec=ucenec).first()
    if request.method == "POST":
        form = OddajaForm(request.POST, request.FILES)
        if form.is_valid():
            if oddaja and not form.cleaned_data.get("potrdi_povozitev"):
                form.add_error(
                    "potrdi_povozitev",
                    "Za to nalogo že obstaja oddaja. Označi potrditev, da povoziš "
                    "prejšnjo datoteko (novo datoteko izberi ponovno).",
                )
            else:
                prepozno = timezone.now() > naloga.rok
                if oddaja:
                    oddaja.datoteka.delete(save=False)
                    oddaja.datoteka = form.cleaned_data["datoteka"]
                    oddaja.prepozno = prepozno
                    # ponovna oddaja razveljavi prejšnjo oceno (učitelj znova pregleda)
                    oddaja.ocena = None
                    oddaja.komentar = ""
                    oddaja.ocenjeno = None
                    oddaja.save()
                    messages.success(request, "Prejšnja oddaja je bila povožena z novo datoteko.")
                else:
                    oddaja = Oddaja(naloga=naloga, ucenec=ucenec,
                                    datoteka=form.cleaned_data["datoteka"], prepozno=prepozno)
                    oddaja.save()
                    messages.success(request, "Naloga je bila oddana.")
                if prepozno:
                    messages.warning(request, "Oddano po roku – oddaja je označena kot prepozna.")
                Obvestilo.obvesti(
                    _uporabnik_ucitelja(naloga.ustvaril),
                    f"Nova oddaja: {ucenec} – {naloga.naslov}",
                    reverse("ucitelj_naloga", args=[naloga.id]),
                )
                return redirect("ucenec_naloga", pk=naloga.id)
    else:
        form = OddajaForm()
    return render(
        request,
        "portal/ucenec_naloga.html",
        {"naloga": naloga, "oddaja": oddaja, "form": form, "zdaj": timezone.now()},
    )


@login_required
def moje_oddaje(request):
    ucenec = _zahtevaj_ucenca(request)
    oddaje = Oddaja.objects.filter(ucenec=ucenec).select_related("naloga", "naloga__predmet")
    return render(request, "portal/moje_oddaje.html", {"oddaje": oddaje})


# --- Nadzorna plošča in strani učitelja ---------------------------------

@login_required
def ucitelj_domov(request):
    ucitelj = _zahtevaj_ucitelja(request)
    predmeti = Predmet.objects.filter(ucitelji=ucitelj).order_by("ime")
    naloge = (
        Naloga.objects.filter(predmet__ucitelji=ucitelj)
        .select_related("predmet")
        .annotate(
            st_oddaj=Count("oddaje", distinct=True),
            st_neocenjenih=Count("oddaje", filter=Q(oddaje__ocena__isnull=True), distinct=True),
        )
    )
    statistika = {
        "stevilo_predmetov": predmeti.count(),
        "stevilo_nalog": naloge.count(),
        "neocenjene_oddaje": Oddaja.objects.filter(
            naloga__predmet__ucitelji=ucitelj, ocena__isnull=True
        ).count(),
    }
    return render(
        request,
        "portal/ucitelj_domov.html",
        {"ucitelj": ucitelj, "predmeti": predmeti, "naloge": naloge, "statistika": statistika},
    )


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
    ucitelj = _zahtevaj_ucitelja(request)
    predmet = _predmet_ucitelja_ali_403(ucitelj, predmet_id)
    return render(
        request,
        "portal/ucitelj_predmet.html",
        {"predmet": predmet, "gradiva": predmet.gradiva.all(), "naloge": predmet.naloge.all()},
    )


@login_required
def gradivo_nalozi(request):
    ucitelj = _zahtevaj_ucitelja(request)
    predmeti = Predmet.objects.filter(ucitelji=ucitelj)
    if request.method == "POST":
        form = GradivoForm(request.POST, request.FILES, dovoljeni_predmeti=predmeti)
        if form.is_valid():
            gradivo = form.save(commit=False)
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


# --- Naloge (učitelj) ---------------------------------------------------

@login_required
def ucitelj_naloge(request):
    ucitelj = _zahtevaj_ucitelja(request)
    naloge = (
        Naloga.objects.filter(predmet__ucitelji=ucitelj)
        .select_related("predmet")
        .annotate(st_oddaj=Count("oddaje", distinct=True))
    )
    return render(request, "portal/ucitelj_naloge.html", {"naloge": naloge, "zdaj": timezone.now()})


@login_required
def naloga_nova(request):
    ucitelj = _zahtevaj_ucitelja(request)
    predmeti = Predmet.objects.filter(ucitelji=ucitelj)
    if request.method == "POST":
        form = NalogaForm(request.POST, dovoljeni_predmeti=predmeti)
        if form.is_valid():
            naloga = form.save(commit=False)
            if not predmeti.filter(pk=naloga.predmet_id).exists():
                raise PermissionDenied
            naloga.ustvaril = ucitelj
            naloga.save()
            # obvesti vpisane učence
            for ucenec in Ucenec.objects.filter(predmeti=naloga.predmet):
                Obvestilo.obvesti(
                    _uporabnik_ucenca(ucenec),
                    f"Nova naloga pri {naloga.predmet.sifra}: {naloga.naslov}",
                    reverse("ucenec_naloga", args=[naloga.id]),
                )
            messages.success(request, "Naloga je bila ustvarjena.")
            return redirect("ucitelj_naloga", pk=naloga.id)
    else:
        form = NalogaForm(dovoljeni_predmeti=predmeti)
    return render(request, "portal/naloga_obrazec.html", {"form": form, "naslov": "Nova naloga"})


def _naloga_ucitelja_ali_403(ucitelj, pk):
    naloga = get_object_or_404(Naloga.objects.select_related("predmet"), pk=pk)
    if not Predmet.objects.filter(pk=naloga.predmet_id, ucitelji=ucitelj).exists():
        raise PermissionDenied
    return naloga


@login_required
def naloga_uredi(request, pk):
    ucitelj = _zahtevaj_ucitelja(request)
    naloga = _naloga_ucitelja_ali_403(ucitelj, pk)
    predmeti = Predmet.objects.filter(ucitelji=ucitelj)
    if request.method == "POST":
        form = NalogaForm(request.POST, instance=naloga, dovoljeni_predmeti=predmeti)
        if form.is_valid():
            form.save()
            messages.success(request, "Naloga je bila posodobljena.")
            return redirect("ucitelj_naloga", pk=naloga.id)
    else:
        form = NalogaForm(instance=naloga, dovoljeni_predmeti=predmeti)
    return render(request, "portal/naloga_obrazec.html", {"form": form, "naslov": "Uredi nalogo"})


@login_required
@require_http_methods(["GET", "POST"])
def naloga_izbrisi(request, pk):
    ucitelj = _zahtevaj_ucitelja(request)
    naloga = _naloga_ucitelja_ali_403(ucitelj, pk)
    if request.method == "POST":
        predmet_id = naloga.predmet_id
        for oddaja in naloga.oddaje.all():
            oddaja.datoteka.delete(save=False)
        naloga.delete()
        messages.success(request, "Naloga je bila izbrisana.")
        return redirect("ucitelj_predmet", predmet_id=predmet_id)
    return render(request, "portal/naloga_potrdi_brisanje.html", {"naloga": naloga})


@login_required
def ucitelj_naloga(request, pk):
    ucitelj = _zahtevaj_ucitelja(request)
    naloga = _naloga_ucitelja_ali_403(ucitelj, pk)
    oddaje = naloga.oddaje.select_related("ucenec").all()
    return render(request, "portal/ucitelj_naloga.html", {"naloga": naloga, "oddaje": oddaje, "zdaj": timezone.now()})


@login_required
def ucitelj_naloga_izvoz_csv(request, pk):
    """NADGRADNJA: izvoz seznama oddaj in ocen v CSV (Excel)."""
    ucitelj = _zahtevaj_ucitelja(request)
    naloga = _naloga_ucitelja_ali_403(ucitelj, pk)
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = f'attachment; filename="naloga_{naloga.id}_oddaje.csv"'
    writer = csv.writer(response)
    writer.writerow(["Učenec", "E-pošta", "Datum oddaje", "Prepozno", "Ocena", "Komentar"])
    for o in naloga.oddaje.select_related("ucenec").order_by("ucenec__priimek", "ucenec__ime"):
        writer.writerow([
            f"{o.ucenec.priimek} {o.ucenec.ime}",
            o.ucenec.email,
            timezone.localtime(o.oddano).strftime("%Y-%m-%d %H:%M:%S") if o.oddano else "",
            "DA" if o.prepozno else "NE",
            o.ocena or "",
            o.komentar or "",
        ])
    return response


@login_required
def oddaja_oceni(request, pk):
    ucitelj = _zahtevaj_ucitelja(request)
    oddaja = get_object_or_404(Oddaja.objects.select_related("naloga", "ucenec"), pk=pk)
    if not Predmet.objects.filter(pk=oddaja.naloga.predmet_id, ucitelji=ucitelj).exists():
        raise PermissionDenied
    if request.method == "POST":
        form = OcenaForm(request.POST, instance=oddaja)
        if form.is_valid():
            oddaja = form.save(commit=False)
            oddaja.ocenjeno = timezone.now()
            oddaja.save()
            Obvestilo.obvesti(
                _uporabnik_ucenca(oddaja.ucenec),
                f"Ocena ({oddaja.ocena}) pri nalogi: {oddaja.naloga.naslov}",
                reverse("ucenec_naloga", args=[oddaja.naloga_id]),
            )
            messages.success(request, "Oddaja je bila ocenjena.")
            return redirect("ucitelj_naloga", pk=oddaja.naloga_id)
    else:
        form = OcenaForm(instance=oddaja)
    return render(request, "portal/oddaja_oceni.html", {"form": form, "oddaja": oddaja})


# --- Obvestila ----------------------------------------------------------

@login_required
def obvestila(request):
    seznam = list(request.user.obvestila.all()[:50])
    # ob ogledu označimo neprebrana kot prebrana
    request.user.obvestila.filter(prebrano=False).update(prebrano=True)
    return render(request, "portal/obvestila.html", {"obvestila": seznam})


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
        return Predmet.objects.filter(pk=oddaja.naloga.predmet_id, ucitelji=user.profil.ucitelj).exists()
    if je_ucenec(user):
        return oddaja.ucenec_id == user.profil.ucenec_id
    return False


@login_required
def gradivo_prenos(request, pk):
    gradivo = get_object_or_404(Gradivo, pk=pk)
    if not _sme_do_gradiva(request.user, gradivo):
        raise PermissionDenied
    try:
        return FileResponse(gradivo.datoteka.open("rb"), as_attachment=True, filename=gradivo.ime_datoteke())
    except FileNotFoundError:
        raise Http404("Datoteka ne obstaja.")


@login_required
def oddaja_prenos(request, pk):
    oddaja = get_object_or_404(Oddaja.objects.select_related("naloga"), pk=pk)
    if not _sme_do_oddaje(request.user, oddaja):
        raise PermissionDenied
    try:
        return FileResponse(oddaja.datoteka.open("rb"), as_attachment=True, filename=oddaja.ime_datoteke())
    except FileNotFoundError:
        raise Http404("Datoteka ne obstaja.")
