"""
Modelos para la generación de reportes.

Este módulo contiene el modelo Reporte para gestionar
la generación y almacenamiento de reportes del sistema.
"""

from django.db import models


class Reporte(models.Model):
    """
    Modelo de Reporte (HU-024).
    
    Almacena reportes generados en PDF o Excel.
    """
    
    TIPO_CHOICES = [
        ('CITAS', 'Reporte de citas'),
        ('SERVICIOS', 'Reporte de servicios'),
        ('FINANCIERO', 'Reporte financiero'),
        ('PACIENTES', 'Reporte de pacientes'),
        ('VETERINARIOS', 'Reporte de veterinarios'),
    ]
    
    FORMATO_CHOICES = [
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
    ]
    
    tipo = models.CharField(
        max_length=15,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de reporte'
    )
    
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre del reporte',
        help_text='Nombre descriptivo del reporte generado'
    )
    
    parametros = models.JSONField(
        verbose_name='Parámetros',
        help_text='Parámetros utilizados para generar el reporte'
    )
    
    formato = models.CharField(
        max_length=10,
        choices=FORMATO_CHOICES,
        verbose_name='Formato'
    )
    
    archivo = models.FileField(
        upload_to='reportes/%Y/%m/',
        verbose_name='Archivo del reporte'
    )
    
    generado_por = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        related_name='reportes_generados',
        verbose_name='Generado por'
    )
    
    fecha_generacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de generación'
    )
    
    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-fecha_generacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_formato_display()} - {self.fecha_generacion.strftime('%d/%m/%Y')}"
