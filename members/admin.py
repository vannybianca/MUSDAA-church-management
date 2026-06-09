from django.contrib import admin
from .models import MemberProfile

class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'occupation', 'join_date', 'is_active')
    list_filter = ('gender', 'marital_status', 'is_active', 'join_date')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

admin.site.register(MemberProfile, MemberProfileAdmin)