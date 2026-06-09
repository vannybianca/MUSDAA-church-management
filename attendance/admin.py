from django.contrib import admin
from .models import ServiceType, Service, Attendance

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'start_time', 'is_active']
    list_filter = ['is_active']
    search_fields = ['display_name', 'name']
    list_editable = ['is_active']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_type', 'date', 'speaker', 'total_attendance']
    list_filter = ['service_type', 'date', 'service_type__is_active']
    search_fields = ['speaker', 'theme', 'notes']
    readonly_fields = ['total_attendance']
    date_hierarchy = 'date'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['member', 'service', 'checked_in_at', 'checked_by']
    list_filter = ['service__service_type', 'service__date']
    search_fields = ['member__user__first_name', 'member__user__last_name', 'member__user__email']
    readonly_fields = ['checked_in_at']
    date_hierarchy = 'checked_in_at'