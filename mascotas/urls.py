from django.urls import path
from . import views

app_name = 'mascotas'

urlpatterns = [
    path('registrar/<int:propietario_id>/', views.registrar_mascota, name='registrar'),
    path('transferir/', views.transferir_mascota, name='transferir'),
    path('<int:pk>/', views.detalle_mascota, name='detalle'),
    path('<int:pk>/editar/', views.editar_mascota, name='editar'),
]
