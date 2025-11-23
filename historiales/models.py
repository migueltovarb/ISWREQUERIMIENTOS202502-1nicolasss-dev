"""
Modelos para la gestión de historiales clínicos.

Este módulo contiene los modelos para registrar y gestionar
historiales clínicos de las mascotas.
"""

from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator
import uuid


class HistorialClinico(models.Model):
    """
    Modelo de Historial Clínico (HU-018, HU-019).
    
    Registra diagnósticos, tratamientos y evolución de las mascotas.
    """
    
    mascota = models.ForeignKey(
        'mascotas.Mascota',
        on_delete=models.PROTECT,
        related_name='historiales',
        verbose_name='Mascota'
    )
    
    cita = models.ForeignKey(
        'citas.Cita',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historiales',
        verbose_name='Cita asociada'
    )
    
    veterinario = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        limit_choices_to={'rol': 'VETERINARIO'},
        related_name='historiales_registrados',
        verbose_name='Veterinario responsable'
    )
    
    fecha_consulta = models.DateField(
        verbose_name='Fecha de consulta'
    )
    
    # Información médica
    diagnostico = models.TextField(
        verbose_name='Diagnóstico',
        help_text='Diagnóstico realizado por el veterinario'
    )
    
    tratamiento = models.TextField(
        verbose_name='Tratamiento',
        help_text='Tratamiento prescrito'
    )
    
    vacunas = models.TextField(
        blank=True,
        verbose_name='Vacunas aplicadas',
        help_text='Vacunas administradas durante la consulta'
    )
    
    procedimientos = models.TextField(
        blank=True,
        verbose_name='Procedimientos realizados',
        help_text='Procedimientos médicos realizados'
    )
    
    evolucion = models.TextField(
        verbose_name='Evolución',
        help_text='Estado y evolución del paciente'
    )
    
    peso_actual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)],
        verbose_name='Peso actual (kg)',
        help_text='Peso registrado durante la consulta'
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
        verbose_name = 'Historial clínico'
        verbose_name_plural = 'Historiales clínicos'
        ordering = ['-fecha_consulta']
    
    def __str__(self):
        return f"{self.mascota.nombre} - {self.fecha_consulta} - Dr. {self.veterinario.get_full_name()}"


class ArchivoHistorial(models.Model):
    """
    Modelo de Archivo del Historial Clínico (HU-020).
    
    Almacena archivos adjuntos (imágenes, PDFs) del historial.
    """
    
    historial = models.ForeignKey(
        HistorialClinico,
        on_delete=models.CASCADE,
        related_name='archivos',
        verbose_name='Historial clínico'
    )
    
    archivo = models.FileField(
        upload_to='historiales/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name='Archivo',
        help_text='Archivo adjunto (PDF, JPG, PNG - máx 10MB)'
    )
    
    tipo = models.CharField(
        max_length=10,
        verbose_name='Tipo de archivo'
    )
    
    descripcion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Descripción'
    )
    
    fecha_carga = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de carga'
    )
    
    usuario = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        verbose_name='Usuario que cargó el archivo'
    )
    
    class Meta:
        verbose_name = 'Archivo de historial'
        verbose_name_plural = 'Archivos de historiales'
        ordering = ['-fecha_carga']
    
    def __str__(self):
        return f"{self.historial.mascota.nombre} - {self.tipo} - {self.fecha_carga.strftime('%d/%m/%Y')}"


class CertificadoVacunacion(models.Model):
    """
    Modelo de Certificado de Vacunación (HU-035).
    
    Genera y almacena certificados de vacunación en PDF.
    """
    
    mascota = models.ForeignKey(
        'mascotas.Mascota',
        on_delete=models.PROTECT,
        related_name='certificados_vacunacion',
        verbose_name='Mascota'
    )
    
    numero_certificado = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Número de certificado',
        help_text='Número único del certificado'
    )
    
    veterinario = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        limit_choices_to={'rol': 'VETERINARIO'},
        verbose_name='Veterinario emisor'
    )
    
    fecha_emision = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de emisión'
    )
    
    pdf = models.FileField(
        upload_to='certificados/%Y/%m/',
        verbose_name='Certificado PDF'
    )
    
    # Mantener registro de vacunas incluidas
    vacunas_incluidas = models.TextField(
        verbose_name='Vacunas incluidas',
        help_text='Lista de vacunas incluidas en el certificado'
    )
    
    class Meta:
        verbose_name = 'Certificado de vacunación'
        verbose_name_plural = 'Certificados de vacunación'
        ordering = ['-fecha_emision']
    
    def __str__(self):
        return f"Certificado {self.numero_certificado} - {self.mascota.nombre}"
    
    def save(self, *args, **kwargs):
        """Genera número único si no existe."""
        if not self.numero_certificado:
            self.numero_certificado = f"CERT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
