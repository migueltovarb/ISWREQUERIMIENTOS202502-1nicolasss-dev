from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Propietario
from .forms import PropietarioForm
from autenticacion.models import Usuario
from autenticacion.decorators import staff_required

@login_required
@staff_required
def lista_propietarios(request):
    """Listar propietarios con búsqueda (solo staff)."""
    query = request.GET.get('q')
    if query:
        propietarios = Propietario.objects.filter(
            nombre__icontains=query
        ) | Propietario.objects.filter(
            documento__icontains=query
        )
    else:
        propietarios = Propietario.objects.all()
        
    return render(request, 'propietarios/lista.html', {'propietarios': propietarios})

@login_required
@staff_required
def registrar_propietario(request):
    """Registrar nuevo propietario (HU-005) - Solo staff."""
    if request.method == 'POST':
        form = PropietarioForm(request.POST)
        if form.is_valid():
            # Crear usuario asociado automáticamente (simplificado para este caso)
            # En un caso real, se pediría contraseña o se generaría una
            try:
                documento = form.cleaned_data['documento']
                email = form.cleaned_data['correo']
                nombre = form.cleaned_data['nombre']
                
                # Crear usuario base
                usuario = Usuario.objects.create_user(
                    username=documento,  # Usar documento como username
                    email=email,
                    password=documento,  # Contraseña temporal = documento
                    first_name=nombre.split()[0],
                    rol='PROPIETARIO'
                )
                
                propietario = form.save(commit=False)
                propietario.usuario = usuario
                propietario.save()
                
                messages.success(request, 'Propietario registrado exitosamente.')
                return redirect('propietarios:lista')
            except Exception as e:
                messages.error(request, f'Error al crear usuario: {str(e)}')
    else:
        form = PropietarioForm()
    
    return render(request, 'propietarios/formulario.html', {'form': form, 'titulo': 'Registrar Propietario'})

@login_required
def detalle_propietario(request, pk):
    """Ver detalles de un propietario (HU-007)."""
    propietario = get_object_or_404(Propietario, pk=pk)
    if request.user.rol == 'PROPIETARIO' and propietario.usuario_id != request.user.id:
        return redirect('home')
    
    # Obtener citas completadas pendientes de pago
    citas_pendientes_pago = propietario.citas.filter(
        estado='COMPLETADA',
        pagado=False
    ).select_related('mascota', 'servicio').order_by('-fecha', '-hora')
    
    return render(request, 'propietarios/detalle.html', {
        'propietario': propietario,
        'citas_pendientes_pago': citas_pendientes_pago
    })

@login_required
def editar_propietario(request, pk):
    """Editar información de propietario (HU-006)."""
    propietario = get_object_or_404(Propietario, pk=pk)
    if request.user.rol == 'PROPIETARIO' and propietario.usuario_id != request.user.id:
        return redirect('home')
    if request.method == 'POST':
        form = PropietarioForm(request.POST, instance=propietario)
        if request.user.rol == 'PROPIETARIO':
            form.fields['documento'].disabled = True
        if form.is_valid():
            if request.user.rol == 'PROPIETARIO':
                form.cleaned_data.pop('documento', None)
                form.instance.documento = propietario.documento
            form.save()
            messages.success(request, 'Información actualizada exitosamente.')
            return redirect('propietarios:detalle', pk=pk)
    else:
        form = PropietarioForm(instance=propietario)
        if request.user.rol == 'PROPIETARIO':
            form.fields['documento'].disabled = True
    
    return render(request, 'propietarios/formulario.html', {'form': form, 'titulo': 'Editar Propietario'})
