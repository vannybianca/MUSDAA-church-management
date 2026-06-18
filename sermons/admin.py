from django.contrib import admin
from .models import SermonSeries, Sermon

@admin.register(SermonSeries)
class SermonSeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date']
    search_fields = ['title']

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'date', 'series', 'listens', 'downloads']
    list_filter = ['speaker', 'date', 'series']
    search_fields = ['title', 'speaker', 'bible_verses']