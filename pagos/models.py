"""
Modelos para la gestión de pagos y facturación.

Este módulo contiene los modelos para el sistema de pagos simulados
y generación de facturas en PDF.
"""

from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
import uuid


class Pago(models.Model):
    """
    Modelo de Pago (HU-021, HU-023).
    
    Registra pagos simulados con diferentes métodos de pago.
    """
    
    TIPO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('PENDIENTE', 'Pendiente'),
    ]
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
    ]
    
    cita = models.ForeignKey(
        'citas.Cita',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagos',
        verbose_name='Cita asociada'
    )
    
    propietario = models.ForeignKey(
        'propietarios.Propietario',
        on_delete=models.PROTECT,
        related_name='pagos',
        verbose_name='Propietario'
    )
    
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Monto',
        help_text='Monto del pago en pesos colombianos'
    )
    
    tipo_pago = models.CharField(
        max_length=15,
        choices=TIPO_PAGO_CHOICES,
        verbose_name='Tipo de pago'
    )
    
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        verbose_name='Estado del pago'
    )
    
    referencia = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Referencia/Comprobante',
        help_text='Número de referencia o comprobante'
    )
    
    # Solo últimos 4 dígitos de tarjeta por seguridad
    ultimos_4_digitos_validator = RegexValidator(
        regex=r'^\d{4}$',
        message='Debe contener exactamente 4 dígitos'
    )
    
    ultimos_4_digitos = models.CharField(
        max_length=4,
        blank=True,
        validators=[ultimos_4_digitos_validator],
        verbose_name='Últimos 4 dígitos',
        help_text='Últimos 4 dígitos de la tarjeta (solo si es pago con tarjeta)'
    )
    
    fecha_pago = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha del pago'
    )
    
    simulado = models.BooleanField(
        default=True,
        verbose_name='Pago simulado',
        help_text='Indica si es un pago simulado (siempre True en este sistema)'
    )
    
    # Campos de auditoría
    usuario_registro = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        verbose_name='Usuario que registró el pago'
    )
    
    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']
    
    def __str__(self):
        return f"Pago {self.id} - {self.propietario.nombre} - ${self.monto} ({self.get_tipo_pago_display()})"
    
    def marcar_como_completado(self):
        """Marca el pago como completado."""
        self.estado = 'COMPLETADO'
        self.save()


class Factura(models.Model):
    """
    Modelo de Factura (HU-022).
    
    Genera y almacena facturas en PDF para los pagos.
    """
    
    numero_factura = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Número de factura',
        help_text='Número único y consecutivo de la factura'
    )
    
    pago = models.ForeignKey(
        Pago,
        on_delete=models.PROTECT,
        related_name='facturas',
        verbose_name='Pago asociado'
    )
    
    propietario = models.ForeignKey(
        'propietarios.Propietario',
        on_delete=models.PROTECT,
        related_name='facturas',
        verbose_name='Propietario'
    )
    
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Subtotal'
    )
    
    impuestos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='Impuestos'
    )
    
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Total'
    )
    
    pdf = models.FileField(
        upload_to='facturas/%Y/%m/',
        verbose_name='Factura PDF'
    )
    
    fecha_emision = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de emisión'
    )
    
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.propietario.nombre} - ${self.total}"
    
    def save(self, *args, **kwargs):
        """Genera número de factura único si no existe."""
        if not self.numero_factura:
            self.numero_factura = f"FACT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
