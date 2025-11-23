from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.calendario_citas, name='calendario'),
    path('api/eventos/', views.api_citas, name='api_eventos'),
    path('agendar/', views.agendar_cita, name='agendar'),
    path('<int:pk>/', views.detalle_cita, name='detalle'),
    path('<int:pk>/cancelar/', views.cancelar_cita, name='cancelar'),
    path('<int:pk>/confirmar/', views.confirmar_cita, name='confirmar'),
    path('<int:pk>/reprogramar/', views.reprogramar_cita, name='reprogramar'),
    path('ajax/cargar-mascotas/', views.cargar_mascotas, name='cargar_mascotas'),
]
