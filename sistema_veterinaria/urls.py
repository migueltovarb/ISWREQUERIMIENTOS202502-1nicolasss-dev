"""
Configuración de URLs para el proyecto MyDOG.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    
    # URLs de aplicaciones (se descomentarán a medida que se implementen)
    path("autenticacion/", include("autenticacion.urls")),
    path("propietarios/", include("propietarios.urls")),
    path("mascotas/", include("mascotas.urls")),
    path("citas/", include("citas.urls")),
    path("historiales/", include("historiales.urls")),
    path("pagos/", include("pagos.urls")),
    path("notificaciones/", include("notificaciones.urls")),
    path("reportes/", include("reportes.urls")),
    # path("servicios/", include("servicios.urls")),
]

# Configuración para servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
