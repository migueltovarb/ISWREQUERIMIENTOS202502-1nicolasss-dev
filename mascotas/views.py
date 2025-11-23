from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Mascota, TransferenciaMascota
from .forms import MascotaForm, TransferenciaMascotaForm
from propietarios.models import Propietario
from autenticacion.models import Usuario
from autenticacion.decorators import staff_required

@login_required
def registrar_mascota(request, propietario_id):
    """Registrar nueva mascota para un propietario (HU-008)."""
    propietario = get_object_or_404(Propietario, pk=propietario_id)
    if request.user.rol == 'PROPIETARIO' and propietario.usuario_id != request.user.id:
        return redirect('home')
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.propietario = propietario
            mascota.save()
            messages.success(request, f'Mascota {mascota.nombre} registrada exitosamente.')
            return redirect('propietarios:detalle', pk=propietario.pk)
    else:
        form = MascotaForm()
    
    return render(request, 'mascotas/formulario.html', {
        'form': form, 
        'titulo': f'Registrar Mascota para {propietario.nombre}',
        'propietario': propietario
    })

@login_required
def detalle_mascota(request, pk):
    """Ver detalles de una mascota."""
    mascota = get_object_or_404(Mascota, pk=pk)
    return render(request, 'mascotas/detalle.html', {'mascota': mascota})

@login_required
def editar_mascota(request, pk):
    """Editar información de mascota (HU-009)."""
    mascota = get_object_or_404(Mascota, pk=pk)
    if request.user.rol == 'PROPIETARIO' and mascota.propietario.usuario_id != request.user.id:
        return redirect('home')
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información de mascota actualizada.')
            return redirect('propietarios:detalle', pk=mascota.propietario.pk)
    else:
        form = MascotaForm(instance=mascota)
    
    return render(request, 'mascotas/formulario.html', {
        'form': form, 
        'titulo': f'Editar Mascota: {mascota.nombre}',
        'propietario': mascota.propietario
    })


@login_required
@staff_required
def transferir_mascota(request):
    """Transferir una mascota de un propietario a otro (HU-010) - Solo staff."""
    if request.method == 'POST':
        form = TransferenciaMascotaForm(request.POST)
        if form.is_valid():
            mascota = form.cleaned_data['mascota']
            nuevo_propietario = form.cleaned_data['nuevo_propietario']
            motivo = form.cleaned_data.get('motivo', '')
            
            # Guardar propietario anterior
            propietario_anterior = mascota.propietario
            
            # Crear registro de transferencia
            transferencia = TransferenciaMascota.objects.create(
                mascota=mascota,
                propietario_anterior=propietario_anterior,
                propietario_nuevo=nuevo_propietario,
                usuario_responsable=request.user,
                motivo=motivo
            )
            
            # Actualizar propietario de la mascota
            mascota.propietario = nuevo_propietario
            mascota.save()
            
            messages.success(
                request, 
                f'Mascota {mascota.nombre} transferida exitosamente de {propietario_anterior.nombre} a {nuevo_propietario.nombre}.'
            )
            return redirect('propietarios:detalle', pk=nuevo_propietario.pk)
    else:
        form = TransferenciaMascotaForm()
    
    return render(request, 'mascotas/transferir.html', {
        'form': form,
        'titulo': 'Transferir Mascota'
    })
