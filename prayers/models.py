from django.db import models
from members.models import MemberProfile

class PrayerRequest(models.Model):
    """A prayer request submitted by a member"""
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='prayer_requests')
    request = models.TextField()
    is_public = models.BooleanField(default=True)  # Public = everyone sees, Private = only pastors
    prayed_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)
    testimony = models.TextField(blank=True)  # Story of how prayer was answered
    
    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.request[:50]}"
    
    class Meta:
        ordering = ['-created_at']

class PrayerRecord(models.Model):
    """Records who prayed for a request"""
    prayer_request = models.ForeignKey(PrayerRequest, on_delete=models.CASCADE, related_name='prayers')
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE)
    prayed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['prayer_request', 'member']  # Can't pray twice for same request
    
    def __str__(self):
        return f"{self.member.user.get_full_name()} prayed for {self.prayer_request.id}"