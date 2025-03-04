from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Recurso, Reserva, NoDisponibilidad
from .forms import RegistroUsuarioForm, ReservaForm, BloqueoForm

def inicio(request):
    """Página de inicio."""
    return render(request, 'reservas/index.html')

def registro(request):
    """Registro de nuevo usuario."""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Usuario registrado correctamente. ¡Puedes iniciar sesión!")
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'reservas/register.html', {'form': form})

def login_view(request):
    """Iniciar sesión."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Has iniciado sesión.")
            return redirect('inicio')
        else:
            messages.error(request, "Credenciales inválidas. Intenta de nuevo.")
    else:
        form = AuthenticationForm()
    return render(request, 'reservas/login.html', {'form': form})

def logout_view(request):
    """Cerrar sesión."""
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('inicio')

class RecursoListView(ListView):
    """Lista de recursos."""
    model = Recurso
    template_name = 'reservas/recurso_list.html'
    context_object_name = 'recursos'

class RecursoDetailView(DetailView):
    """Detalle de un recurso."""
    model = Recurso
    template_name = 'reservas/recurso_detail.html'
    context_object_name = 'recurso'

class ReservaListView(LoginRequiredMixin, ListView):
    """Lista de reservas del usuario."""
    model = Reserva
    template_name = 'reservas/reserva_list.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user).order_by('-creada_en')

@login_required
def crear_reserva(request):
    """Crear una nueva reserva."""
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.estado = 'confirmada'
            reserva.save()
            messages.success(request, f"Reserva creada correctamente para {reserva.recurso.nombre}.")
            return redirect('reserva_list')
    else:
        form = ReservaForm()
    return render(request, 'reservas/reserva_form.html', {'form': form})

@login_required
def detalle_reserva(request, pk):
    """Detalle de una reserva específica del usuario."""
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    return render(request, 'reservas/reserva_detail.html', {'reserva': reserva})

@login_required
def cancelar_reserva(request, pk):
    """Cancelar una reserva del usuario."""
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    if reserva.estado != 'cancelada':
        reserva.estado = 'cancelada'
        reserva.save()
        messages.info(request, "Reserva cancelada.")
    else:
        messages.warning(request, "La reserva ya estaba cancelada.")
    return redirect('reserva_list')

class BloqueoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Crear un bloqueo de disponibilidad para un recurso."""
    model = NoDisponibilidad
    form_class = BloqueoForm
    template_name = 'reservas/bloqueo_form.html'
    success_url = reverse_lazy('recurso_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        return super().form_valid(form)
