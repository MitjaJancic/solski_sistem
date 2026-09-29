from django.contrib import admin

from .models import Gradivo, Oddaja, Profil


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ("uporabnik", "vloga", "ucitelj", "ucenec")
    list_filter = ("vloga",)
    search_fields = ("uporabnik__username", "uporabnik__email")


@admin.register(Gradivo)
class GradivoAdmin(admin.ModelAdmin):
    list_display = ("naslov", "predmet", "nalozil", "ustvarjeno")
    list_filter = ("predmet",)
    search_fields = ("naslov",)


@admin.register(Oddaja)
class OddajaAdmin(admin.ModelAdmin):
    list_display = ("naslov", "predmet", "ucenec", "oddano")
    list_filter = ("predmet",)
    search_fields = ("naslov", "ucenec__priimek")
