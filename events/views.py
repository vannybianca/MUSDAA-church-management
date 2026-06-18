from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import Event, EventRSVP
from .serializers import EventSerializer, EventRSVPSerializer, RSVPSerializer
from members.models import MemberProfile

class EventListView(generics.ListCreateAPIView):
    """List all events OR create a new event (admin only)"""
    queryset = Event.objects.annotate(rsvp_count=Count('rsvps'))
    serializer_class = EventSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a single event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class RSVPView(APIView):
    """Member submits RSVP for an event"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = RSVPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        event = Event.objects.get(id=serializer.validated_data['event_id'])
        member = MemberProfile.objects.get(user=request.user)
        
        # Update existing or create new RSVP
        rsvp, created = EventRSVP.objects.update_or_create(
            event=event,
            member=member,
            defaults={
                'will_attend': serializer.validated_data['will_attend'],
                'guests': serializer.validated_data['guests']
            }
        )
        
        return Response({
            'success': True,
            'message': 'RSVP updated',
            'rsvp': EventRSVPSerializer(rsvp).data
        })

class EventRSVPListView(generics.ListAPIView):
    """List all RSVPs for an event (admin only)"""
    serializer_class = EventRSVPSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return EventRSVP.objects.filter(event_id=event_id)