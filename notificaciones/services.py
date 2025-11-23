from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notificacion, NotificacionLog


def push_user(user_id, payload):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{user_id}',
        {
            'type': 'notify',
            'data': payload,
        },
    )


def crear_evento_cita(actor, cita, tipo, asunto, mensaje):
    usuarios_objetivo = []
    if cita.propietario and cita.propietario.usuario_id:
        usuarios_objetivo.append(cita.propietario.usuario)
    if cita.veterinario:
        usuarios_objetivo.append(cita.veterinario)

    for u in usuarios_objetivo:
        n = Notificacion.objects.create(
            usuario=u,
            actor=actor,
            tipo=tipo,
            asunto=asunto,
            mensaje=mensaje,
            cita=cita,
            canal_enviado=getattr(getattr(u, 'preferencia_notificacion', None), 'canal_preferido', 'EMAIL'),
        )
        NotificacionLog.objects.create(notificacion=n, accion='CREADA', usuario=actor, detalles={'cita_id': cita.id})
        push_user(u.id, {
            'id': n.id,
            'tipo': n.tipo,
            'asunto': n.asunto,
            'mensaje': n.mensaje,
            'cita_id': cita.id,
        })
