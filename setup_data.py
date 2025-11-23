"""
Script de datos iniciales para el sistema MyDOG.
Ejecutar con: python manage.py shell < setup_data.py
"""

from django.contrib.auth import get_user_model
from servicios.models import Servicio
from propietarios.models import Propietario

Usuario = get_user_model()

print("=== Creando datos iniciales para MyDOG ===\n")

# 1. Crear usuario administrador
if not Usuario.objects.filter(username='admin').exists():
    admin = Usuario.objects.create_superuser(
        username='admin',
        email='admin@mydog.com',
        password='admin123',
        first_name='Administrador',
        last_name='Sistema',
        rol='ADMIN'
    )
    print("✓ Usuario admin creado (user: admin, pass: admin123)")
else:
    print("- Usuario admin ya existe")

# 2. Crear veterinario de prueba
if not Usuario.objects.filter(username='vet01').exists():
    vet = Usuario.objects.create_user(
        username='vet01',
        email='veterinario@mydog.com',
        password='vet123',
        first_name='Dr. Carlos',
        last_name='Veterinario',
        rol='VETERINARIO'
    )
    print("✓ Veterinario creado (user: vet01, pass: vet123)")
else:
    print("- Veterinario ya existe")

# 3. Crear servicios básicos
servicios_data = [
    {'nombre': 'CONSULTA', 'duracion_minutos': 30, 'precio': 50000, 'color': '#00736A'},
    {'nombre': 'VACUNACION', 'duracion_minutos': 15, 'precio': 35000, 'color': '#0FF7750'},
    {'nombre': 'DESPARASITACION', 'duracion_minutos': 15, 'precio': 25000, 'color': '#F95C32'},
    {'nombre': 'CIRUGIA', 'duracion_minutos': 120, 'precio': 300000, 'color': '#003535'},
    {'nombre': 'CONTROL_PESO', 'duracion_minutos': 15, 'precio': 15000, 'color': '#00736A'},
]

for servicio_data in servicios_data:
    if not Servicio.objects.filter(nombre=servicio_data['nombre']).exists():
        Servicio.objects.create(
            nombre=servicio_data['nombre'],
            duracion_minutos=servicio_data['duracion_minutos'],
            precio=servicio_data['precio'],
            color_calendario=servicio_data['color'],
            descripcion=f"Servicio de {servicio_data['nombre'].lower()}",
            activo=True
        )
        print(f"✓ Servicio {servicio_data['nombre']} creado")
    else:
        print(f"- Servicio {servicio_data['nombre']} ya existe")

print("\n=== Datos iniciales creados correctamente ===")
print("\nCredenciales de acceso:")
print("  Admin: admin / admin123")
print("  Veterinario: vet01 / vet123")
print("\nPuedes acceder en: http://127.0.0.1:8001/admin/")
