from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from .models import Content
from .serializers import ContentSerializer


class ContentViewSet(ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = (DjangoModelPermissions,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)