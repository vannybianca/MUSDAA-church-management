from rest_framework import serializers
from .models import SermonSeries, Sermon

class SermonSeriesSerializer(serializers.ModelSerializer):
    sermon_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = SermonSeries
        fields = ['id', 'title', 'description', 'cover_image', 'start_date', 'end_date', 'sermon_count']

class SermonSerializer(serializers.ModelSerializer):
    series_title = serializers.CharField(source='series.title', read_only=True)
    
    class Meta:
        model = Sermon
        fields = ['id', 'title', 'series', 'series_title', 'speaker', 'date', 
                'bible_verses', 'description', 'audio_file', 'duration', 
                'listens', 'downloads', 'created_at']

class SermonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sermon
        fields = ['title', 'series', 'speaker', 'date', 'bible_verses', 'description', 'audio_file', 'duration']