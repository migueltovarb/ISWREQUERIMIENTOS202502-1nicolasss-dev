from django.contrib import admin
from .models import Mascota, TransferenciaMascota

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'propietario', 'edad', 'activo')
    list_filter = ('especie', 'activo')
    search_fields = ('nombre', 'propietario__nombre')

@admin.register(TransferenciaMascota)
class TransferenciaMascotaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'propietario_anterior', 'propietario_nuevo', 'fecha_transferencia')
    list_filter = ('fecha_transferencia',)
