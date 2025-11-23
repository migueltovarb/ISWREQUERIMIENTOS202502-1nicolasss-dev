from django.contrib import admin
from .models import Reporte

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'formato', 'fecha_generacion', 'generado_por')
    list_filter = ('tipo', 'formato')
