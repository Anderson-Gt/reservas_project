from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recurso, Reserva, NoDisponibilidad

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['recurso', 'fecha_inicio', 'fecha_fin']

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fecha_inicio')
        fin = cleaned_data.get('fecha_fin')
        if inicio and fin and inicio >= fin:
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")
        return cleaned_data

class BloqueoForm(forms.ModelForm):
    class Meta:
        model = NoDisponibilidad
        fields = ['recurso', 'fecha_inicio', 'fecha_fin', 'motivo']

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fecha_inicio')
        fin = cleaned_data.get('fecha_fin')
        if inicio and fin and inicio >= fin:
            raise forms.ValidationError("La fecha de fin debe ser mayor que la fecha de inicio.")
        return cleaned_data
