from django.contrib import admin
from .models import Event, EventRSVP

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location']
    list_filter = ['date']
    search_fields = ['title', 'description']

@admin.register(EventRSVP)
class EventRSVPAdmin(admin.ModelAdmin):
    list_display = ['event', 'member', 'will_attend', 'guests']
    list_filter = ['event', 'will_attend']