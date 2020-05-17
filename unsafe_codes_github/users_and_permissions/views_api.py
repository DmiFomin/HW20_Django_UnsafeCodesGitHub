from .models import AdvancedUser
from .serializers import AdvancedUserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser


class AdvancedUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = AdvancedUser.objects.all()
    serializer_class = AdvancedUserSerializer

