from django.urls import path

from . import views

urlpatterns = [
    path("", views.zacetna, name="zacetna"),
    path("registracija/", views.registracija, name="registracija"),
    path("obvestila/", views.obvestila, name="obvestila"),
    # Učenec
    path("ucenec/", views.ucenec_domov, name="ucenec_domov"),
    path("ucenec/profil/", views.profil_uredi, name="profil_uredi"),
    path("ucenec/predmeti/", views.moji_predmeti, name="moji_predmeti"),
    path("ucenec/predmet/<int:predmet_id>/gradiva/", views.ucenec_gradiva, name="ucenec_gradiva"),
    path("ucenec/naloge/", views.ucenec_naloge, name="ucenec_naloge"),
    path("ucenec/naloga/<int:pk>/", views.ucenec_naloga, name="ucenec_naloga"),
    path("ucenec/oddaje/", views.moje_oddaje, name="moje_oddaje"),
    # Učitelj
    path("ucitelj/", views.ucitelj_domov, name="ucitelj_domov"),
    path("ucitelj/predmeti/", views.ucitelj_predmeti, name="ucitelj_predmeti"),
    path("ucitelj/predmet/<int:predmet_id>/", views.ucitelj_predmet, name="ucitelj_predmet"),
    path("ucitelj/gradivo/nalozi/", views.gradivo_nalozi, name="gradivo_nalozi"),
    path("ucitelj/gradivo/<int:pk>/izbrisi/", views.gradivo_izbrisi, name="gradivo_izbrisi"),
    path("ucitelj/naloge/", views.ucitelj_naloge, name="ucitelj_naloge"),
    path("ucitelj/naloga/nova/", views.naloga_nova, name="naloga_nova"),
    path("ucitelj/naloga/<int:pk>/", views.ucitelj_naloga, name="ucitelj_naloga"),
    path("ucitelj/naloga/<int:pk>/izvoz/", views.ucitelj_naloga_izvoz_csv, name="ucitelj_naloga_izvoz_csv"),
    path("ucitelj/naloga/<int:pk>/uredi/", views.naloga_uredi, name="naloga_uredi"),
    path("ucitelj/naloga/<int:pk>/izbrisi/", views.naloga_izbrisi, name="naloga_izbrisi"),
    path("ucitelj/oddaja/<int:pk>/oceni/", views.oddaja_oceni, name="oddaja_oceni"),
    # Zaščiteni prenos datotek
    path("prenos/gradivo/<int:pk>/", views.gradivo_prenos, name="gradivo_prenos"),
    path("prenos/oddaja/<int:pk>/", views.oddaja_prenos, name="oddaja_prenos"),
]
