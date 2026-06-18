from django.contrib import admin
from .models import PrayerRequest, PrayerRecord

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ['member', 'request', 'is_public', 'prayed_count', 'answered', 'created_at']
    list_filter = ['is_public', 'answered', 'created_at']
    search_fields = ['request', 'testimony']

@admin.register(PrayerRecord)
class PrayerRecordAdmin(admin.ModelAdmin):
    list_display = ['prayer_request', 'member', 'prayed_at']