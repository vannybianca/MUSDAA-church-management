from rest_framework import serializers
from .models import PrayerRequest, PrayerRecord
from members.serializers import MemberProfileSerializer

class PrayerRequestSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PrayerRequest
        fields = ['id', 'member', 'member_name', 'request', 'is_public', 'prayed_count', 'created_at', 'answered', 'testimony']
        read_only_fields = ['member', 'prayed_count', 'created_at']  # ← ADD THIS LINE
    
    def get_member_name(self, obj):
        return obj.member.user.get_full_name() or obj.member.user.username

class CreatePrayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerRequest
        fields = ['request', 'is_public']

class PraySerializer(serializers.Serializer):
    """For submitting a prayer for someone's request"""
    prayer_request_id = serializers.IntegerField()