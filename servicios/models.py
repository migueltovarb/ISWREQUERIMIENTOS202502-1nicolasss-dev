"""
Modelos para la gestión de servicios veterinarios.

Este módulo contiene el modelo Servicio que define los diferentes
tipos de servicios que ofrece la veterinaria.
"""

from django.db import models
from django.core.validators import MinValueValidator


class Servicio(models.Model):
    """
    Modelo de Servicio Veterinario (HU-025, HU-026).
    
    Define los servicios que ofrece la veterinaria: consultas,
    vacunaciones, cirugías, etc.
    """
    
    # Tipos de servicio predefinidos
    TIPO_CHOICES = [
        ('CONSULTA', 'Consulta veterinaria'),
        ('VACUNACION', 'Vacunación'),
        ('DESPARASITACION', 'Desparasitación'),
        ('CIRUGIA', 'Cirugía'),
        ('CONTROL_PESO', 'Control de peso'),
        ('PELUQUERIA', 'Peluquería'),
        ('VENTA_PRODUCTOS', 'Venta de productos'),
        ('OTRO', 'Otro'),
    ]
    
    nombre = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        unique=True,
        verbose_name='Nombre del servicio',
        help_text='Tipo de servicio veterinario'
    )
    
    duracion_minutos = models.PositiveIntegerField(
        validators=[MinValueValidator(15)],
        verbose_name='Duración en minutos',
        help_text='Duración estimada del servicio (mínimo 15 minutos)'
    )
    
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio',
        help_text='Precio del servicio en pesos colombianos'
    )
    
    descripcion = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del servicio (opcional)'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el servicio está disponible para agendamiento'
    )
    
    # Color para el calendario (visual)
    color_calendario = models.CharField(
        max_length=7,
        default='#00736A',
        verbose_name='Color en calendario',
        help_text='Color en formato hexadecimal para mostrar en calendario'
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificación'
    )
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.get_nombre_display()} ({self.duracion_minutos} min)"
    
    def puede_desactivar(self):
        """
        Verifica si el servicio puede ser desactivado.
        
        Un servicio no puede desactivarse si tiene citas futuras programadas.
        
        Returns:
            tuple: (puede_desactivar: bool, mensaje: str)
        """
        from django.utils import timezone
        
        citas_futuras = self.citas.filter(
            fecha__gte=timezone.now().date(),
            estado__in=['PROGRAMADA', 'CONFIRMADA']
        ).count()
        
        if citas_futuras > 0:
            return False, f'No se puede desactivar. Hay {citas_futuras} cita(s) futura(s) con este servicio'
        
        return True, ''
