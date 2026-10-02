from django.urls import path

from . import views

urlpatterns = [
    # Začetna stran: razcep glede na vlogo (admin / učitelj / učenec / gost)
    path("", views.zacetna, name="zacetna"),
    # Registracija (prijava/odjava sta v glavnem urls.py prek Djangovih pogledov)
    path("registracija/", views.registracija, name="registracija"),
    # Učenec
    path("ucenec/", views.ucenec_domov, name="ucenec_domov"),
    path("ucenec/profil/", views.profil_uredi, name="profil_uredi"),
    path("ucenec/predmeti/", views.moji_predmeti, name="moji_predmeti"),
    path("ucenec/predmet/<int:predmet_id>/gradiva/", views.ucenec_gradiva, name="ucenec_gradiva"),
    path("ucenec/oddaje/", views.moje_oddaje, name="moje_oddaje"),
    path("ucenec/oddaje/nova/", views.oddaja_nova, name="oddaja_nova"),
    # Učitelj
    path("ucitelj/", views.ucitelj_predmeti, name="ucitelj_predmeti"),
    path("ucitelj/predmet/<int:predmet_id>/", views.ucitelj_predmet, name="ucitelj_predmet"),
    path("ucitelj/gradivo/nalozi/", views.gradivo_nalozi, name="gradivo_nalozi"),
    path("ucitelj/gradivo/<int:pk>/izbrisi/", views.gradivo_izbrisi, name="gradivo_izbrisi"),
    # Zaščiteni prenos datotek
    path("prenos/gradivo/<int:pk>/", views.gradivo_prenos, name="gradivo_prenos"),
    path("prenos/oddaja/<int:pk>/", views.oddaja_prenos, name="oddaja_prenos"),
]
