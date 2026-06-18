from django.urls import path
from .views import EventListView, EventDetailView, RSVPView, EventRSVPListView

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('rsvp/', RSVPView.as_view(), name='rsvp'),
    path('<int:event_id>/rsvps/', EventRSVPListView.as_view(), name='event-rsvps'),
]