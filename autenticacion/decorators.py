"""
Decoradores personalizados para control de acceso por roles.
"""
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def staff_required(view_func):
    """
    Decorador que requiere que el usuario NO sea propietario.
    Solo permite acceso a Admin, Veterinario o Administrativo.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('autenticacion:login')
        
        if request.user.rol == 'PROPIETARIO':
            raise Http404  # Los propietarios no pueden acceder
        
        return view_func(request, *args, **kwargs)
    return wrapper

def propietario_required(view_func):
    """
    Decorador que requiere que el usuario sea propietario.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('autenticacion:login')
        
        if request.user.rol != 'PROPIETARIO':
            # Staff puede acceder también
            pass
        
        return view_func(request, *args, **kwargs)
    return wrapper

def es_veterinario_o_admin(user):
    """Función helper para verificar si es veterinario o admin."""
    return user.rol in ['VETERINARIO', 'ADMIN']

def es_staff(user):
    """Función helper para verificar si es staff (no propietario)."""
    return user.rol in ['ADMIN', 'VETERINARIO', 'ADMINISTRATIVO']

def veterinario_required(view_func):
    """
    Decorador que requiere que el usuario sea veterinario o admin.
    Solo permite crear historiales clínicos.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('autenticacion:login')
        
        if request.user.rol not in ['VETERINARIO', 'ADMIN']:
            raise Http404
        
        return view_func(request, *args, **kwargs)
    return wrapper
