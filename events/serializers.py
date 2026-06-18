from rest_framework import serializers
from .models import Event, EventRSVP
from members.serializers import MemberProfileSerializer

class EventSerializer(serializers.ModelSerializer):
    rsvp_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'image', 'created_by', 'created_at', 'rsvp_count']
        read_only_fields = ['created_by', 'created_at']  # ← ADD THIS LINE

class EventRSVPSerializer(serializers.ModelSerializer):
    member_details = MemberProfileSerializer(source='member', read_only=True)
    
    class Meta:
        model = EventRSVP
        fields = ['id', 'event', 'member', 'member_details', 'will_attend', 'guests', 'rsvp_date']

class RSVPSerializer(serializers.Serializer):
    """For submitting RSVP"""
    event_id = serializers.IntegerField()
    will_attend = serializers.BooleanField(default=True)
    guests = serializers.IntegerField(default=0)
    
    def validate_event_id(self, value):
        if not Event.objects.filter(id=value).exists():
            raise serializers.ValidationError("Event not found")
        return value