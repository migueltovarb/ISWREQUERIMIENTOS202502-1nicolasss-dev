"""
Configuración de Django para el proyecto MyDOG - Sistema de Gestión Veterinaria

Desarrollado para el curso de Ingeniería de Requisitos
Universidad Cooperativa de Colombia
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages

# Construir rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-mydog-2025-veterinaria-sistema-gestion"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

# Definición de aplicaciones instaladas
INSTALLED_APPS = [
    # Apps de Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
    
    # Apps personalizadas del proyecto MyDOG
    "autenticacion",          # Sistema de usuarios y roles
    "propietarios",           # Gestión de propietarios
    "mascotas",               # Gestión de mascotas
    "citas",                  # Agendamiento y calendario
    "historiales",            # Historiales clínicos
    "pagos",                  # Pagos y facturación simulados
    "notificaciones",         # Sistema de notificaciones simuladas
    "reportes",               # Generación de reportes
    "servicios",              # Gestión de servicios veterinarios
    "administracion",         # Panel admin y respaldos
    "channels",               # WebSockets (notificaciones en tiempo real)
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sistema_veterinaria.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Directorio global de templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",  # Para archivos de media
                "notificaciones.context_processors.notificaciones_unread",
            ],
        },
    },
]

WSGI_APPLICATION = "sistema_veterinaria.wsgi.application"
ASGI_APPLICATION = "sistema_veterinaria.asgi.application"

# Configuración de base de datos SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,  # Mínimo 8 caracteres según HU-002
        }
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'autenticacion.Usuario'

# Internacionalización - Español (Colombia)
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos (CSS, JavaScript, Imágenes)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuración de archivos de media (uploads de usuarios)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Tipo de campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración de sesiones (HU-003: Cierre automático después de 30 min)
SESSION_COOKIE_AGE = 1800  # 30 minutos en segundos
SESSION_SAVE_EVERY_REQUEST = True  # Renovar sesión en cada request
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Configuración de seguridad
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# Configuración de login
LOGIN_URL = "/autenticacion/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/autenticacion/login/"

# Configuración de email (para recuperación de contraseña - HU-002)
# En desarrollo, usar console backend para ver emails en consola
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# En producción, configurar SMTP real:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'mydog@example.com'
# EMAIL_HOST_PASSWORD = 'password'
# DEFAULT_FROM_EMAIL = 'MyDOG Sistema Veterinario <mydog@example.com>'

# Configuración de archivos de log
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "mydog.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "mydog": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Crear directorio de logs si no existe
os.makedirs(BASE_DIR / "logs", exist_ok=True)

# Configuración de mensajes de Django
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

# Configuración de django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Configuración de tamaño máximo de archivos (HU-020: Adjuntos máx 10MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB en bytes
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB en bytes

# Formatos de fecha y hora para templates
DATE_FORMAT = "d/m/Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = "d/m/Y H:i"
SHORT_DATE_FORMAT = "d/m/Y"
SHORT_DATETIME_FORMAT = "d/m/Y H:i"

# Horario laboral de la veterinaria (HU-011, HU-012)
HORARIO_LABORAL = {
    "hora_inicio": "08:00",
    "hora_fin": "18:00",
    "dias_laborales": [0, 1, 2, 3, 4, 5],  # Lunes (0) a Sábado (5)
}
# Canal de mensajes en memoria para desarrollo
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}
