from django.contrib import admin

from .models import Gradivo, Naloga, Obvestilo, Oddaja, Profil


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


@admin.register(Naloga)
class NalogaAdmin(admin.ModelAdmin):
    list_display = ("naslov", "predmet", "rok", "ustvaril", "ustvarjeno")
    list_filter = ("predmet",)
    search_fields = ("naslov",)


@admin.register(Oddaja)
class OddajaAdmin(admin.ModelAdmin):
    list_display = ("naloga", "ucenec", "oddano", "prepozno", "ocena", "ocenjeno")
    list_filter = ("naloga__predmet", "prepozno")
    search_fields = ("naloga__naslov", "ucenec__priimek")


@admin.register(Obvestilo)
class ObvestiloAdmin(admin.ModelAdmin):
    list_display = ("prejemnik", "besedilo", "prebrano", "ustvarjeno")
    list_filter = ("prebrano",)
