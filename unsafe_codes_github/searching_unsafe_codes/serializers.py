from .models import Settings, Statuses, Languages, Unsafe_codes
from rest_framework import serializers
from users_and_permissions.serializers import AdvancedUserSerializer


class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    create_user = AdvancedUserSerializer()
    class Meta:
        model = Settings
        exclude = ['path_to_token']


class StatusesSerializer(serializers.HyperlinkedModelSerializer):
    create_user = AdvancedUserSerializer()
    class Meta:
        model = Statuses
        fields = '__all__'


class LanguagesSerializer(serializers.HyperlinkedModelSerializer):
    create_user = AdvancedUserSerializer()
    class Meta:
        model = Languages
        fields = '__all__'


class UnsafeCodesSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguagesSerializer()
    status = StatusesSerializer()
    create_user = AdvancedUserSerializer()
    class Meta:
        model = Unsafe_codes
        fields = '__all__'