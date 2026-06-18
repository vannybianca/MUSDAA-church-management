from django.urls import path
from .views import PrayerRequestListView, PrayerDetailView, PrayView, MyPrayersView

urlpatterns = [
    path('', PrayerRequestListView.as_view(), name='prayer-list'),
    path('<int:pk>/', PrayerDetailView.as_view(), name='prayer-detail'),
    path('pray/', PrayView.as_view(), name='pray'),
    path('my-prayers/', MyPrayersView.as_view(), name='my-prayers'),
]