from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
from .serializers import UserPermissionSerializer

class UserPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # list of group names
        groups = list(user.groups.values_list("name", flat=True))

        # all permissions: user + group permissions
        permissions = list(
            Permission.objects.filter(
                user=user
            ).values_list("codename", flat=True)
        )

        group_permissions = list(
            Permission.objects.filter(
                group__user=user
            ).values_list("codename", flat=True)
        )

        all_permissions = sorted(set(permissions + group_permissions))

        data = {
            "username": user.username,
            "groups": groups,
            "permissions": all_permissions,
        }

        serializer = UserPermissionSerializer(data)
        return Response(serializer.data)