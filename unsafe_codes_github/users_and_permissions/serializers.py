from .models import AdvancedUser
from rest_framework import serializers


class AdvancedUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdvancedUser
        fields = ['username']


