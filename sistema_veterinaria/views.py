from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """Vista principal del sistema (dashboard)."""
    # Propietarios van directo a ver sus mascotas
    if request.user.rol == 'PROPIETARIO':
        return redirect('historiales:mis_mascotas')
    
    # Staff ve el dashboard tradicional
    context = {
        'user': request.user,
    }
    return render(request, 'home.html', context)