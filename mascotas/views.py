from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Mascota, TransferenciaMascota
from .forms import MascotaForm
from propietarios.models import Propietario
from autenticacion.models import Usuario

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
