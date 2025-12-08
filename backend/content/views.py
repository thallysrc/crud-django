from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
    pagination_class = ContentPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        my_content = self.request.query_params.get('my_content')

        if my_content == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)

        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class FavoriteContentViewSet(ModelViewSet):
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Content.objects.filter(favorited_by_relation__user=self.request.user).distinct()

    @action(detail=False, methods=['post'], url_path='favorite')
    def favorite(self, request):
        content_id = request.data.get("content_id")
        if not content_id:
            return Response({"error": "content_id is required"}, status=400)

        content = get_object_or_404(Content, pk=content_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, content=content)

        if created:
            return Response({"message": "Content favorited"}, status=201)
        return Response({"message": "Content already favorited"}, status=200)

    @action(detail=False, methods=['post'], url_path='unfavorite')
    def unfavorite(self, request):
        content_id = request.data.get("content_id")
        if not content_id:
            return Response({"error": "content_id is required"}, status=400)

        content = get_object_or_404(Content, pk=content_id)
        favorite = Favorite.objects.filter(user=request.user, content=content)

        if favorite.exists():
            favorite.delete()
            return Response({"message": "Content unfavorited"}, status=200)
        return Response({"message": "Content was not favorited"}, status=400)