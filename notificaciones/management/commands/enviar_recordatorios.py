"""
Comando de Django para enviar recordatorios automáticos de citas.

Este comando debe ejecutarse diariamente (mediante cron o Task Scheduler)
para enviar recordatorios a los propietarios 24 horas antes de sus citas.

Uso:
    python manage.py enviar_recordatorios

Configuración recomendada (cron):
    0 9 * * * cd /path/to/project && python manage.py enviar_recordatorios
    
Configuración recomendada (Windows Task Scheduler):
    Ejecutar diariamente a las 9:00 AM
    Acción: python manage.py enviar_recordatorios
    Directorio: C:\path\to\project
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from citas.models import Cita
from notificaciones.models import Notificacion, PreferenciasNotificacion
from notificaciones.services import crear_evento_cita


class Command(BaseCommand):
    help = 'Envía recordatorios automáticos de citas programadas para mañana'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra las citas que recibirían recordatorio sin enviarlos',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Calcular fecha de mañana
        hoy = timezone.now().date()
        manana = hoy + timedelta(days=1)
        
        self.stdout.write(
            self.style.SUCCESS(f'\n=== Enviando recordatorios para citas del {manana} ===\n')
        )
        
        # Buscar citas programadas o confirmadas para mañana
        citas_manana = Cita.objects.filter(
            fecha=manana,
            estado__in=['PROGRAMADA', 'CONFIRMADA']
        ).select_related('propietario', 'mascota', 'servicio', 'veterinario')
        
        total_citas = citas_manana.count()
        recordatorios_enviados = 0
        recordatorios_omitidos = 0
        
        if total_citas == 0:
            self.stdout.write(
                self.style.WARNING('No hay citas programadas para mañana.')
            )
            return
        
        self.stdout.write(f'Encontradas {total_citas} cita(s) para mañana.\n')
        
        for cita in citas_manana:
            propietario = cita.propietario
            
            # Verificar si el propietario tiene usuario asociado
            if not propietario.usuario_id:
                self.stdout.write(
                    self.style.WARNING(
                        f'  ⚠ Propietario {propietario.nombre} no tiene usuario asociado. '
                        f'Cita #{cita.id} omitida.'
                    )
                )
                recordatorios_omitidos += 1
                continue
            
            usuario = propietario.usuario
            
            # Verificar preferencias de notificación
            try:
                preferencias = PreferenciasNotificacion.objects.get(usuario=usuario)
                if not preferencias.recordatorios:
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠ {usuario.get_full_name()} tiene recordatorios desactivados. '
                            f'Cita #{cita.id} omitida.'
                        )
                    )
                    recordatorios_omitidos += 1
                    continue
                canal = preferencias.canal_preferido
            except PreferenciasNotificacion.DoesNotExist:
                # Si no tiene preferencias, usar EMAIL por defecto y enviar
                canal = 'EMAIL'
            
            # Verificar si ya existe un recordatorio para esta cita
            recordatorio_existente = Notificacion.objects.filter(
                usuario=usuario,
                cita=cita,
                tipo='RECORDATORIO'
            ).exists()
            
            if recordatorio_existente:
                self.stdout.write(
                    self.style.WARNING(
                        f'  ⚠ Ya existe recordatorio para cita #{cita.id}. Omitida.'
                    )
                )
                recordatorios_omitidos += 1
                continue
            
            # Preparar mensaje del recordatorio
            asunto = f'Recordatorio: Cita mañana a las {cita.hora.strftime("%H:%M")}'
            mensaje = (
                f'Hola {propietario.nombre},\n\n'
                f'Te recordamos que tienes una cita programada para mañana:\n\n'
                f'📅 Fecha: {cita.fecha.strftime("%d/%m/%Y")}\n'
                f'🕐 Hora: {cita.hora.strftime("%H:%M")}\n'
                f'🐾 Mascota: {cita.mascota.nombre}\n'
                f'💉 Servicio: {cita.servicio.get_nombre_display()}\n'
                f'👨‍⚕️ Veterinario: Dr. {cita.veterinario.get_full_name()}\n\n'
                f'Por favor, llega 10 minutos antes de tu cita.\n\n'
                f'Si necesitas reprogramar o cancelar, hazlo con al menos 6 horas de anticipación.\n\n'
                f'¡Te esperamos!\n'
                f'Equipo MyDOG'
            )
            
            if dry_run:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ [DRY RUN] Recordatorio para {usuario.get_full_name()} - '
                        f'Cita #{cita.id} ({cita.mascota.nombre} - {cita.servicio.get_nombre_display()})'
                    )
                )
                recordatorios_enviados += 1
            else:
                # Crear notificación de recordatorio
                try:
                    notificacion = Notificacion.objects.create(
                        usuario=usuario,
                        actor=usuario,  # El sistema actúa como el usuario
                        tipo='RECORDATORIO',
                        asunto=asunto,
                        mensaje=mensaje,
                        cita=cita,
                        canal_enviado=canal
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✓ Recordatorio enviado a {usuario.get_full_name()} - '
                            f'Cita #{cita.id} ({cita.mascota.nombre} - {cita.servicio.get_nombre_display()}) '
                            f'[Canal: {canal}]'
                        )
                    )
                    recordatorios_enviados += 1
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'  ✗ Error al enviar recordatorio para cita #{cita.id}: {str(e)}'
                        )
                    )
                    recordatorios_omitidos += 1
        
        # Resumen
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Resumen:\n'
                f'  • Total de citas mañana: {total_citas}\n'
                f'  • Recordatorios enviados: {recordatorios_enviados}\n'
                f'  • Recordatorios omitidos: {recordatorios_omitidos}\n'
            )
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠ Modo DRY RUN: No se enviaron recordatorios reales.\n'
                    'Ejecuta sin --dry-run para enviar los recordatorios.\n'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✅ Proceso completado exitosamente.\n')
            )
