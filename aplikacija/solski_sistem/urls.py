from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    # Prijava / odjava (Djangovi vgrajeni pogledi; gesla so zgoščena)
    path(
        "prijava/",
        auth_views.LoginView.as_view(template_name="registration/prijava.html"),
        name="prijava",
    ),
    path("odjava/", auth_views.LogoutView.as_view(), name="odjava"),
    # Portal (registracija, pogleda učitelja in učenca, prenos datotek)
    path("", include("portal.urls")),
    # Administratorski CRUD (predmeti, učitelji, učenci)
    path("", include("administracija.urls")),
]
