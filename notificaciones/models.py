"""
Modelos para el sistema de notificaciones simuladas.

Este módulo contiene los modelos para gestionar preferencias de notificación
y el registro de notificaciones simuladas del sistema.
"""

from django.db import models



class PreferenciaNotificacion(models.Model):
    """
    Modelo de Preferencia de Notificación (HU-017).
    
    Almacena las preferencias de canal y tipos de notificaciones del usuario.
    """
    
    CANAL_CHOICES = [
        ('EMAIL', 'Correo electrónico'),
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
    ]
    
    usuario = models.OneToOneField(
        'autenticacion.Usuario',
        on_delete=models.CASCADE,
        related_name='preferencia_notificacion',
        verbose_name='Usuario'
    )
    
    canal_preferido = models.CharField(
        max_length=10,
        choices=CANAL_CHOICES,
        default='EMAIL',
        verbose_name='Canal preferido',
        help_text='Canal preferido para recibir notificaciones'
    )
    
    # Tipos de notificaciones activadas/desactivadas
    confirmaciones = models.BooleanField(
        default=True,
        verbose_name='Confirmaciones',
        help_text='Recibir confirmaciones de citas agendadas'
    )
    
    recordatorios = models.BooleanField(
        default=True,
        verbose_name='Recordatorios',
        help_text='Recibir recordatorios de citas próximas'
    )
    
    cancelaciones = models.BooleanField(
        default=True,
        verbose_name='Cancelaciones',
        help_text='Recibir notificaciones de cancelaciones'
    )
    
    resultados = models.BooleanField(
        default=True,
        verbose_name='Resultados',
        help_text='Recibir notificaciones de resultados disponibles'
    )
    
    class Meta:
        verbose_name = 'Preferencia de notificación'
        verbose_name_plural = 'Preferencias de notificaciones'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_canal_preferido_display()}"


class Notificacion(models.Model):
    """
    Modelo de Notificación (HU-016).
    
    Registra notificaciones simuladas enviadas a usuarios.
    """
    
    TIPO_CHOICES = [
        ('CONFIRMACION', 'Confirmación'),
        ('RECORDATORIO', 'Recordatorio'),
        ('CANCELACION', 'Cancelación'),
        ('RESULTADO', 'Resultado disponible'),
        ('SISTEMA', 'Notificación del sistema'),
    ]
    
    usuario = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.CASCADE,
        related_name='notificaciones',
        verbose_name='Usuario'
    )

    actor = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notificaciones_emitidas',
        verbose_name='Actor'
    )
    
    tipo = models.CharField(
        max_length=15,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de notificación'
    )
    
    asunto = models.CharField(
        max_length=200,
        verbose_name='Asunto',
        help_text='Título o asunto de la notificación'
    )
    
    mensaje = models.TextField(
        verbose_name='Mensaje',
        help_text='Contenido de la notificación'
    )
    
    leida = models.BooleanField(
        default=False,
        verbose_name='Leída',
        help_text='Indica si la notificación ha sido leída'
    )
    
    canal_enviado = models.CharField(
        max_length=10,
        verbose_name='Canal de envío',
        help_text='Canal por el cual se "envió" la notificación'
    )
    
    fecha_envio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de envío'
    )
    
    fecha_lectura = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de lectura'
    )
    
    simulada = models.BooleanField(
        default=True,
        verbose_name='Simulada',
        help_text='Indica que es una notificación simulada (siempre True)'
    )
    
    # Referencia a cita relacionada (opcional)
    cita = models.ForeignKey(
        'citas.Cita',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notificaciones',
        verbose_name='Cita relacionada'
    )
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_envio']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_tipo_display()} - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"
    
    def marcar_como_leida(self):
        """Marca la notificación como leída."""
        from django.utils import timezone
        if not self.leida:
            self.leida = True
            self.fecha_lectura = timezone.now()
            self.save()


class NotificacionLog(models.Model):
    """Registro de eventos de notificaciones (creación, lectura, envío)."""
    ACCION_CHOICES = [
        ('CREADA', 'Creada'),
        ('LEIDA', 'Leída'),
        ('ENVIADA', 'Enviada'),
    ]

    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE, related_name='logs')
    accion = models.CharField(max_length=10, choices=ACCION_CHOICES)
    usuario = models.ForeignKey('autenticacion.Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    detalles = models.JSONField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Log de notificación'
        verbose_name_plural = 'Logs de notificaciones'
        ordering = ['-fecha']
