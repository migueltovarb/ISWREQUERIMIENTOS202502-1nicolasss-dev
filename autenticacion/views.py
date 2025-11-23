from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import LoginForm, RegistroUsuarioForm, RecuperacionPasswordForm
from .models import Usuario

def login_view(request):
    """Vista de inicio de sesión (HU-001)."""
    if request.user.is_authenticated:
        return redirect('home')  # Redirigir si ya está logueado
        
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.esta_bloqueado():
                    messages.error(request, f'Tu cuenta está bloqueada temporalmente hasta {user.bloqueado_hasta}.')
                elif not user.activo:
                    messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
                else:
                    login(request, user)
                    user.registrar_login_exitoso()
                    return redirect('home')
            else:
                # Intentar buscar el usuario para registrar intento fallido
                try:
                    user_attempt = Usuario.objects.get(username=username)
                    user_attempt.registrar_intento_fallido()
                    if user_attempt.intentos_fallidos >= 5:
                        messages.error(request, 'Has excedido el número de intentos. Tu cuenta ha sido bloqueada por 15 minutos.')
                    else:
                        messages.error(request, f'Credenciales inválidas. Intento {user_attempt.intentos_fallidos}/5.')
                except Usuario.DoesNotExist:
                    messages.error(request, 'Credenciales inválidas.')
        else:
            messages.error(request, 'Error en el formulario. Verifica tus datos.')
    else:
        form = LoginForm()
        
    return render(request, 'autenticacion/login.html', {'form': form})

def logout_view(request):
    """Vista de cierre de sesión."""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('autenticacion:login')

@login_required
@user_passes_test(lambda u: u.es_admin())
def registrar_usuario(request):
    """Vista para registrar nuevos usuarios (Solo Admin) (HU-027)."""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.username} creado exitosamente.')
            return redirect('autenticacion:registro')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'autenticacion/registro.html', {'form': form})

def recuperar_password(request):
    """Vista para solicitud de recuperación de contraseña (HU-002)."""
    if request.method == 'POST':
        form = RecuperacionPasswordForm(request.POST)
        if form.is_valid():
            # Aquí iría la lógica de envío de correo
            # Por ahora solo simulamos el éxito
            messages.success(request, 'Se han enviado las instrucciones a tu correo electrónico.')
            return redirect('autenticacion:login')
    else:
        form = RecuperacionPasswordForm()
        
    return render(request, 'autenticacion/recuperar_password.html', {'form': form})
