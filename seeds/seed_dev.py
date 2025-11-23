import os
import sys
from datetime import timedelta, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_veterinaria.settings')
import django
django.setup()

from django.utils import timezone
from autenticacion.models import Usuario
from propietarios.models import Propietario
from mascotas.models import Mascota
from servicios.models import Servicio
from citas.models import Cita


def ensure_password(user, password):
    user.set_password(password)
    user.save()


def main():
    vet, created = Usuario.objects.get_or_create(
        username='vet1',
        defaults={
            'email': 'vet1@example.com',
            'rol': 'VETERINARIO',
            'first_name': 'Vet',
            'last_name': 'Uno',
        },
    )
    ensure_password(vet, 'Vet*12345')

    prop_user, _ = Usuario.objects.get_or_create(
        username='prop1',
        defaults={
            'email': 'prop1@example.com',
            'rol': 'PROPIETARIO',
            'first_name': 'Prop',
            'last_name': 'Uno',
        },
    )
    ensure_password(prop_user, 'Prop*12345')

    propietario, _ = Propietario.objects.get_or_create(
        usuario=prop_user,
        defaults={
            'nombre': 'Propietario Uno',
            'documento': '123456789',
            'telefono': '3001234567',
            'correo': 'prop1@example.com',
            'direccion': 'Calle 123',
        },
    )

    serv, _ = Servicio.objects.get_or_create(
        nombre='CONSULTA',
        defaults={
            'duracion_minutos': 30,
            'precio': 50000,
            'descripcion': 'Consulta general',
            'color_calendario': '#1E90FF',
        },
    )

    mascota, _ = Mascota.objects.get_or_create(
        propietario=propietario,
        nombre='Firulais',
        especie='PERRO',
        raza='Criollo',
        defaults={'edad': 3},
    )

    future_date = (timezone.now() + timedelta(days=2)).date()
    future_time = time(10, 0)

    cita, _ = Cita.objects.get_or_create(
        propietario=propietario,
        mascota=mascota,
        servicio=serv,
        veterinario=vet,
        fecha=future_date,
        hora=future_time,
        usuario_creador=vet,
        defaults={'estado': 'PROGRAMADA'},
    )

    print({
        'prop_login': {'username': 'prop1', 'password': 'Prop*12345'},
        'vet_login': {'username': 'vet1', 'password': 'Vet*12345'},
        'propietario_id': propietario.id,
        'mascota_id': mascota.id,
        'cita_id': cita.id,
    })


if __name__ == '__main__':
    main()
