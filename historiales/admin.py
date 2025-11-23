from django.contrib import admin
from .models import HistorialClinico, ArchivoHistorial, CertificadoVacunacion

class ArchivoInline(admin.TabularInline):
    model = ArchivoHistorial
    extra = 0

@admin.register(HistorialClinico)
class HistorialClinicoAdmin(admin.ModelAdmin):
    list_display = ('fecha_consulta', 'mascota', 'veterinario', 'cita')
    list_filter = ('fecha_consulta',)
    search_fields = ('mascota__nombre',)
    inlines = [ArchivoInline]

@admin.register(CertificadoVacunacion)
class CertificadoVacunacionAdmin(admin.ModelAdmin):
    list_display = ('numero_certificado', 'mascota', 'veterinario', 'fecha_emision')
