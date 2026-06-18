from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/members/', include('members.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/events/', include('events.urls')),      
    path('api/prayers/', include('prayers.urls')),    
    path('api/sermons/', include('sermons.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)