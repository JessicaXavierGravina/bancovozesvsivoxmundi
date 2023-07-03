from django.contrib import admin
from .models import Dubladore, Usuario
from django.contrib.auth.admin import UserAdmin

# Register your models here.

campos = list(UserAdmin.fieldsets)
campos.append(
    ('Historico', {'fields': ('dubladores_vistos',)})
)
UserAdmin.fieldsets = tuple(campos)


admin.site.register(Dubladore)
admin.site.register(Usuario, UserAdmin)
