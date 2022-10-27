from django.contrib import admin
from .models import City, Language, Vacancy


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    exclude = ['slug']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    exclude = ['slug']


@admin.register(Vacancy)
class Vacancy(admin.ModelAdmin):
    pass
