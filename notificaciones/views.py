from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notificacion

@login_required
def lista_notificaciones(request):
    """Listar notificaciones del usuario actual."""
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_envio')
    
    # Marcar como leídas al ver la lista (simplificado)
    notificaciones.filter(leida=False).update(leida=True)
    
    return render(request, 'notificaciones/lista.html', {'notificaciones': notificaciones})

def crear_notificacion(usuario, tipo, asunto, mensaje, cita=None):
    """
    Función utilitaria para crear notificaciones.
    Puede ser llamada desde otras apps (ej: al agendar cita).
    """
    try:
        Notificacion.objects.create(
            usuario=usuario,
            tipo=tipo,
            asunto=asunto,
            mensaje=mensaje,
            cita=cita
        )
        return True
    except Exception:
        return False
