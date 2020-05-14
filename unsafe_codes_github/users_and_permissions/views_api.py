from .models import AdvancedUser
from .serializers import AdvancedUserSerializer
from rest_framework import viewsets


class AdvancedUserViewSet(viewsets.ModelViewSet):
    queryset = AdvancedUser.objects.all()
    serializer_class = AdvancedUserSerializer

