"""
Modelos para la gestión de citas veterinarias.

Este módulo contiene los modelos Cita y ListaEspera para gestionar
el agendamiento de citas y la lista de espera de pacientes.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta, time as dt_time


class Cita(models.Model):
    """
    Modelo de Cita Veterinaria (HU-011 a HU-015, HU-029 a HU-032).
    
    Gestiona las citas programadas entre propietarios, mascotas,
    servicios y veterinarios.
    """
    
    # Opciones de estado
    ESTADO_CHOICES = [
        ('PROGRAMADA', 'Programada'),
        ('CONFIRMADA', 'Confirmada'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
        ('INASISTENCIA', 'Inasistencia'),
    ]
    
    # Relaciones
    propietario = models.ForeignKey(
        'propietarios.Propietario',
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Propietario',
        help_text='Propietario de la mascota'
    )
    
    mascota = models.ForeignKey(
        'mascotas.Mascota',
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Mascota',
        help_text='Mascota a atender'
    )
    
    servicio = models.ForeignKey(
        'servicios.Servicio',
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Servicio',
        help_text='Servicio veterinario solicitado'
    )
    
    veterinario = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        limit_choices_to={'rol': 'VETERINARIO'},
        related_name='citas_asignadas',
        verbose_name='Veterinario',
        help_text='Veterinario asignado'
    )
    
    # Fecha y hora
    fecha = models.DateField(
        verbose_name='Fecha',
        help_text='Fecha de la cita'
    )
    
    hora = models.TimeField(
        verbose_name='Hora',
        help_text='Hora de inicio de la cita'
    )
    
    # Estado y tipo
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='PROGRAMADA',
        verbose_name='Estado'
    )
    
    es_emergencia = models.BooleanField(
        default=False,
        verbose_name='Es emergencia',
        help_text='Indica si es una cita de emergencia (sin restricciones de horario)'
    )
    
    # Información adicional
    observaciones = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Observaciones',
        help_text='Observaciones o motivo de la cita'
    )
    
    motivo_cancelacion = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Motivo de cancelación',
        help_text='Motivo por el cual se canceló la cita'
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
    
    usuario_creador = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        related_name='citas_creadas',
        verbose_name='Usuario creador',
        help_text='Usuario que creó la cita'
    )
    
    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha', '-hora']
        indexes = [
            models.Index(fields=['fecha', 'hora']),
            models.Index(fields=['veterinario', 'fecha']),
            models.Index(fields=['estado']),
        ]
        unique_together = [['veterinario', 'fecha', 'hora']]  # No permitir citas duplicadas
    
    def __str__(self):
        return f"{self.mascota.nombre} - {self.servicio.get_nombre_display()} ({self.fecha} {self.hora})"
    
    def clean(self):
        """
        Validaciones personalizadas del modelo.
        
        Valida:
        - Horario laboral (lunes a sábado, 8:00-18:00) si no es emergencia
        - Disponibilidad del veterinario
        - Mascota pertenece al propietario
        """
        super().clean()
        
        # Validar que la mascota pertenece al propietario
        if hasattr(self, 'mascota') and hasattr(self, 'propietario'):
            if self.mascota.propietario != self.propietario:
                raise ValidationError({
                    'mascota': f'La mascota {self.mascota.nombre} no pertenece al propietario seleccionado'
                })
        
        # Validar horario laboral si no es emergencia
        if not self.es_emergencia:
            # Validar día laboral (lunes=0 a sábado=5)
            if self.fecha.weekday() == 6:  # Domingo
                raise ValidationError({
                    'fecha': 'No se atiende los domingos. Horario: Lunes a Sábado'
                })
            
            # Validar horario (8:00 - 18:00)
            hora_inicio = dt_time(8, 0)
            hora_fin = dt_time(18, 0)
            
            if not (hora_inicio <= self.hora <= hora_fin):
                raise ValidationError({
                    'hora': 'Horario laboral: 8:00 AM - 6:00 PM'
                })
    
    def puede_cancelar(self, usuario):
        """
        Valida si una cita puede ser cancelada (HU-015).
        
        Restricciones:
        - Mínimo 6 horas de anticipación
        - Estado debe ser PROGRAMADA o CONFIRMADA
        - Administradores pueden anular la regla de 6h
        
        Args:
            usuario: Usuario que intenta cancelar
            
        Returns:
            tuple: (puede_cancelar: bool, mensaje: str)
        """
        # Validar estado
        if self.estado not in ['PROGRAMADA', 'CONFIRMADA']:
            return False, 'La cita ya no puede ser cancelada'
        
        # Administradores pueden anular la regla
        if usuario.es_admin():
            return True, ''
        
        # Calcular tiempo de anticipación
        fecha_hora_cita = datetime.combine(self.fecha, self.hora)
        ahora = timezone.now()
        diferencia = fecha_hora_cita - ahora.replace(tzinfo=None)
        
        # Validar 6 horas de anticipación
        if diferencia < timedelta(hours=6):
            return False, 'La cancelación requiere al menos 6 horas de anticipación'
        
        return True, ''
    
    def puede_reprogramar(self, usuario):
        """
        Valida si una cita puede ser reprogramada (HU-014).
        
        Restricciones:
        - Mínimo 12 horas de anticipación
        - Estado debe ser PROGRAMADA o CONFIRMADA
        - Administradores pueden anular la regla de 12h
        
        Args:
            usuario: Usuario que intenta reprogramar
            
        Returns:
            tuple: (puede_reprogramar: bool, mensaje: str)
        """
        # Validar estado
        if self.estado not in ['PROGRAMADA', 'CONFIRMADA']:
            return False, 'La cita ya no puede ser reprogramada'
        
        # Administradores pueden anular la regla
        if usuario.es_admin():
            return True, ''
        
        # Calcular tiempo de anticipación
        fecha_hora_cita = datetime.combine(self.fecha, self.hora)
        ahora = timezone.now()
        diferencia = fecha_hora_cita - ahora.replace(tzinfo=None)
        
        # Validar 12 horas de anticipación
        if diferencia < timedelta(hours=12):
            return False, 'La reprogramación requiere al menos 12 horas de anticipación'
        
        return True, ''


class ListaEspera(models.Model):
    """
    Modelo de Lista de Espera (HU-032).
    
    Gestiona pacientes en lista de espera cuando no hay disponibilidad inmediata.
    """
    
    # Niveles de prioridad según tipo de servicio
    PRIORIDAD_CHOICES = [
        (1, 'Emergencias'),
        (2, 'Cirugías'),
        (3, 'Servicios médicos'),
        (4, 'Peluquería'),
        (5, 'Venta de productos'),
    ]
    
    paciente = models.ForeignKey(
        'mascotas.Mascota',
        on_delete=models.CASCADE,
        related_name='lista_espera',
        verbose_name='Paciente',
        help_text='Mascota en lista de espera'
    )
    
    servicio = models.ForeignKey(
        'servicios.Servicio',
        on_delete=models.CASCADE,
        verbose_name='Servicio',
        help_text='Servicio solicitado'
    )
    
    prioridad = models.IntegerField(
        choices=PRIORIDAD_CHOICES,
        verbose_name='Prioridad',
        help_text='Nivel de prioridad en la lista de espera'
    )
    
    fecha_solicitud = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de solicitud'
    )
    
    observaciones = models.TextField(
        max_length=300,
        blank=True,
        verbose_name='Observaciones'
    )
    
    atendido = models.BooleanField(
        default=False,
        verbose_name='Atendido',
        help_text='Indica si ya se le asignó una cita'
    )
    
    class Meta:
        verbose_name = 'Lista de espera'
        verbose_name_plural = 'Listas de espera'
        ordering = ['prioridad', 'fecha_solicitud']
    
    def __str__(self):
        return f"{self.paciente.nombre} - {self.servicio.get_nombre_display()} (Prioridad: {self.get_prioridad_display()})"
