from django.urls import path
from .views import (
    ServiceTypeListView, ServiceListView, ServiceCreateView, ServiceDetailView,
    CheckInView, MyAttendanceView, ServiceAttendanceView, 
    AttendanceStatsView, AttendanceReportView
)

urlpatterns = [
    # Service Types
    path('service-types/', ServiceTypeListView.as_view(), name='service-types'),
    
    # Services
    path('services/', ServiceListView.as_view(), name='services'),
    path('services/create/', ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    
    # Attendance
    path('checkin/', CheckInView.as_view(), name='checkin'),
    path('my-attendance/', MyAttendanceView.as_view(), name='my-attendance'),
    path('service/<int:service_id>/attendance/', ServiceAttendanceView.as_view(), name='service-attendance'),
    
    # Reports & Stats
    path('stats/', AttendanceStatsView.as_view(), name='attendance-stats'),
    path('report/', AttendanceReportView.as_view(), name='attendance-report'),
]