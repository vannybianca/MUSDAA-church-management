from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import SermonSeries, Sermon
from .serializers import SermonSeriesSerializer, SermonSerializer, SermonCreateSerializer

class SermonSeriesListView(generics.ListCreateAPIView):
    """List all sermon series"""
    queryset = SermonSeries.objects.annotate(sermon_count=Count('sermons'))
    serializer_class = SermonSeriesSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class SermonListView(generics.ListCreateAPIView):
    """List all sermons OR upload new sermon (admin only)"""
    serializer_class = SermonSerializer
    
    def get_queryset(self):
        queryset = Sermon.objects.all()
        
        # Filter by series
        series = self.request.query_params.get('series')
        if series:
            queryset = queryset.filter(series_id=series)
        
        # Filter by speaker
        speaker = self.request.query_params.get('speaker')
        if speaker:
            queryset = queryset.filter(speaker__icontains=speaker)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(speaker__icontains=search) |
                models.Q(bible_verses__icontains=search)
            )
        
        return queryset.order_by('-date')
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save()

class SermonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a sermon"""
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class SermonListenView(APIView):
    """Track when someone listens to a sermon (increases count)"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, pk):
        try:
            sermon = Sermon.objects.get(id=pk)
            sermon.listens += 1
            sermon.save()
            return Response({'listens': sermon.listens})
        except Sermon.DoesNotExist:
            return Response({'error': 'Sermon not found'}, status=404)

class SermonDownloadView(APIView):
    """Track when someone downloads a sermon"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, pk):
        try:
            sermon = Sermon.objects.get(id=pk)
            sermon.downloads += 1
            sermon.save()
            return Response({'downloads': sermon.downloads})
        except Sermon.DoesNotExist:
            return Response({'error': 'Sermon not found'}, status=404)