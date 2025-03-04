from django.db import migrations

def seed_data(apps, schema_editor):
    Recurso = apps.get_model('reservas', 'Recurso')
    data = [
        {
            'nombre': 'Sala de Conferencias',
            'descripcion': 'Sala con proyector y capacidad para 50 personas',
            'ubicacion': 'Edificio A, Piso 2',
            'disponible': True
        },
        {
            'nombre': 'Aula de Computación',
            'descripcion': '15 ordenadores, proyector y aire acondicionado',
            'ubicacion': 'Edificio B, Piso 1',
            'disponible': True
        },
        {
            'nombre': 'Cancha de Fútbol',
            'descripcion': 'Campo de césped natural para partidos y entrenamientos',
            'ubicacion': 'Zona deportiva',
            'disponible': True
        },
    ]
    for item in data:
        Recurso.objects.get_or_create(
            nombre=item['nombre'],
            defaults={
                'descripcion': item['descripcion'],
                'ubicacion': item['ubicacion'],
                'disponible': item['disponible']
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0001_initial'),  # la migración inmediatamente anterior
    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
