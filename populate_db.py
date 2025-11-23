"""
Script completo de datos de prueba para MyDOG.
Ejecutar con: Get-Content populate_db.py | python manage.py shell
"""

from django.contrib.auth import get_user_model
from servicios.models import Servicio
from propietarios.models import Propietario
from mascotas.models import Mascota
from citas.models import Cita
from historiales.models import HistorialClinico
from pagos.models import Pago, Factura
from datetime import datetime, timedelta, time as dt_time
from django.utils import timezone

Usuario = get_user_model()

print("=== CREANDO DATOS DE PRUEBA PARA MYDOG ===\n")

# 1. USUARIOS
print("1. Creando usuarios...")
admin, created = Usuario.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@mydog.com',
        'first_name': 'Administrador',
        'last_name': 'Sistema',
        'rol': 'ADMIN'
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print("  ✓ Admin creado")
else:
    print("  - Admin ya existe")

vet1, created = Usuario.objects.get_or_create(
    username='vet01',
    defaults={
        'email': 'carlos@mydog.com',
        'first_name': 'Carlos',
        'last_name': 'Veterinario',
        'rol': 'VETERINARIO'
    }
)
if created:
    vet1.set_password('vet123')
    vet1.save()
    print("  ✓ Veterinario Dr. Carlos creado")

vet2, created = Usuario.objects.get_or_create(
    username='vet02',
    defaults={
        'email': 'maria@mydog.com',
        'first_name': 'María',
        'last_name': 'López',
        'rol': 'VETERINARIO'
    }
)
if created:
    vet2.set_password('vet123')
    vet2.save()
    print("  ✓ Veterinaria Dra. María creada")

admin_staff, created = Usuario.objects.get_or_create(
    username='recepcion',
    defaults={
        'email': 'recepcion@mydog.com',
        'first_name': 'Laura',
        'last_name': 'Recepcionista',
        'rol': 'ADMINISTRATIVO'
    }
)
if created:
    admin_staff.set_password('recep123')
    admin_staff.save()
    print("  ✓ Personal Administrativo Laura creado")

# 2. SERVICIOS
print("\n2. Creando servicios...")
servicios_data = [
    {'nombre': 'CONSULTA', 'duracion': 30, 'precio': 50000, 'color': '#00736A', 'desc': 'Consulta veterinaria general'},
    {'nombre': 'VACUNACION', 'duracion': 15, 'precio': 35000, 'color': '#0FF7750', 'desc': 'Aplicación de vacunas'},
    {'nombre': 'DESPARASITACION', 'duracion': 15, 'precio': 25000, 'color': '#F95C32', 'desc': 'Desparasitación interna y externa'},
    {'nombre': 'CIRUGIA', 'duracion': 120, 'precio': 300000, 'color': '#003535', 'desc': 'Procedimientos quirúrgicos'},
    {'nombre': 'CONTROL_PESO', 'duracion': 15, 'precio': 15000, 'color': '#00736A', 'desc': 'Control y seguimiento de peso'},
]

for s in servicios_data:
    servicio, created = Servicio.objects.get_or_create(
        nombre=s['nombre'],
        defaults={
            'duracion_minutos': s['duracion'],
            'precio': s['precio'],
            'color_calendario': s['color'],
            'descripcion': s['desc'],
            'activo': True
        }
    )
    if created:
        print(f"  ✓ Servicio {s['nombre']} creado")

# 3. PROPIETARIOS Y SUS USUARIOS
print("\n3. Creando propietarios...")
propietarios_data = [
    {'username': 'nicolas', 'nombre': 'Nicolas González', 'doc': '1234567890', 'tel': '3218795394', 'email': 'nicolas@email.com', 'dir': 'Calle 123 #45-67'},
    {'username': 'juan', 'nombre': 'Juan Pérez', 'doc': '9876543210', 'tel': '3101234567', 'email': 'juan@email.com', 'dir': 'Carrera 7 #12-34'},
    {'username': 'ana', 'nombre': 'Ana Martínez', 'doc': '5555555555', 'tel': '3159876543', 'email': 'ana@email.com', 'dir': 'Avenida 68 #100-20'},
]

propietarios = []
for p in propietarios_data:
    user, created = Usuario.objects.get_or_create(
        username=p['username'],
        defaults={
            'email': p['email'],
            'first_name': p['nombre'].split()[0],
            'last_name': ' '.join(p['nombre'].split()[1:]),
            'rol': 'PROPIETARIO'
        }
    )
    if created:
        user.set_password('prop123')
        user.save()
    
    propietario, created = Propietario.objects.get_or_create(
        documento=p['doc'],
        defaults={
            'usuario': user,
            'nombre': p['nombre'],
            'telefono': p['tel'],
            'correo': p['email'],
            'direccion': p['dir']
        }
    )
    propietarios.append(propietario)
    if created:
        print(f"  ✓ Propietario {p['nombre']} creado")

# 4. MASCOTAS
print("\n4. Creando mascotas...")
mascotas_data = [
    {'propietario': 0, 'nombre': 'Pitulio', 'especie': 'PERRO', 'raza': 'Golden Retriever', 'edad': 3, 'peso': 25.5, 'sexo': 'M'},
    {'propietario': 0, 'nombre': 'Luna', 'especie': 'GATO', 'raza': 'Siamés', 'edad': 2, 'peso': 4.2, 'sexo': 'H'},
    {'propietario': 1, 'nombre': 'Max', 'especie': 'PERRO', 'raza': 'Labrador', 'edad': 5, 'peso': 30.0, 'sexo': 'M'},
    {'propietario': 1, 'nombre': 'Bella', 'especie': 'PERRO', 'raza': 'Poodle', 'edad': 1, 'peso': 8.5, 'sexo': 'H'},
    {'propietario': 2, 'nombre': 'Michi', 'especie': 'GATO', 'raza': 'Persa', 'edad': 4, 'peso': 5.0, 'sexo': 'M'},
]

