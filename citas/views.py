from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cita
from .forms import CitaForm
from mascotas.models import Mascota
from datetime import datetime
from autenticacion.decorators import staff_required
from notificaciones.services import crear_evento_cita

@login_required
@staff_required
def calendario_citas(request):
    """Vista principal del calendario de citas (HU-011)."""
    return render(request, 'citas/calendario.html')

@login_required
def api_citas(request):
    """API para obtener citas en formato JSON para FullCalendar."""
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    citas = Cita.objects.filter(
        fecha__range=[start[:10], end[:10]],
        estado__in=['PROGRAMADA', 'CONFIRMADA', 'COMPLETADA']
    )
    
    eventos = []
    for cita in citas:
        color = cita.servicio.color_calendario
        if cita.estado == 'COMPLETADA':
            color = '#808080'  # Gris para completadas
        elif cita.es_emergencia:
            color = '#DC3545'  # Rojo para emergencias
            
        eventos.append({
            'id': cita.id,
            'title': f"{cita.mascota.nombre} - {cita.servicio.nombre}",
            'start': f"{cita.fecha}T{cita.hora}",
            'color': color,
            'extendedProps': {
                'propietario': cita.propietario.nombre,
                'veterinario': cita.veterinario.get_full_name(),
                'estado': cita.get_estado_display()
            }
        })
    
    return JsonResponse(eventos, safe=False)

@login_required
@staff_required
def agendar_cita(request):
    """Vista para agendar una nueva cita (HU-013) - Solo staff."""
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.usuario_creador = request.user
            cita.save()
            crear_evento_cita(
                actor=request.user,
                cita=cita,
                tipo='CONFIRMACION',
                asunto='Nueva cita creada',
                mensaje=f"Se creó la cita #{cita.id} para {cita.fecha} a las {cita.hora}"
            )
            messages.success(request, 'Cita agendada exitosamente.')
            return redirect('citas:calendario')
    else:
        form = CitaForm()
    
    return render(request, 'citas/formulario.html', {'form': form, 'titulo': 'Agendar Cita'})

@login_required
def detalle_cita(request, pk):
    """Vista para ver detalles y gestionar una cita."""
    cita = get_object_or_404(Cita, pk=pk)
    necesita_pago = cita.necesita_pago()
    return render(request, 'citas/detalle.html', {
        'cita': cita,
        'necesita_pago': necesita_pago
    })

@login_required
def cargar_mascotas(request):
    """AJAX para cargar mascotas de un propietario seleccionado."""
    propietario_id = request.GET.get('propietario_id')
    mascotas = Mascota.objects.filter(propietario_id=propietario_id, activo=True).values('id', 'nombre')
    return JsonResponse(list(mascotas), safe=False)

@login_required
def cancelar_cita(request, pk):
    """Cancelar una cita (HU-015)."""
    cita = get_object_or_404(Cita, pk=pk)
    if request.user.rol == 'PROPIETARIO' and cita.propietario.usuario_id != request.user.id:
        messages.error(request, 'No tienes permisos para gestionar esta cita.')
        return redirect('citas:detalle', pk=pk)
    
    puede_cancelar, mensaje = cita.puede_cancelar(request.user)
    
    if request.method == 'POST':
        if puede_cancelar:
            motivo = request.POST.get('motivo', '')
            cita.estado = 'CANCELADA'
            cita.motivo_cancelacion = motivo
            cita.save()
            crear_evento_cita(
                actor=request.user,
                cita=cita,
                tipo='CANCELACION',
                asunto='Cita cancelada',
                mensaje=f'La cita #{cita.id} fue cancelada. Motivo: {motivo}'
            )
            messages.success(request, 'Cita cancelada exitosamente.')
            return redirect('citas:detalle', pk=pk)
        else:
            messages.error(request, mensaje)
            return redirect('citas:detalle', pk=pk)
    
    # Mostrar confirmación
    return render(request, 'citas/cancelar_confirmar.html', {
        'cita': cita,
        'puede_cancelar': puede_cancelar,
        'mensaje': mensaje
    })

@login_required
def confirmar_cita(request, pk):
    """Confirmar asistencia a una cita."""
    cita = get_object_or_404(Cita, pk=pk)
    
    if cita.estado == 'PROGRAMADA':
        cita.estado = 'CONFIRMADA'
        cita.save()
        messages.success(request, 'Asistencia confirmada exitosamente.')
    else:
        messages.warning(request, 'Solo se pueden confirmar citas programadas.')
    
    return redirect('citas:detalle', pk=pk)

@login_required
def reprogramar_cita(request, pk):
    """Reprogramar una cita (HU-014)."""
    cita = get_object_or_404(Cita, pk=pk)
    if request.user.rol == 'PROPIETARIO' and cita.propietario.usuario_id != request.user.id:
        messages.error(request, 'No tienes permisos para gestionar esta cita.')
        return redirect('citas:detalle', pk=pk)
    
    puede_reprogramar, mensaje = cita.puede_reprogramar(request.user)
    
    if not puede_reprogramar:
        messages.error(request, mensaje)
        return redirect('citas:detalle', pk=pk)
    
    if request.method == 'POST':
        nueva_fecha = request.POST.get('fecha')
        nueva_hora = request.POST.get('hora')
        
        cita.fecha = nueva_fecha
        cita.hora = nueva_hora
        cita.save()
        crear_evento_cita(
            actor=request.user,
            cita=cita,
            tipo='SISTEMA',
            asunto='Cita reprogramada',
            mensaje=f'La cita #{cita.id} fue reprogramada para {nueva_fecha} a las {nueva_hora}'
        )
        
        messages.success(request, 'Cita reprogramada exitosamente.')
        return redirect('citas:detalle', pk=pk)
    
    return render(request, 'citas/reprogramar.html', {'cita': cita})
