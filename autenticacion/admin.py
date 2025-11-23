from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'activo', 'is_staff')
    list_filter = ('rol', 'activo', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('rol', 'telefono', 'foto_perfil', 'activo')}),
        ('Seguridad', {'fields': ('intentos_fallidos', 'bloqueado_hasta')}),
    )
