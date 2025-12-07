from django.urls import path
from .views import UserPermissionView

urlpatterns = [
    path("me/", UserPermissionView.as_view(), name="my-permissions"),
]