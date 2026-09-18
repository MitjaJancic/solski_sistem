from django.contrib import admin

from .models import Predmet, Ucenec, UcenecPredmet, Ucitelj, UciteljPredmet


class UciteljPredmetInline(admin.TabularInline):
    model = UciteljPredmet
    extra = 1


class UcenecPredmetInline(admin.TabularInline):
    model = UcenecPredmet
    extra = 1


@admin.register(Predmet)
class PredmetAdmin(admin.ModelAdmin):
    list_display = ("sifra", "ime")
    search_fields = ("sifra", "ime")


@admin.register(Ucitelj)
class UciteljAdmin(admin.ModelAdmin):
    list_display = ("priimek", "ime", "email")
    search_fields = ("priimek", "ime", "email")
    inlines = [UciteljPredmetInline]


@admin.register(Ucenec)
class UcenecAdmin(admin.ModelAdmin):
    list_display = ("priimek", "ime", "email")
    search_fields = ("priimek", "ime", "email")
    inlines = [UcenecPredmetInline]
