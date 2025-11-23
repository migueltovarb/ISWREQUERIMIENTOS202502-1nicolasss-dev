"""
Modelos para la gestión de mascotas.

Este módulo contiene los modelos Mascota y TransferenciaMascota
para gestionar la información de las mascotas y su historial de transferencias.
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Mascota(models.Model):
    """
    Modelo de Mascota.
    
    Almacena la información de las mascotas atendidas en la veterinaria.
    """
    
    # Opciones de especie
    ESPECIE_CHOICES = [
        ('PERRO', 'Perro'),
        ('GATO', 'Gato'),
        ('AVE', 'Ave'),
        ('ROEDOR', 'Roedor'),
        ('REPTIL', 'Reptil'),
        ('OTRO', 'Otro'),
    ]
    
    # Opciones de sexo
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]
    
    propietario = models.ForeignKey(
        'propietarios.Propietario',
        on_delete=models.PROTECT,
        related_name='mascotas',
        verbose_name='Propietario',
        help_text='Propietario actual de la mascota'
    )
    
    # Información básica (HU-008)
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre',
        help_text='Nombre de la mascota (2-50 caracteres)'
    )
    
    especie = models.CharField(
        max_length=10,
        choices=ESPECIE_CHOICES,
        verbose_name='Especie',
        help_text='Especie de la mascota'
    )
    
    raza = models.CharField(
        max_length=50,
        verbose_name='Raza',
        help_text='Raza de la mascota'
    )
    
    edad = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Edad',
        help_text='Edad de la mascota en años'
    )
    
    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)],
        verbose_name='Peso',
        help_text='Peso de la mascota en kilogramos (opcional)'
    )
    
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        blank=True,
        verbose_name='Sexo',
        help_text='Sexo de la mascota (opcional)'
    )
    
    observaciones = models.TextField(
        max_length=300,
        blank=True,
        verbose_name='Observaciones',
        help_text='Observaciones adicionales (máx 300 caracteres)'
    )
    
    foto = models.ImageField(
        upload_to='mascotas/',
        null=True,
        blank=True,
        verbose_name='Foto',
        help_text='Foto de la mascota'
    )
    
    # Estado
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si la mascota está activa (no transferida ni fallecida)'
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
    
    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['propietario', 'nombre']),
            models.Index(fields=['especie']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.get_especie_display()}) - {self.propietario.nombre}"
    
    def clean(self):
        """
        Validaciones personalizadas del modelo.
        
        Valida:
        - Longitud del nombre (2-50 caracteres)
        - Edad >= 0
        - Peso > 0 si se proporciona
        - Observaciones <= 300 caracteres
        """
        super().clean()
        
        # Validar longitud del nombre
        if len(self.nombre) < 2:
            raise ValidationError({
                'nombre': 'El nombre debe tener al menos 2 caracteres'
            })
        
        # Validar observaciones
        if self.observaciones and len(self.observaciones) > 300:
            raise ValidationError({
                'observaciones': 'Las observaciones no pueden exceder 300 caracteres'
            })
    
    def edad_texto(self):
        """
        Retorna la edad en formato legible.
        
        Returns:
            str: Edad formateada (ej: "2 años", "1 año")
        """
        if self.edad == 1:
            return "1 año"
        return f"{self.edad} años"


class TransferenciaMascota(models.Model):
    """
    Modelo de Transferencia de Mascota (HU-010).
    
    Registra el historial de transferencias de propiedad de mascotas.
    """
    
    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='transferencias',
        verbose_name='Mascota',
        help_text='Mascota transferida'
    )
    
    propietario_anterior = models.ForeignKey(
        'propietarios.Propietario',
        on_delete=models.PROTECT,
        related_name='transferencias_salientes',
        verbose_name='Propietario anterior',
        help_text='Propietario que transfiere la mascota'
    )
    
    propietario_nuevo = models.ForeignKey(
        'propietarios.Propietario',
        on_delete=models.PROTECT,
        related_name='transferencias_entrantes',
        verbose_name='Propietario nuevo',
        help_text='Propietario que recibe la mascota'
    )
    
    fecha_transferencia = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de transferencia'
    )
    
    usuario_responsable = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        verbose_name='Usuario responsable',
        help_text='Usuario que realizó la transferencia'
    )
    
    motivo = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Motivo',
        help_text='Motivo de la transferencia (opcional)'
    )
    
    class Meta:
        verbose_name = 'Transferencia de mascota'
        verbose_name_plural = 'Transferencias de mascotas'
        ordering = ['-fecha_transferencia']
    
    def __str__(self):
        return f"{self.mascota.nombre}: {self.propietario_anterior.nombre} → {self.propietario_nuevo.nombre}"
