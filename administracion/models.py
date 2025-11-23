"""
Modelos para la administración del sistema.

Este módulo contiene los modelos para respaldos automát y logs de auditoría.
"""

from django.db import models


class Respaldo(models.Model):
    """
    Modelo de Respaldo (HU-028).
    
    Registra respaldos automáticos diarios de la base de datos.
    """
    
    archivo = models.FileField(
        upload_to='respaldos/%Y/%m/',
        verbose_name='Archivo de respaldo'
    )
    
    fecha_respaldo = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha del respaldo'
    )
    
    tamano_bytes = models.BigIntegerField(
        verbose_name='Tamaño en bytes'
    )
    
    exitoso = models.BooleanField(
        default=True,
        verbose_name='Exitoso',
        help_text='Indica si el respaldo se completó exitosamente'
    )
    
    mensaje_error = models.TextField(
        blank=True,
        verbose_name='Mensaje de error',
        help_text='Mensaje de error si el respaldo falló'
    )
    
    class Meta:
        verbose_name = 'Respaldo'
        verbose_name_plural = 'Respaldos'
        ordering = ['-fecha_respaldo']
    
    def __str__(self):
        estado = "Exitoso" if self.exitoso else "Fallido"
        return f"Respaldo {self.fecha_respaldo.strftime('%d/%m/%Y %H:%M')} - {estado}"
    
    def tamano_mb(self):
        """Retorna el tamaño del respaldo en MB."""
        return round(self.tamano_bytes / (1024 * 1024), 2)


class LogAuditoria(models.Model):
    """
    Modelo de Log de Auditoría (RNF-006).
    
    Registra todas las acciones críticas del sistema de forma inmutable.
    """
    
    usuario = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        related_name='logs_auditoria',
        verbose_name='Usuario'
    )
    
    accion = models.CharField(
        max_length=50,
        verbose_name='Acción',
        help_text='Tipo de acción realizada (CREAR, MODIFICAR, ELIMINAR, etc.)'
    )
    
    modelo = models.CharField(
        max_length=50,
        verbose_name='Modelo',
        help_text='Nombre del modelo afectado'
    )
    
    objeto_id = models.IntegerField(
        verbose_name='ID del objeto',
        help_text='ID del registro afectado'
    )
    
    datos_anteriores = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Datos anteriores',
        help_text='Estado anterior del registro (para modificaciones)'
    )
    
    datos_nuevos = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Datos nuevos',
        help_text='Nuevo estado del registro'
    )
    
    ip = models.GenericIPAddressField(
        verbose_name='Dirección IP',
        help_text='IP desde la que se realizó la acción'
    )
    
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y hora'
    )
    
    class Meta:
        verbose_name = 'Log de auditoría'
        verbose_name_plural = 'Logs de auditoría'
        ordering = ['-fecha']
        # Índices para consultas rápidas
        indexes = [
            models.Index(fields=['usuario', 'fecha']),
            models.Index(fields=['modelo', 'objeto_id']),
            models.Index(fields=['accion']),
        ]
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.accion} {self.modelo} #{self.objeto_id} - {self.fecha.strftime('%d/%m/%Y %H:%M:%S')}"
