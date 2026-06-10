from django.urls import path
from .views import MemberProfileDetailView

urlpatterns = [
    path('profile/', MemberProfileDetailView.as_view(), name='member-profile'),
]