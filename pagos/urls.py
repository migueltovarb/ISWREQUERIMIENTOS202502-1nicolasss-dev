from django.urls import path
from . import views

app_name = 'pagos'

urlpatterns = [
    path('', views.lista_pagos, name='lista'),
    path('registrar/', views.registrar_pago, name='registrar'),
    path('registrar/cita/<int:cita_id>/', views.registrar_pago, name='registrar_cita'),
    path('<int:pk>/', views.detalle_pago, name='detalle'),
    path('factura/<int:pk>/print/', views.ver_factura, name='factura_print'),
]
