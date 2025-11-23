from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('', views.lista_notificaciones, name='lista'),
    path('admin/', views.admin_notificaciones, name='admin'),
    path('veterinario/', views.veterinario_notificaciones, name='veterinario'),
    path('propietario/', views.propietario_notificaciones, name='propietario'),
    path('api/mis/', views.api_mis_notificaciones, name='api_mis'),
    path('api/marcar-leida/<int:pk>/', views.api_marcar_leida, name='api_marcar_leida'),
    path('api/marcar-todas/', views.api_marcar_todas, name='api_marcar_todas'),
]
