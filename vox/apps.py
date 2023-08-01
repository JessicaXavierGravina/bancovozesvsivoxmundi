from django.apps import AppConfig

class VoxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vox'

    def ready(self):
        from .models import Usuario
        import os

        email = os.getenv("EMAIL_ADMIN")
        senha = os.getenv("SENHA_ADMIN")
        username = "admin"

        try:
            admin_user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            admin_user = None

        if not admin_user:
            usuarios = Usuario.objects.filter(email=email)
            if not usuarios:
                Usuario.objects.create_superuser(username=username, email=email, password=senha, is_active=True, is_superuser=True)
