from django.db import models
from django.conf import settings

class SermonSeries(models.Model):
    """A series of sermons (e.g., "Faith Series" with 5 sermons)"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='series/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-start_date']

class Sermon(models.Model):
    """Individual sermon with audio file"""
    title = models.CharField(max_length=200)
    series = models.ForeignKey(SermonSeries, on_delete=models.SET_NULL, null=True, blank=True, related_name='sermons')
    speaker = models.CharField(max_length=100)
    date = models.DateField()
    bible_verses = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='sermons/audio/')
    duration = models.CharField(max_length=20, blank=True)  # e.g., "45:23"
    listens = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.speaker}"
    
    class Meta:
        ordering = ['-date']