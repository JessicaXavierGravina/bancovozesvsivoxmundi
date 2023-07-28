import django.contrib
from .models import Dubladore, Usuario
from django.contrib.auth.admin import UserAdmin

# Register your models here.

campos = list(UserAdmin.fieldsets)
campos.append(
    ('Historico', {'fields': ('dubladores_vistos',)})
)
UserAdmin.fieldsets = tuple(campos)


django.contrib.admin.site.register(Dubladore)
django.contrib.admin.site.register(Usuario, UserAdmin)
