from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import HistorialClinico, ArchivoHistorial
from .forms import HistorialClinicoForm, ArchivoHistorialForm
from mascotas.models import Mascota
from citas.models import Cita
from django.utils import timezone
from django.http import Http404
from autenticacion.decorators import veterinario_required

def es_veterinario(user):
    return user.rol == 'VETERINARIO' or user.es_admin()

@login_required
def historial_mascota(request, mascota_id):
    """Ver el historial clínico completo de una mascota."""
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    if request.user.rol == 'PROPIETARIO' and mascota.propietario.usuario_id != request.user.id:
        raise Http404
    historiales = mascota.historiales.all().order_by('-fecha_consulta')
    return render(request, 'historiales/lista_mascota.html', {'mascota': mascota, 'historiales': historiales})

@login_required
@veterinario_required
def registrar_consulta(request, mascota_id, cita_id=None):
    """
    Registrar una nueva consulta médica (HU-018) - Solo veterinarios.
    Puede venir vinculada a una cita específica o ser una consulta directa.
    """
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    cita = None
    if cita_id:
        cita = get_object_or_404(Cita, pk=cita_id)
    
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.mascota = mascota
            consulta.veterinario = request.user
            if cita:
                consulta.cita = cita
                # Actualizar estado de la cita a COMPLETADA
                cita.estado = 'COMPLETADA'
                cita.save()
            
            consulta.save()
            
            # Actualizar peso de la mascota si cambió
            if consulta.peso_actual:
                mascota.peso = consulta.peso_actual
                mascota.save()
                
            messages.success(request, 'Consulta registrada exitosamente.')
            return redirect('historiales:detalle', pk=consulta.pk)
    else:
        initial_data = {'fecha_consulta': timezone.now().date()}
        if cita:
            initial_data['fecha_consulta'] = cita.fecha
            
        form = HistorialClinicoForm(initial=initial_data)
    
    context = {
        'form': form,
        'mascota': mascota,
        'cita': cita,
        'titulo': f'Registrar Consulta - {mascota.nombre}'
    }
    return render(request, 'historiales/formulario.html', context)

@login_required
def detalle_historial(request, pk):
    """Ver detalle de una consulta específica y gestionar archivos."""
    historial = get_object_or_404(HistorialClinico, pk=pk)
    archivos = historial.archivos.all()
    
    if request.method == 'POST' and 'subir_archivo' in request.POST:
        archivo_form = ArchivoHistorialForm(request.POST, request.FILES)
        if archivo_form.is_valid():
            archivo = archivo_form.save(commit=False)
            archivo.historial = historial
            archivo.usuario = request.user
            archivo.save()
            messages.success(request, 'Archivo adjuntado exitosamente.')
            return redirect('historiales:detalle', pk=pk)
    else:
        archivo_form = ArchivoHistorialForm()
        
    return render(request, 'historiales/detalle.html', {
        'historial': historial,
        'archivos': archivos,
        'archivo_form': archivo_form
    })

@login_required
def mis_historiales(request):
    propietario = getattr(request.user, 'propietario', None)
    if request.user.rol == 'PROPIETARIO' and propietario is None:
        raise Http404
    mascotas = []
    if propietario:
        mascotas = propietario.mascotas.all().order_by('nombre')
    return render(request, 'historiales/mis_historiales.html', {'mascotas': mascotas})
