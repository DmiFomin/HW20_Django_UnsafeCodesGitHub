from .models import Settings, Statuses, Languages, Unsafe_codes
from .serializers import SettingsSerializer, StatusesSerializer, LanguagesSerializer, UnsafeCodesSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .permissions import ReadOnly


class SettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Settings.objects.all().select_related('create_user')
    serializer_class = SettingsSerializer


class StatusesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Statuses.objects.all().select_related('create_user')
    serializer_class = StatusesSerializer


class LanguagesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Languages.objects.all().select_related('create_user')
    serializer_class = LanguagesSerializer


class UnsafeCodesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Unsafe_codes.objects.all().select_related('language', 'status', 'create_user')
    serializer_class = UnsafeCodesSerializer