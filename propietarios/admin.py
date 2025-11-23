from django.contrib import admin
from .models import Propietario

@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'telefono', 'correo', 'usuario')
    search_fields = ('nombre', 'documento', 'correo')
