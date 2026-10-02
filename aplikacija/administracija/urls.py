from django.urls import path

from . import views

urlpatterns = [
    # Predmeti
    path("predmeti/", views.PredmetListView.as_view(), name="predmet_seznam"),
    path("predmeti/dodaj/", views.PredmetCreateView.as_view(), name="predmet_dodaj"),
    path("predmeti/<int:pk>/uredi/", views.PredmetUpdateView.as_view(), name="predmet_uredi"),
    path("predmeti/<int:pk>/izbrisi/", views.PredmetDeleteView.as_view(), name="predmet_izbrisi"),
    # Učitelji
    path("ucitelji/", views.UciteljListView.as_view(), name="ucitelj_seznam"),
    path("ucitelji/dodaj/", views.UciteljCreateView.as_view(), name="ucitelj_dodaj"),
    path("ucitelji/<int:pk>/uredi/", views.UciteljUpdateView.as_view(), name="ucitelj_uredi"),
    path("ucitelji/<int:pk>/izbrisi/", views.UciteljDeleteView.as_view(), name="ucitelj_izbrisi"),
    # Učenci
    path("ucenci/", views.UcenecListView.as_view(), name="ucenec_seznam"),
    path("ucenci/dodaj/", views.UcenecCreateView.as_view(), name="ucenec_dodaj"),
    path("ucenci/<int:pk>/uredi/", views.UcenecUpdateView.as_view(), name="ucenec_uredi"),
    path("ucenci/<int:pk>/izbrisi/", views.UcenecDeleteView.as_view(), name="ucenec_izbrisi"),
]
