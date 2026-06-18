from django.db import models
from django.conf import settings
from members.models import MemberProfile

class Event(models.Model):
    """An event like Youth Conference, Prayer Night, etc."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['date']

class EventRSVP(models.Model):
    """Records who is coming to an event"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE)
    will_attend = models.BooleanField(default=True)
    guests = models.IntegerField(default=0)
    rsvp_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'member']  # One RSVP per member per event
    
    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.event.title}"