from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import PredmetForm, UcenecForm, UciteljForm
from .models import Predmet, Ucenec, Ucitelj


def zacetna(request):
    kontekst = {
        "stevilo_predmetov": Predmet.objects.count(),
        "stevilo_uciteljev": Ucitelj.objects.count(),
        "stevilo_ucencev": Ucenec.objects.count(),
    }
    return render(request, "administracija/zacetna.html", kontekst)


# --- Predmeti -----------------------------------------------------------

class PredmetListView(ListView):
    model = Predmet
    template_name = "administracija/predmet_seznam.html"
    context_object_name = "predmeti"
    paginate_by = 20


class PredmetCreateView(SuccessMessageMixin, CreateView):
    model = Predmet
    form_class = PredmetForm
    template_name = "administracija/obrazec.html"
    success_url = reverse_lazy("predmet_seznam")
    success_message = "Predmet je bil dodan."
    extra_context = {"naslov": "Nov predmet"}


class PredmetUpdateView(SuccessMessageMixin, UpdateView):
    model = Predmet
    form_class = PredmetForm
    template_name = "administracija/obrazec.html"
    success_url = reverse_lazy("predmet_seznam")
    success_message = "Predmet je bil posodobljen."
    extra_context = {"naslov": "Uredi predmet"}


class PredmetDeleteView(DeleteView):
    model = Predmet
    template_name = "administracija/potrdi_brisanje.html"
    success_url = reverse_lazy("predmet_seznam")

    def form_valid(self, form):
        messages.success(self.request, "Predmet je bil izbrisan.")
        return super().form_valid(form)


# --- Učitelji -------------------------------------------------------------

class UciteljListView(ListView):
    model = Ucitelj
    template_name = "administracija/ucitelj_seznam.html"
    context_object_name = "ucitelji"
    paginate_by = 20

    def get_queryset(self):
        return Ucitelj.objects.prefetch_related("predmeti")


class UciteljCreateView(SuccessMessageMixin, CreateView):
    model = Ucitelj
    form_class = UciteljForm
    template_name = "administracija/obrazec.html"
    success_url = reverse_lazy("ucitelj_seznam")
    success_message = "Učitelj je bil dodan."
    extra_context = {"naslov": "Nov učitelj"}


class UciteljUpdateView(SuccessMessageMixin, UpdateView):
    model = Ucitelj
    form_class = UciteljForm
    template_name = "administracija/obrazec.html"
    success_url = reverse_lazy("ucitelj_seznam")
    success_message = "Učitelj je bil posodobljen."
    extra_context = {"naslov": "Uredi učitelja"}


class UciteljDeleteView(DeleteView):
    model = Ucitelj
    template_name = "administracija/potrdi_brisanje.html"
    success_url = reverse_lazy("ucitelj_seznam")

    def form_valid(self, form):
        messages.success(self.request, "Učitelj je bil izbrisan.")
        return super().form_valid(form)


# --- Učenci -----------------------------------------------------------

class UcenecListView(ListView):
    model = Ucenec
    template_name = "administracija/ucenec_seznam.html"
    context_object_name = "ucenci"
    paginate_by = 20

    def get_queryset(self):
        return Ucenec.objects.prefetch_related("predmeti")


class UcenecCreateView(SuccessMessageMixin, CreateView):
    model = Ucenec
    form_class = UcenecForm
    template_name = "administracija/obrazec.html"
    success_url = reverse_lazy("ucenec_seznam")
    success_message = "Učenec je bil dodan."
    extra_context = {"naslov": "Nov učenec"}


class UcenecUpdateView(SuccessMessageMixin, UpdateView):
    model = Ucenec
    form_class = UcenecForm
    template_name = "administracija/obrazec.html"
    success_url = reverse_lazy("ucenec_seznam")
    success_message = "Učenec je bil posodobljen."
    extra_context = {"naslov": "Uredi učenca"}


class UcenecDeleteView(DeleteView):
    model = Ucenec
    template_name = "administracija/potrdi_brisanje.html"
    success_url = reverse_lazy("ucenec_seznam")

    def form_valid(self, form):
        messages.success(self.request, "Učenec je bil izbrisan.")
        return super().form_valid(form)
