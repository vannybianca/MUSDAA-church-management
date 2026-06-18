from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import PrayerRequest, PrayerRecord
from .serializers import PrayerRequestSerializer, CreatePrayerSerializer, PraySerializer
from members.models import MemberProfile

class PrayerRequestListView(generics.ListCreateAPIView):
    """List public prayer requests OR create new prayer request"""
    serializer_class = PrayerRequestSerializer
    
    def get_queryset(self):
        # Public prayers (everyone can see)
        # Private prayers (only admin can see - will implement later)
        return PrayerRequest.objects.filter(is_public=True).annotate(
            prayer_count=Count('prayers')
        ).order_by('-created_at')
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        member = MemberProfile.objects.get(user=self.request.user)
        serializer.save(member=member)

class PrayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a prayer request"""
    queryset = PrayerRequest.objects.all()
    serializer_class = PrayerRequestSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class PrayView(APIView):
    """Member prays for a prayer request (increases count)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PraySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        prayer_request = PrayerRequest.objects.get(id=serializer.validated_data['prayer_request_id'])
        member = MemberProfile.objects.get(user=request.user)
        
        # Check if already prayed for this
        existing, created = PrayerRecord.objects.get_or_create(
            prayer_request=prayer_request,
            member=member
        )
        
        if created:
            # Update the prayer count
            prayer_request.prayed_count = PrayerRecord.objects.filter(prayer_request=prayer_request).count()
            prayer_request.save()
            return Response({'message': 'Prayer recorded', 'prayed_count': prayer_request.prayed_count})
        else:
            return Response({'message': 'You already prayed for this request'}, status=status.HTTP_400_BAD_REQUEST)

class MyPrayersView(generics.ListAPIView):
    """List prayers submitted by the logged-in member"""
    serializer_class = PrayerRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        member = MemberProfile.objects.get(user=self.request.user)
        return PrayerRequest.objects.filter(member=member)