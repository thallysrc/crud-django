from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Content, Favorite
from .permissions import ContentPermission
from .serializers import ContentSerializer


class ContentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class ContentViewSet(ModelViewSet):
    queryset = Content.objects.all().order_by('-created_at')
    serializer_class = ContentSerializer
    permission_classes = (ContentPermission,)
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = ContentPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        my_content = self.request.query_params.get('my_content')

        if my_content == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
