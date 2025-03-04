from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('register/', views.registro, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('recursos/', views.RecursoListView.as_view(), name='recurso_list'),
    path('recurso/<int:pk>/', views.RecursoDetailView.as_view(), name='recurso_detail'),

    path('reservas/', views.ReservaListView.as_view(), name='reserva_list'),
    path('reservas/nueva/', views.crear_reserva, name='crear_reserva'),
    path('reservas/<int:pk>/', views.detalle_reserva, name='detalle_reserva'),
    path('reservas/<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),

    path('bloqueo/nuevo/', views.BloqueoCreateView.as_view(), name='bloqueo_nuevo'),
]
