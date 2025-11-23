from django.contrib import admin
from .models import Cita, ListaEspera

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora', 'servicio', 'mascota', 'veterinario', 'estado', 'es_emergencia')
    list_filter = ('estado', 'es_emergencia', 'fecha')
    search_fields = ('mascota__nombre', 'propietario__nombre')

@admin.register(ListaEspera)
class ListaEsperaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'servicio', 'fecha_solicitud', 'prioridad', 'atendido')
    list_filter = ('prioridad', 'atendido')
