from django.urls import path
from . import views

app_name = 'historiales'

urlpatterns = [
    path('mis/', views.mis_historiales, name='mis_mascotas'),
    path('mascota/<int:mascota_id>/', views.historial_mascota, name='lista_mascota'),
    path('registrar/<int:mascota_id>/', views.registrar_consulta, name='registrar'),
    path('registrar/<int:mascota_id>/cita/<int:cita_id>/', views.registrar_consulta, name='registrar_cita'),
    path('<int:pk>/', views.detalle_historial, name='detalle'),
]
