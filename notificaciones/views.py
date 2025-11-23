from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notificacion, NotificacionLog
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from autenticacion.decorators import staff_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404

@login_required
@ensure_csrf_cookie
def lista_notificaciones(request):
    """Listar notificaciones del usuario actual."""
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_envio')
    return render(request, 'notificaciones/lista.html', {'notificaciones': notificaciones})

def crear_notificacion(usuario, actor, tipo, asunto, mensaje, cita=None):
    """
    Función utilitaria para crear notificaciones.
    Puede ser llamada desde otras apps (ej: al agendar cita).
    """
    try:
        n = Notificacion.objects.create(
            usuario=usuario,
            actor=actor,
            tipo=tipo,
            asunto=asunto,
            mensaje=mensaje,
            cita=cita,
            canal_enviado=getattr(getattr(usuario, 'preferencia_notificacion', None), 'canal_preferido', 'EMAIL')
        )
        NotificacionLog.objects.create(notificacion=n, accion='CREADA', usuario=actor, detalles={'cita_id': getattr(cita, 'id', None)})
        return True
    except Exception:
        return False


@login_required
@staff_required
def admin_notificaciones(request):
    tipo = request.GET.get('tipo')
    usuario_id = request.GET.get('usuario')
    qs = Notificacion.objects.all()
    if tipo:
        qs = qs.filter(tipo=tipo)
    if usuario_id:
        qs = qs.filter(usuario_id=usuario_id)
    return render(request, 'notificaciones/admin_lista.html', {'notificaciones': qs})


@login_required
@ensure_csrf_cookie
def veterinario_notificaciones(request):
    if request.user.rol != 'VETERINARIO':
        return HttpResponseForbidden()
    qs = Notificacion.objects.filter(usuario=request.user)
    return render(request, 'notificaciones/vet_lista.html', {'notificaciones': qs})


@login_required
@ensure_csrf_cookie
def propietario_notificaciones(request):
    if request.user.rol != 'PROPIETARIO':
        return HttpResponseForbidden()
    qs = Notificacion.objects.filter(usuario=request.user)
    return render(request, 'notificaciones/prop_lista.html', {'notificaciones': qs})


@login_required
def api_mis_notificaciones(request):
    qs = Notificacion.objects.filter(usuario=request.user)
    datos = [{
        'id': n.id,
        'tipo': n.tipo,
        'asunto': n.asunto,
        'mensaje': n.mensaje,
        'leida': n.leida,
        'fecha_envio': n.fecha_envio.isoformat(),
        'cita_id': n.cita_id,
    } for n in qs[:100]]
    return JsonResponse({'unread': qs.filter(leida=False).count(), 'items': datos})


@login_required
def api_marcar_leida(request, pk):
    n = get_object_or_404(Notificacion, pk=pk, usuario=request.user)
    n.marcar_como_leida()
    NotificacionLog.objects.create(notificacion=n, accion='LEIDA', usuario=request.user)
    return JsonResponse({'ok': True})


@login_required
@require_POST
def api_marcar_todas(request):
    qs = Notificacion.objects.filter(usuario=request.user, leida=False)
    total = qs.count()
    for n in qs:
        n.marcar_como_leida()
        NotificacionLog.objects.create(notificacion=n, accion='LEIDA', usuario=request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'marked': total})
    referer = request.META.get('HTTP_REFERER') or '/'
    return redirect(referer)
