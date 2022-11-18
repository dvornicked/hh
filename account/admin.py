from django.contrib import admin
from .models import Profile, Subscription


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'notify']
    list_editable = ['notify']


@admin.register(Subscription)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city']
    list_editable = ['city']
