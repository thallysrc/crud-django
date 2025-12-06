from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet
from .models import Content
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