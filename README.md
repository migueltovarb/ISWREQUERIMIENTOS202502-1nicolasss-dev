# MyDOG - Sistema de Gestión Veterinaria

![MyDOG Logo](static/img/logo_mydog.png)

## Descripción

**MyDOG** es un sistema integral de gestión veterinaria desarrollado en Django que permite administrar citas, historiales clínicos, mascotas, propietarios, pagos y reportes de manera eficiente y segura.

**Lema:** "Cuidamos lo que más amas"

---

## Características Principales

✅ **Gestión de Citas** con calendario interactivo  
✅ **Historiales Clínicos** completos y trazables  
✅ **Sistema de Pagos** simulados con generación de facturas PDF  
✅ **Notificaciones** automáticas simuladas  
✅ **Reportes** en PDF y Excel  
✅ **Control de Acceso** basado en roles (RBAC)  
✅ **Diseño Responsive** adaptado a móvil, tablet y desktop  
✅ **Interfaz Minimalista** según styletile de marca  

---

## Requisitos del Sistema

- **Python:** 3.10 o superior
- **Django:** 4.2 o superior
- **Base de Datos:** SQLite (incluida por defecto)
- **Navegadores:** Chrome, Firefox, Edge, Safari (últimas 2 versiones)

---

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/migueltovarb/ISWREQUERIMIENTOS202502-1nicolasss-dev.git
cd PROYECTO_FINAL_DJANGO_NICOLAS
```

### 2. Crear Entorno Virtual

```powershell
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

```bash
python manage.py migrate
```

### 5. Cargar Datos Iniciales (Opcional)

```bash
python manage.py loaddata fixtures/initial_data.json
```

### 6. Crear Superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear un administrador del sistema.

### 7. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

Accede al sistema en: **http://localhost:8000**

---

## Logos y Recursos Visuales

El sistema utiliza dos placeholders para los logos de la marca:

### Logo del Header (Navbar)
- **Ubicación:** `static/img/${logo_header}.png`
- **Tamaño:** 48px de altura, ancho automático
- **Formato:** PNG con fondo transparente
- **Descripción:** Logo principal que aparece en la barra de navegación superior izquierda

### Logo del Footer
- **Ubicación:** `static/img/${logo_footer}.png`
- **Tamaño:** 32px de altura, ancho automático
- **Formato:** PNG con fondo transparente
- **Descripción:** Logo secundario que aparece centrado en el pie de página

> **Nota:** Reemplaza los placeholders `${logo_header}` y `${logo_footer}` con tus archivos de logo en formato PNG.

---

## Estructura del Proyecto

```
PROYECTO_FINAL_DJANGO_NICOLAS/
├── sistema_veterinaria/       # Proyecto Django principal
│   ├── settings.py            # Configuración general
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # WSGI config
├── autenticacion/             # App: Sistema de usuarios y roles
├── propietarios/              # App: Gestión de propietarios
├── mascotas/                  # App: Gestión de mascotas
├── citas/                     # App: Agendamiento y calendario
├── historiales/               # App: Historiales clínicos
├── pagos/                     # App: Pagos y facturación
├── notificaciones/            # App: Sistema de notificaciones
├── reportes/                  # App: Generación de reportes
├── servicios/                 # App: Gestión de servicios veterinarios
├── administracion/            # App: Panel admin y respaldos
├── static/                    # Archivos estáticos (CSS, JS, imágenes)
│   ├── css/                   # Hojas de estilo
│   ├── js/                    # JavaScript
│   └── img/                   # Imágenes y logos
├── media/                     # Archivos subidos por usuarios
├── templates/                 # Plantillas HTML
└── manage.py                  # Django management script
```

---

## Módulos del Sistema

### 1. Autenticación y Seguridad
- Inicio de sesión con control de intentos fallidos
- Recuperación de contraseña vía correo
- Cierre automático de sesión por inactividad (30 min)
- Gestión de roles: Administrador, Veterinario, Personal Administrativo, Propietario
- Logs de auditoría

### 2. Propietarios
- Registro con validación de unicidad (documento, correo)
- Modificación de información
- Búsqueda con filtros avanzados

### 3. Mascotas
- Registro asociado a propietario
- Edición de información
- Transferencia entre propietarios con historial

### 4. Citas (Calendario Interactivo)
- Agendamiento con validación en tiempo real
- Calendario visual con FullCalendar.js
- Reprogramación (mín 12h anticipación)
- Cancelación (mín 6h anticipación)
- Registro de emergencias sin restricciones
- Gestión de lista de espera

### 5. Historiales Clínicos
- Registro de diagnósticos y tratamientos
- Adjuntar archivos (PDF, JPG, PNG máx 10MB)
- Generación de certificados de vacunación en PDF
- Consulta por propietario o veterinario

### 6. Pagos y Facturación (Simulados)
- Simulación de pasarela de pago (siempre exitosa)
- Registro de pagos (Efectivo, Tarjeta, Transferencia)
- Generación automática de facturas PDF
- Historial de transacciones

