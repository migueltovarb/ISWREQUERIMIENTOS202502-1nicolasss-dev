from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('generar/', views.generar_reporte, name='generar'),
]
