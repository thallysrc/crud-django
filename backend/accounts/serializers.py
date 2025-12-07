from rest_framework import serializers
from django.contrib.auth.models import Permission

class UserPermissionSerializer(serializers.Serializer):
    username = serializers.CharField()
    groups = serializers.ListField(child=serializers.CharField())
    permissions = serializers.ListField(child=serializers.CharField())