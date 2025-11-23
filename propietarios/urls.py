from django.urls import path
from . import views

app_name = 'propietarios'

urlpatterns = [
    path('', views.lista_propietarios, name='lista'),
    path('registrar/', views.registrar_propietario, name='registrar'),
    path('<int:pk>/', views.detalle_propietario, name='detalle'),
    path('<int:pk>/editar/', views.editar_propietario, name='editar'),
]
