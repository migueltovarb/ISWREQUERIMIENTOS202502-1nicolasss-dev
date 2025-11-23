from django.contrib import admin
from .models import LogAuditoria, Respaldo

@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'modelo', 'objeto_id')
    list_filter = ('accion', 'modelo')
    readonly_fields = ('fecha', 'usuario', 'accion', 'modelo', 'objeto_id', 'datos_anteriores', 'datos_nuevos', 'ip')

@admin.register(Respaldo)
class RespaldoAdmin(admin.ModelAdmin):
    list_display = ('fecha_respaldo', 'archivo', 'tamano_mb', 'exitoso')
