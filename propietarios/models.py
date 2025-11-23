"""
Modelos para la gestión de propietarios de mascotas.

Este módulo contiene el modelo Propietario que almacena la información
de los dueños de mascotas que utilizan el sistema veterinario.
"""

from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


class Propietario(models.Model):
    """
    Modelo de Propietario de mascotas.
    
    Almacena la información personal y de contacto de los dueños de mascotas.
    Relacionado con el modelo Usuario através de OneToOne.
    """
    
    usuario = models.OneToOneField(
        'autenticacion.Usuario',
        on_delete=models.CASCADE,
        related_name='propietario',
        verbose_name='Usuario',
        help_text='Usuario del sistema asociado al propietario'
    )
    
    # Información personal (HU-005)
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre completo',
        help_text='Nombre completo del propietario (3-100 caracteres)'
    )
    
    documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Documento de identidad',
        help_text='Número de documento único del propietario'
    )
    
    # Información de contacto
    telefono_validator = RegexValidator(
        regex=r'^\d{7,15}$',
        message='El teléfono debe contener entre 7 y 15 dígitos numéricos'
    )
    
    telefono = models.CharField(
        max_length=15,
        validators=[telefono_validator],
        verbose_name='Teléfono',
        help_text='Teléfono de contacto (7-15 dígitos)'
    )
    
    correo = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name='Correo electrónico',
        help_text='Correo electrónico único del propietario'
    )
    
    direccion = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='Dirección',
        help_text='Dirección de residencia (opcional, máx 200 caracteres)'
    )
    
    # Campos de auditoría
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificación'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el propietario está activo en el sistema'
    )
    
    class Meta:
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['documento']),
            models.Index(fields=['correo']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.documento})"
    
    def clean(self):
        """
        Validaciones personalizadas del modelo.
        
        Valida:
        - Longitud del nombre (3-100 caracteres)
        - Formato del teléfono
        - Unicidad de correo y documento
        """
        super().clean()
        
        # Validar longitud del nombre
        if len(self.nombre) < 3:
            raise ValidationError({
                'nombre': 'El nombre debe tener al menos 3 caracteres'
            })
        
        if len(self.nombre) > 100:
            raise ValidationError({
                'nombre': 'El nombre no puede exceder 100 caracteres'
            })
    
    def numero_mascotas(self):
        """
        Retorna el número total de mascotas del propietario.
        
        Returns:
            int: Número de mascotas registradas
        """
        return self.mascotas.count()
    
    def mascotas_activas(self):
        """
        Retorna las mascotas activas del propietario.
        
        Returns:
            QuerySet: Mascotas que no han sido transferidas
        """
        return self.mascotas.filter(activo=True)
