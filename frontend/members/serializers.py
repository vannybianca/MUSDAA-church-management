from rest_framework import serializers
from .models import MemberProfile
from accounts.serializers import UserSerializer

class MemberProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = MemberProfile
        fields = '__all__'
        read_only_fields = ['id', 'join_date']