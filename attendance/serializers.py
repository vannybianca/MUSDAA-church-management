from rest_framework import serializers
from .models import ServiceType, Service, Attendance
from members.serializers import MemberProfileSerializer
from members.models import MemberProfile

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'display_name', 'start_time', 'is_active']


class ServiceSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='service_type.display_name', read_only=True)
    attendance_count = serializers.IntegerField(read_only=True)
    attendance_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ['id', 'service_type', 'service_type_display', 'date', 'theme', 
                'speaker', 'notes', 'total_attendance', 'attendance_count', 
                'attendance_percentage', 'created_at']
    
    def get_attendance_percentage(self, obj):
        # This would need total members count - can be added later
        return 0


class AttendanceSerializer(serializers.ModelSerializer):
    member_details = MemberProfileSerializer(source='member', read_only=True)
    service_details = ServiceSerializer(source='service', read_only=True)
    member_name = serializers.SerializerMethodField()
    service_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = ['id', 'member', 'member_details', 'member_name', 'service', 
                'service_details', 'service_info', 'checked_in_at', 'checked_by', 'notes']
        read_only_fields = ['checked_in_at']
    
    def get_member_name(self, obj):
        return obj.member.user.get_full_name() or obj.member.user.username
    
    def get_service_info(self, obj):
        return f"{obj.service.service_type.display_name} - {obj.service.date}"


class CheckInSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    member_id = serializers.IntegerField(required=False)
    
    def validate_service_id(self, value):
        if not Service.objects.filter(id=value).exists():
            raise serializers.ValidationError("Service not found")
        return value
    
    def validate_member_id(self, value):
        if value and not MemberProfile.objects.filter(id=value).exists():
            raise serializers.ValidationError("Member not found")
        return value


class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_type', 'date', 'theme', 'speaker', 'notes']