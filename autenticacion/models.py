"""
Modelos de autenticación para el sistema MyDOG.

Este módulo contiene el modelo de Usuario personalizado que extiende
AbstractUser de Django para incluir roles específicos del sistema.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado del sistema MyDOG.
    
    Extiende AbstractUser de Django para agregar:
    - Roles específicos del sistema veterinario
    - Control de estado activo/inactivo
    - Control de intentos fallidos de login
    - Bloqueo temporal por seguridad
    """
    
    # Definición de roles del sistema (HU-004)
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('VETERINARIO', 'Veterinario'),
        ('ADMINISTRATIVO', 'Personal Administrativo'),
        ('PROPIETARIO', 'Propietario'),
    ]
    
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        verbose_name='Rol',
        help_text='Rol del usuario en el sistema'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el usuario puede acceder al sistema'
    )
    
    # Control de seguridad (HU-001: Bloqueo después de 5 intentos)
    intentos_fallidos = models.IntegerField(
        default=0,
        verbose_name='Intentos fallidos',
        help_text='Número de intentos fallidos de login consecutivos'
    )
    
    bloqueado_hasta = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Bloqueado hasta',
        help_text='Fecha y hora hasta la cual el usuario está bloqueado'
    )
    
    # Campos adicionales
    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        null=True,
        blank=True,
        verbose_name='Foto de perfil'
    )
    
    telefono = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Teléfono'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificación'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"
    
    def esta_bloqueado(self):
        """
        Verifica si el usuario está actualmente bloqueado.
        
        Returns:
            bool: True si está bloqueado, False en caso contrario
        """
        if self.bloqueado_hasta is None:
            return False
        return timezone.now() < self.bloqueado_hasta
    
    def bloquear_temporalmente(self, minutos=15):
        """
        Bloquea el usuario temporalmente por seguridad.
        
        Args:
            minutos (int): Número de minutos de bloqueo (default: 15)
        """
        from datetime import timedelta
        self.bloqueado_hasta = timezone.now() + timedelta(minutes=minutos)
        self.save()
    
    def desbloquear(self):
        """Desbloquea el usuario y reinicia el contador de intentos fallidos."""
        self.bloqueado_hasta = None
        self.intentos_fallidos = 0
        self.save()
    
    def registrar_intento_fallido(self):
        """
        Registra un intento fallido de login.
        
        Si alcanza 5 intentos, bloquea el usuario por 15 minutos (HU-001).
        """
        self.intentos_fallidos += 1
        if self.intentos_fallidos >= 5:
            self.bloquear_temporalmente(minutos=15)
        self.save()
    
    def registrar_login_exitoso(self):
        """Reinicia el contador de intentos fallidos tras login exitoso."""
        self.intentos_fallidos = 0
        self.bloqueado_hasta = None
        self.save()
    
    def es_admin(self):
        """Verifica si el usuario es administrador."""
        return self.rol == 'ADMIN'
    
    def es_veterinario(self):
        """Verifica si el usuario es veterinario."""
        return self.rol == 'VETERINARIO'
    
    def es_administrativo(self):
        """Verifica si el usuario es personal administrativo."""
        return self.rol == 'ADMINISTRATIVO'
    
    def es_propietario(self):
        """Verifica si el usuario es propietario."""
        return self.rol == 'PROPIETARIO'
