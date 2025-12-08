from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from content.models import Content
from django.utils import timezone


class Command(BaseCommand):
    help = "Create initial users, groups, permissions, and example content"

    def create_user_with_group(self, group=None, **kwargs):
        """
        Creates (or fetches) a user and assigns them to the given group.
        Expected kwargs: username, email, password
        """

        password = kwargs.pop("password")
        username = kwargs["username"]

        user, created = User.objects.get_or_create(username=username, defaults=kwargs)

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))
        else:
            self.stdout.write(f"User '{username}' already exists")

        if group:
            user.groups.add(group)

        return user

    def handle(self, *args, **kwargs):

        # -----------------------------------------------------
        # Groups
        # -----------------------------------------------------
        admin_group, created = Group.objects.get_or_create(name="admin")
        author_group, created = Group.objects.get_or_create(name="author")

        # -----------------------------------------------------
        # Permissions for Content model
        # -----------------------------------------------------
        content_type = ContentType.objects.get_for_model(Content)
        permissions = Permission.objects.filter(content_type=content_type)

        admin_group.permissions.set(permissions)
        author_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Permissions assigned to groups"))

        # -----------------------------------------------------
        # Users
        # -----------------------------------------------------

        # Admin superuser
        admin, created = User.objects.get_or_create(username="admin")
        if created:
            admin.email = "admin@gmail.com"
            admin.set_password("123")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            self.stdout.write(self.style.SUCCESS("Created superuser: admin"))
        else:
            self.stdout.write("Superuser admin already exists")
        admin.groups.add(admin_group)

        # Author user
        author = self.create_user_with_group(
            group=author_group,
            username="autor",
            email="autor@gmail.com",
            password="123",
        )

        # Reader user (no group)
        reader = self.create_user_with_group(
            username="leitor",
            email="leitor@gmail.com",
            password="123",
        )

        # -----------------------------------------------------
        # Content examples
        # -----------------------------------------------------
        sample_data = [
            (
                "10 Dicas Simples para Melhorar Sua Saúde Hoje",
                "Uma lista prática criada pelo admin com hábitos fáceis para melhorar o bem-estar físico e mental.",
                admin
            ),
            (
                "Como Criar uma Rotina de Exercícios Sustentável",
                "O autor compartilha estratégias realistas para manter uma rotina de treinos sem desistir após a primeira semana.",
                author
            ),
            (
                "Alimentação Inteligente: Pequenas Mudanças, Grandes Resultados",
                "Um guia do autor mostrando como ajustes simples na dieta podem gerar melhorias significativas na saúde.",
                author
            ),
        ]

        for title, desc, author in sample_data:
            if not Content.objects.filter(title=title).exists():
                Content.objects.create(
                    title=title,
                    description=desc,
                    author=author,
                    created_at=timezone.now(),
                )
                self.stdout.write(self.style.SUCCESS(f"Created content: {title}"))
            else:
                self.stdout.write(f"Content '{title}' already exists")
