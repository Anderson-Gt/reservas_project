from django.core.management.base import BaseCommand
from reservas.models import Recurso

class Command(BaseCommand):
    help = 'Crea recursos de ejemplo en la base de datos'

    def handle(self, *args, **options):
        data = [
            {
                'nombre': 'Sala de Reuniones 1',
                'descripcion': 'Sala con proyector y 10 sillas',
                'ubicacion': 'Edificio A, Piso 3',
                'disponible': True
            },
            {
                'nombre': 'Laboratorio de Electrónica',
                'descripcion': 'Espacio con bancos de trabajo y equipo electrónico',
                'ubicacion': 'Edificio C, Piso 1',
                'disponible': True
            },
            {
                'nombre': 'Campo de Béisbol',
                'descripcion': 'Campo de césped natural para práctica de béisbol',
                'ubicacion': 'Zona deportiva',
                'disponible': True
            },
        ]

        for item in data:
            recurso, created = Recurso.objects.get_or_create(
                nombre=item['nombre'],
                defaults={
                    'descripcion': item['descripcion'],
                    'ubicacion': item['ubicacion'],
                    'disponible': item['disponible']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Recurso '{recurso.nombre}' creado."))
            else:
                self.stdout.write(self.style.WARNING(f"El recurso '{recurso.nombre}' ya existía."))
