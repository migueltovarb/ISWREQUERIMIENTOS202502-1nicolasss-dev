from .models import Notificacion


def notificaciones_unread(request):
    if getattr(request, 'user', None) and request.user.is_authenticated:
        count = Notificacion.objects.filter(usuario=request.user, leida=False).count()
        return {'notificaciones_unread': count}
    return {'notificaciones_unread': 0}
