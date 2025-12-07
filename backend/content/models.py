from django.contrib.auth.models import User
from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contents")

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="favorited_by_relation")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content")

    def __str__(self):
        return f"{self.user.username} -> {self.content.title}"