mascotas = []
for m in mascotas_data:
    mascota, created = Mascota.objects.get_or_create(
        nombre=m['nombre'],
        propietario=propietarios[m['propietario']],
        defaults={
            'especie': m['especie'],
            'raza': m['raza'],
            'edad': m['edad'],
            'peso': m['peso'],
            'sexo': m['sexo'],
            'activo': True
        }
    )
    mascotas.append(mascota)
    if created:
        print(f"  ✓ Mascota {m['nombre']} ({m['especie']}) creada")

# 5. CITAS
print("\n5. Creando citas...")
hoy = timezone.now().date()
servicios_list = list(Servicio.objects.all())

citas_data = [
    # Citas pasadas (completadas)
    {'mascota': 0, 'servicio': 1, 'vet': vet1, 'fecha': hoy - timedelta(days=15), 'hora': dt_time(10, 0), 'estado': 'COMPLETADA'},
    {'mascota': 2, 'servicio': 0, 'vet': vet2, 'fecha': hoy - timedelta(days=10), 'hora': dt_time(11, 0), 'estado': 'COMPLETADA'},
    {'mascota': 4, 'servicio': 1, 'vet': vet1, 'fecha': hoy - timedelta(days=5), 'hora': dt_time(14, 0), 'estado': 'COMPLETADA'},
    
    # Citas futuras (programadas)
    {'mascota': 0, 'servicio': 1, 'vet': vet1, 'fecha': hoy + timedelta(days=2), 'hora': dt_time(18, 0), 'estado': 'PROGRAMADA'},
    {'mascota': 1, 'servicio': 0, 'vet': vet2, 'fecha': hoy + timedelta(days=3), 'hora': dt_time(10, 0), 'estado': 'PROGRAMADA'},
    {'mascota': 3, 'servicio': 2, 'vet': vet1, 'fecha': hoy + timedelta(days=5), 'hora': dt_time(15, 0), 'estado': 'CONFIRMADA'},
]

citas = []
for c in citas_data:
    mascota = mascotas[c['mascota']]
    servicio = servicios_list[c['servicio']]
    
    cita, created = Cita.objects.get_or_create(
        mascota=mascota,
        fecha=c['fecha'],
        hora=c['hora'],
        defaults={
            'propietario': mascota.propietario,
            'servicio': servicio,
            'veterinario': c['vet'],
            'estado': c['estado'],
            'es_emergencia': False,
            'usuario_creador': admin
        }
    )
    citas.append(cita)
    if created:
        print(f"  ✓ Cita para {mascota.nombre} el {c['fecha']} creada")

# 6. HISTORIALES CLÍNICOS (para citas completadas)
print("\n6. Creando historiales clínicos...")
citas_completadas = [c for c in citas if c.estado == 'COMPLETADA']

historiales_data = [
    {'desc': 'Vacunación antirrábica. Paciente en buen estado general.', 'trat': 'Vacuna antirrábica anual. Próxima dosis en 1 año.'},
    {'desc': 'Consulta de rutina. Revisión general satisfactoria.', 'trat': 'Continuar con alimentación actual. Control en 6 meses.'},
    {'desc': 'Aplicación de vacuna triple. Sin reacciones adversas.', 'trat': 'Vacuna aplicada correctamente. Reposo por 24 horas.'},
]

for i, cita in enumerate(citas_completadas[:3]):
    historial, created = HistorialClinico.objects.get_or_create(
        cita=cita,
        mascota=cita.mascota,
        defaults={
            'veterinario': cita.veterinario,
            'fecha_consulta': cita.fecha,
            'diagnostico': historiales_data[i]['desc'],
            'tratamiento': historiales_data[i]['trat'],
            'evolucion': 'Favorable',
            'peso_actual': cita.mascota.peso
        }
    )
    if created:
        print(f"  ✓ Historial para {cita.mascota.nombre} creado")

# 7. PAGOS Y FACTURAS
print("\n7. Creando pagos y facturas...")
for cita in citas_completadas:
    if not Pago.objects.filter(cita=cita).exists():
        pago = Pago.objects.create(
            cita=cita,
            propietario=cita.propietario,
            monto=cita.servicio.precio,
            tipo_pago='EFECTIVO',
            estado='COMPLETADO',
            usuario_registro=admin
        )
        
        Factura.objects.create(
            pago=pago,
            propietario=cita.propietario,
            subtotal=pago.monto,
            impuestos=0,
            total=pago.monto
        )
        print(f"  ✓ Pago y factura para cita #{cita.id} creados")

print("\n=== DATOS DE PRUEBA CREADOS EXITOSAMENTE ===")
print("\nCREDENCIALES:")
print("  Admin: admin / admin123")
print("  Vet 1: vet01 / vet123")
print("  Vet 2: vet02 / vet123")
print("  Recepción: recepcion / recep123")
print("  Propietario 1: nicolas / prop123")
print("  Propietario 2: juan / prop123")
print("  Propietario 3: ana / prop123")
print("\nDATOS CREADOS:")
print(f"  - {Usuario.objects.count()} usuarios")
print(f"  - {Servicio.objects.count()} servicios")
print(f"  - {Propietario.objects.count()} propietarios")
print(f"  - {Mascota.objects.count()} mascotas")
print(f"  - {Cita.objects.count()} citas")
print(f"  - {HistorialClinico.objects.count()} historiales clínicos")
print(f"  - {Pago.objects.count()} pagos")
print(f"  - {Factura.objects.count()} facturas")
print("\n¡Listo para probar! Accede en: http://127.0.0.1:8001/")