### 7. Notificaciones (Simuladas)
- Confirmación al agendar cita
- Recordatorios 1-2 días antes
- Notificaciones de cancelación
- Configuración de preferencias de canal

### 8. Reportes
- Reportes de citas por fecha/estado/servicio
- Reportes de servicios más solicitados
- Reportes financieros
- Exportación en PDF y Excel

### 9. Servicios
- Configuración de servicios y duraciones
- Activación/desactivación de servicios

### 10. Administración
- Respaldos automáticos diarios
- Recuperación de respaldos
- Panel de administración

---

## Credenciales de Prueba

Después de cargar los datos iniciales, puedes usar estas credenciales:

### Administrador
- **Usuario:** `admin@mydog.com`
- **Contraseña:** `Admin123*`
- **Permisos:** Acceso completo a todas las funcionalidades

### Veterinario
- **Usuario:** `vet@mydog.com`
- **Contraseña:** `Vet123*`
- **Permisos:** Historiales clínicos, citas, consultas

### Personal Administrativo
- **Usuario:** `admin_personal@mydog.com`
- **Contraseña:** `Admin123*`
- **Permisos:** Citas, propietarios, mascotas, pagos

### Propietario
- **Usuario:** `propietario@mydog.com`
- **Contraseña:** `Prop123*`
- **Permisos:** Consulta de mascotas y citas propias

---

## Diseño UI/UX (Styletile)

El diseño del sistema sigue el styletile de la marca MyDOG:

### Paleta de Colores
- **Verde Oscuro (Primary):** `#00736A` - Profesionalismo
- **Verde Muy Oscuro (Secondary):** `#003535` - Solidez
- **Naranja (Accent):** `#F95C32` - Vitalidad
- **Verde Claro:** `#0FF7750` - Salud
- **Azul Claro:** `#F0F4FF` - Calma
- **Gris:** `#CCCBD1` - Limpieza

### Tipografía
- **Títulos:** Barlow Extra Bold
- **Subtítulos:** Montserrat Bold
- **Textos:** Montserrat Medium

### Principios de Diseño
- ❌ **NO** usar emojis
- ❌ **NO** usar degradados
- ❌ **NO** usar border-radius
- ✅ Diseño minimalista y profesional
- ✅ Espaciado en múltiplos de 8px

### Responsive Design
- **Móvil:** 320px - 767px
- **Tablet:** 768px - 1023px
- **Desktop:** 1024px+

---

## Testing

### Ejecutar Tests Automatizados

```bash
# Todos los tests
python manage.py test

# Tests de una app específica
python manage.py test autenticacion
python manage.py test citas
```

### Coverage

```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

---

## Tecnologías Utilizadas

### Backend
- **Django 4.2:** Framework web
- **SQLite:** Base de datos
- **Pillow:** Procesamiento de imágenes
- **ReportLab:** Generación de PDFs
- **openpyxl:** Exportación a Excel

### Frontend
- **HTML5:** Estructura semántica
- **CSS3:** Estilos personalizados
- **JavaScript ES6:** Interactividad
- **FullCalendar.js:** Calendario interactivo
- **Google Fonts:** Barlow y Montserrat

---

## Seguridad

- ✅ Contraseñas hasheadas con bcrypt/Argon2
- ✅ Control de acceso basado en roles (RBAC)
- ✅ Protección CSRF
- ✅ Validación de datos en frontend y backend
- ✅ Logs de auditoría para acciones críticas
- ✅ Bloqueo temporal después de 5 intentos fallidos
- ✅ Cifrado de datos sensibles (preparado para HTTPS)

---

## Cumplimiento Normativo

✅ **Ley 1581 de 2012 - Habeas Data (Colombia)**  
✅ **Trazabilidad completa** de acciones  
✅ **Confidencialidad** de datos médicos  
✅ **Auditoría inmutable** de registros críticos  

---

## Horario Laboral del Sistema

**Lunes a Sábado:** 8:00 AM - 6:00 PM  
**Domingos:** Cerrado  

> Las citas solo pueden agendarse dentro del horario laboral. Las emergencias no tienen restricciones de horario.

---

## Soporte Técnico

Para problemas técnicos o consultas:

- **Desarrollador:** Nicolás Alejandro Díaz Acosta
- **Email:** nicolas.diaz@campusucc.edu.co
- **GitHub:** [@nicolasss-dev](https://github.com/nicolasss-dev)

---

## Licencia

Proyecto académico desarrollado para el curso de **Ingeniería de Requisitos** de la carrera de **Ingeniería de Software**.

**Universidad:** Universidad Cooperativa de Colombia  
**Fecha:** Noviembre 2025  
**Versión:** 1.0

---

## Agradecimientos

- Equipo docente de Ingeniería de Requisitos
- Comunidad de Django
- Librería FullCalendar.js

---

🐾 **MyDOG - Cuidamos lo que más amas**
