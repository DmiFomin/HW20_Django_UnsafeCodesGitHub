from .models import Settings, Statuses, Languages, Unsafe_codes
from .serializers import SettingsSerializer, StatusesSerializer, LanguagesSerializer, UnsafeCodesSerializer
from rest_framework import viewsets


class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


class StatusesViewSet(viewsets.ModelViewSet):
    queryset = Statuses.objects.all()
    serializer_class = StatusesSerializer


class LanguagesViewSet(viewsets.ModelViewSet):
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer


class UnsafeCodesViewSet(viewsets.ModelViewSet):
    queryset = Unsafe_codes.objects.all()
    serializer_class = UnsafeCodesSerializer