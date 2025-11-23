from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pago, Factura
from .forms import PagoForm
from citas.models import Cita
from django.db import transaction
from autenticacion.decorators import staff_required

@login_required
@staff_required
def lista_pagos(request):
    """Listar historial de pagos (solo staff)."""
    pagos = Pago.objects.all().order_by('-fecha_pago')
    return render(request, 'pagos/lista.html', {'pagos': pagos})

@login_required
def registrar_pago(request, cita_id=None):
    """Registrar un nuevo pago, opcionalmente vinculado a una cita."""
    cita = None
    if cita_id:
        cita = get_object_or_404(Cita, pk=cita_id)
        # Verificar permisos
        if request.user.rol == 'PROPIETARIO' and cita.propietario.usuario_id != request.user.id:
            messages.error(request, 'No tienes permisos para pagar esta cita.')
            return redirect('home')
            
    # Buscar si ya existe un pago pendiente para esta cita
    pago_pendiente = None
    if cita:
        pago_pendiente = Pago.objects.filter(cita=cita, estado='PENDIENTE').first()
    
    if request.method == 'POST':
        form = PagoForm(request.POST, cita_id=cita_id, instance=pago_pendiente)
        if form.is_valid():
            with transaction.atomic():
                pago = form.save(commit=False)
                if cita:
                    pago.cita = cita
                    pago.propietario = cita.propietario
                    # Asegurar monto si estaba deshabilitado
                    pago.monto = cita.servicio.precio 
                
                pago.usuario_registro = request.user
                pago.estado = 'COMPLETADO' # Simulamos pago exitoso inmediato
                pago.save()
                
                # Marcar cita como pagada
                if cita:
                    cita.marcar_como_pagado()
                
                # Generar Factura Automáticamente
                Factura.objects.create(
                    pago=pago,
                    propietario=pago.propietario,
                    subtotal=pago.monto,
                    impuestos=0, # Simplificado
                    total=pago.monto
                )
                
                if cita:
                    messages.success(
                        request, 
                        f'Pago registrado exitosamente por {cita.servicio.get_nombre_display()} - {cita.mascota.nombre}. Factura generada.'
                    )
                else:
                    messages.success(request, 'Pago registrado y factura generada exitosamente.')
                
                return redirect('pagos:detalle', pk=pago.pk)
    else:
        form = PagoForm(cita_id=cita_id, instance=pago_pendiente)
    
    context = {
        'form': form,
        'cita': cita,
        'titulo': f'Pagar {cita.servicio.get_nombre_display()} - {cita.mascota.nombre}' if cita else 'Registrar Pago'
    }
    return render(request, 'pagos/formulario.html', context)

@login_required
def detalle_pago(request, pk):
    """Ver detalle de pago y factura."""
    pago = get_object_or_404(Pago, pk=pk)
    factura = pago.facturas.first() # Obtener la factura asociada
    return render(request, 'pagos/detalle.html', {'pago': pago, 'factura': factura})

@login_required
def ver_factura(request, pk):
    """Vista de impresión de factura."""
    factura = get_object_or_404(Factura, pk=pk)
    return render(request, 'pagos/factura_print.html', {'factura': factura})
