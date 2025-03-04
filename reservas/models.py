from django.db import models
from django.contrib.auth.models import User

class Recurso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name='reservas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reserva #{self.id} - {self.recurso.nombre}"

class NoDisponibilidad(models.Model):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name='no_disponible')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    motivo = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Bloqueo {self.recurso.nombre} del {self.fecha_inicio} al {self.fecha_fin}"
