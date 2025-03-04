from django.contrib import admin
from .models import Recurso, Reserva, NoDisponibilidad

admin.site.register(Recurso)
admin.site.register(Reserva)
admin.site.register(NoDisponibilidad)
