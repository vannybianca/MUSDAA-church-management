from django.db import models
from django.conf import settings
from members.models import MemberProfile

class ServiceType(models.Model):
    """Types of church services (Sunday, Wednesday, etc.)"""
    SERVICE_CHOICES = (
        ('kikoni', 'Kikoni Fellowship'),
        ('afrostone', 'Afrostone Fellowship'),
        ('nkrukote', 'Nkrukote Fellowship'),
        ('tuesday', 'Tuesday Fellowship'),
        ('lumbox', 'Lumbox Fellowship'),
        ('mitchelex', 'Uh Mitchelex Fellowship'),
        ('sabbath', 'Sabbath'),
    )
    
    name = models.CharField(max_length=50, choices=SERVICE_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    start_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        ordering = ['name']


class Service(models.Model):
    """Individual service instance"""
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='services')
    date = models.DateField()
    theme = models.CharField(max_length=200, blank=True)
    speaker = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    total_attendance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.service_type.display_name} - {self.date}"
    
    class Meta:
        ordering = ['-date']
        unique_together = ['service_type', 'date']


class Attendance(models.Model):
    """Record of a member attending a service"""
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='attendances')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='attendances')
    checked_in_at = models.DateTimeField(auto_now_add=True)
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ['member', 'service']
        ordering = ['-checked_in_at']
    
    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.service}"