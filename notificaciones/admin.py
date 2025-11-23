from django.contrib import admin
from .models import Notificacion, PreferenciaNotificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('fecha_envio', 'usuario', 'tipo', 'asunto', 'leida')
    list_filter = ('tipo', 'leida')

@admin.register(PreferenciaNotificacion)
class PreferenciaNotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'canal_preferido', 'recordatorios')
