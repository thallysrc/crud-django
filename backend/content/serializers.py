from rest_framework import serializers
from .models import Content, Favorite


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "author")