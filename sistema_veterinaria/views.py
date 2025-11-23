from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """Vista principal del sistema (dashboard)."""
    # Todos los usuarios ven su dashboard personalizado
    context = {
        'user': request.user,
    }
    return render(request, 'home.html', context)