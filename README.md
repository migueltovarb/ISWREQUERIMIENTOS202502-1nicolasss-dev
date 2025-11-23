# MyDOG - Sistema de Gestión Veterinaria

![MyDOG Logo](static/img/logo_mydog.png)

## Descripción

**MyDOG** es un sistema integral de gestión veterinaria desarrollado en Django que permite administrar citas, historiales clínicos, mascotas, propietarios, pagos y reportes de manera eficiente y segura.

**Lema:** "Cuidamos lo que más amas"

---

## Características Principales

✅ **Gestión de Citas** con calendario interactivo  
✅ **Historiales Clínicos** completos y trazables  
✅ **Recordatorios Automáticos** 24h antes de citas  
✅ **Sistema de Pagos** simulados con generación de facturas PDF  
✅ **Notificaciones** automáticas simuladas  
✅ **Certificados de Vacunación** en PDF  
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