from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from content.models import Content
from django.utils import timezone

class Command(BaseCommand):
    help = "Create initial users and example content"

    def handle(self, *args, **kwargs):

        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser(
                username="admin",
                email="admin@gmail.com",
                password="123"
            )
            self.stdout.write(self.style.SUCCESS("Created superuser: admin"))
        else:
            admin = User.objects.get(username="admin")
            self.stdout.write("Superuser admin already exists")

        if not User.objects.filter(username="staff").exists():
            staff = User.objects.create_user(
                username="author",
                email="author@gmail.com",
                password="123",
                is_staff=True
            )
            self.stdout.write(self.style.SUCCESS("Created author user: author"))
        else:
            staff = User.objects.get(username="author")
            self.stdout.write("Author user already exists")

        if not User.objects.filter(username="reader").exists():
            reader = User.objects.create_user(
                username="reader",
                email="reader@gmail.com",
                password="123"
            )
            self.stdout.write(self.style.SUCCESS("Created reader user: reader"))
        else:
            reader = User.objects.get(username="reader")
            self.stdout.write("Reader user already exists")

        contents = [
            {"title": "First Post", "description": "Content by admin", "author": admin},
            {"title": "Staff Post 1", "description": "Content by staff", "author": staff},
            {"title": "Staff Post 2", "description": "Another content by staff", "author": staff},
            {"title": "Reader Post", "description": "Content by reader", "author": reader},
        ]

        for content_data in contents:
            title = content_data['title']
            if not Content.objects.filter(title=title).exists():
                Content.objects.create(
                    title=title,
                    description=content_data['description'],
                    author=content_data['author'],
                    created_at=timezone.now()
                )
                self.stdout.write(self.style.SUCCESS(f"Created content: {title}"))
            else:
                self.stdout.write(f"Content '{title}' already exists")