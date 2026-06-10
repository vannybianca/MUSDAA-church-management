from rest_framework import generics, permissions
from .models import MemberProfile
from .serializers import MemberProfileSerializer

class MemberProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MemberProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = MemberProfile.objects.get_or_create(user=self.request.user)
        return profile