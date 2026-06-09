from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from .models import ServiceType, Service, Attendance
from .serializers import (
    ServiceTypeSerializer, ServiceSerializer, AttendanceSerializer, 
    CheckInSerializer, ServiceCreateSerializer
)
from members.models import MemberProfile


class ServiceTypeListView(generics.ListAPIView):
    """List all active service types"""
    queryset = ServiceType.objects.filter(is_active=True)
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceListView(generics.ListAPIView):
    """List services (upcoming and past)"""
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Service.objects.all().annotate(
            attendance_count=Count('attendances')
        )
        
        # Filter by service type
        service_type = self.request.query_params.get('service_type')
        if service_type:
            queryset = queryset.filter(service_type__name=service_type)
        
        # Filter by date range
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)
        
        # Filter by year/month
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year and month:
            queryset = queryset.filter(date__year=year, date__month=month)
        
        # Upcoming vs past
        upcoming = self.request.query_params.get('upcoming')
        if upcoming == 'true':
            queryset = queryset.filter(date__gte=timezone.now().date())
        elif upcoming == 'false':
            queryset = queryset.filter(date__lt=timezone.now().date())
        
        return queryset.order_by('-date')


class ServiceCreateView(generics.CreateAPIView):
    """Create a new service (admin only)"""
    serializer_class = ServiceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a service"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method != 'GET':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class CheckInView(APIView):
    """Record attendance for a member"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = CheckInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service_id = serializer.validated_data['service_id']
        member_id = serializer.validated_data.get('member_id')
        
        # Get member profile
        if member_id:
            # Admin checking in another member
            if not request.user.role in ['admin', 'pastor']:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            member = MemberProfile.objects.get(id=member_id)
        else:
            # Member checking themselves in
            member = MemberProfile.objects.get(user=request.user)
        
        service = Service.objects.get(id=service_id)
        
        # Check if already checked in
        existing = Attendance.objects.filter(member=member, service=service).first()
        if existing:
            return Response({
                'error': 'Already checked in to this service',
                'attendance_id': existing.id,
                'checked_in_at': existing.checked_in_at
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create attendance record
        attendance = Attendance.objects.create(
            member=member,
            service=service,
            checked_by=request.user if request.user.role in ['admin', 'pastor'] else None
        )
        
        # Update service total attendance
        service.total_attendance = Attendance.objects.filter(service=service).count()
        service.save()
        
        return Response({
            'success': True,
            'message': 'Check-in successful',
            'attendance': AttendanceSerializer(attendance).data
        }, status=status.HTTP_201_CREATED)


class MyAttendanceView(generics.ListAPIView):
    """Get current user's attendance history"""
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        member = MemberProfile.objects.get(user=self.request.user)
        return Attendance.objects.filter(member=member).order_by('-service__date')


class ServiceAttendanceView(generics.ListAPIView):
    """Get all attendees for a specific service"""
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return Attendance.objects.filter(service_id=service_id).select_related('member__user')


class AttendanceStatsView(APIView):
    """Get attendance statistics for dashboard"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        now = timezone.now()
        
        # Current month stats
        month_services = Service.objects.filter(
            date__year=now.year, 
            date__month=now.month
        )
        month_attendance = Attendance.objects.filter(
            service__date__year=now.year, 
            service__date__month=now.month
        )
        
        # Previous month stats
        prev_month = now - timedelta(days=30)
        prev_attendance = Attendance.objects.filter(
            service__date__year=prev_month.year,
            service__date__month=prev_month.month
        ).count()
        
        # Calculate growth
        current_count = month_attendance.count()
        growth = 0
        if prev_attendance > 0:
            growth = ((current_count - prev_attendance) / prev_attendance) * 100
        
        # Get attendance by service type
        attendance_by_type = []
        for st in ServiceType.objects.filter(is_active=True):
            count = Attendance.objects.filter(
                service__service_type=st,
                service__date__year=now.year,
                service__date__month=now.month
            ).count()
            attendance_by_type.append({
                'service_type': st.display_name,
                'count': count
            })
        
        # Recent attendance (last 7 days)
        week_ago = now.date() - timedelta(days=7)
        recent_attendance = Attendance.objects.filter(
            checked_in_at__date__gte=week_ago
        ).select_related('member__user', 'service')
        
        recent_data = []
        for att in recent_attendance[:10]:
            recent_data.append({
                'member': att.member.user.get_full_name(),
                'service': str(att.service),
                'time': att.checked_in_at.strftime('%Y-%m-%d %H:%M')
            })
        
        return Response({
            'current_month': now.strftime('%B %Y'),
            'total_services': month_services.count(),
            'total_attendance': current_count,
            'average_per_service': current_count // month_services.count() if month_services.count() > 0 else 0,
            'growth_percentage': round(growth, 1),
            'by_service_type': attendance_by_type,
            'recent_checkins': recent_data
        })


class AttendanceReportView(APIView):
    """Generate attendance report for a date range"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        
        if not from_date or not to_date:
            return Response({'error': 'from_date and to_date required'}, status=400)
        
        services = Service.objects.filter(
            date__gte=from_date,
            date__lte=to_date
        ).annotate(attendance_count=Count('attendances'))
        
        total_members = MemberProfile.objects.filter(is_active=True).count()
        total_attendance = sum([s.attendance_count for s in services])
        
        report_data = []
        for service in services:
            report_data.append({
                'date': service.date,
                'service_type': service.service_type.display_name,
                'speaker': service.speaker,
                'attendance': service.attendance_count,
                'percentage': round((service.attendance_count / total_members) * 100, 1) if total_members > 0 else 0
            })
        
        return Response({
            'period': f"{from_date} to {to_date}",
            'total_services': services.count(),
            'total_attendance': total_attendance,
            'unique_members': Attendance.objects.filter(
                service__date__gte=from_date,
                service__date__lte=to_date
            ).values('member').distinct().count(),
            'details': report_data
        })