from django.urls import path
from .views import (
    SermonSeriesListView, SermonListView, SermonDetailView,
    SermonListenView, SermonDownloadView
)

urlpatterns = [
    path('series/', SermonSeriesListView.as_view(), name='series-list'),
    path('', SermonListView.as_view(), name='sermon-list'),
    path('<int:pk>/', SermonDetailView.as_view(), name='sermon-detail'),
    path('<int:pk>/listen/', SermonListenView.as_view(), name='sermon-listen'),
    path('<int:pk>/download/', SermonDownloadView.as_view(), name='sermon-download'),
]