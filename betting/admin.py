# betting/admin.py
from django.contrib import admin
from .models import Event, Option, Bet

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)
    ordering = ("-created_at",)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "name")
    list_filter = ("event",)
    search_fields = ("name",)


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ("id", "option", "amount", "created_at")
    list_filter = ("option__event",)
    search_fields = ("option__name",)
    ordering = ("-created_at",)
