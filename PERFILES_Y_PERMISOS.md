# GUÍA DE PERFILES Y PERMISOS - MyDOG

## 🔑 **CREDENCIALES POR ROL**

### 👨‍💼 **Administrador**
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:**
  - ✅ Acceso COMPLETO al sistema
  - ✅ Django Admin
  - ✅ Crear usuarios (veterinarios, administrativos)
  - ✅ Ver reportes
  - ✅ Gestión de propietarios y mascotas
  - ✅ Calendario de citas
  - ✅ Registrar historiales clínicos
  - ✅ Pagos y facturas
  - ✅ Puede omitir restricciones de tiempo en citas

### 👨‍⚕️ **Veterinario 1**
- **Usuario:** `vet01`
- **Contraseña:** `vet123`
- **Nombre:** Dr. Carlos Veterinario
- **Permisos:**
  - ✅ Calendario de citas
  - ✅ Ver propietarios y mascotas
  - ✅ **Registrar historiales clínicos**
  - ✅ Ver historiales de todas las mascotas
  - ✅ Agendar citas
  - ✅ Ver pagos
  - ❌ Django Admin
  - ❌ Crear usuarios
  - ❌ Reportes

### 👩‍⚕️ **Veterinario 2**
- **Usuario:** `vet02`
- **Contraseña:** `vet123`
- **Nombre:** Dra. María López
- **Permisos:** Iguales a Veterinario 1

### 📋 **Personal Administrativo/Recepción**
- **Usuario:** `recepcion`
- **Contraseña:** `recep123`
- **Nombre:** Laura Recepcionista
- **Permisos:**
  - ✅ Calendario de citas
  - ✅ Agendar citas
  - ✅ Ver propietarios y mascotas
  - ✅ Registrar propietarios nuevos
  - ✅ Registrar pagos
  - ✅ Ver historiales (lectura)
  - ❌ **NO puede crear historiales clínicos** (solo veterinarios)
  - ❌ Django Admin
  - ❌ Reportes

### 👤 **Propietario 1**
- **Usuario:** `nicolas`
- **Contraseña:** `prop123`
- **Mascotas:** Pitulio (Perro Golden Retriever), Luna (Gato Siamés)
- **Permisos:**
  - ✅ Ver solo SUS mascotas
  - ✅ Ver historial clínico de SUS mascotas
  - ✅ Ver sus notificaciones
  - ❌ Calendario de citas
  - ❌ Agendar citas
  - ❌ Ver otros propietarios
  - ❌ Ver pagos de otros
  - ❌ Cualquier función administrativa

### 👤 **Propietario 2**
- **Usuario:** `juan`
- **Contraseña:** `prop123`
- **Mascotas:** Max (Labrador), Bella (Poodle)
- **Permisos:** Iguales a Propietario 1

### 👤 **Propietario 3**
- **Usuario:** `ana`
- **Contraseña:** `prop123`
- **Mascotas:** Michi (Gato Persa)
- **Permisos:** Iguales a Propietario 1

---

## 📊 **MATRIZ DE PERMISOS**

| Funcionalidad | Admin | Veterinario | Administrativo | Propietario |
|--------------|-------|-------------|----------------|-------------|
| Django Admin | ✅ | ❌ | ❌ | ❌ |
| Crear Usuarios | ✅ | ❌ | ❌ | ❌ |
| Reportes | ✅ | ❌ | ❌ | ❌ |
| Calendario Citas | ✅ | ✅ | ✅ | ❌ |
| Agendar Citas | ✅ | ✅ | ✅ | ❌ |
| Ver Propietarios | ✅ | ✅ | ✅ | Solo sí mismo |
| Registrar Propietarios | ✅ | ✅ | ✅ | ❌ |
| Ver Historiales | ✅ | ✅ | ✅ | Solo sus mascotas |
| **Crear Historiales** | ✅ | ✅ | ❌ | ❌ |
| Registrar Pagos | ✅ | ✅ | ✅ | ❌ |
| Ver Lista Pagos | ✅ | ✅ | ✅ | ❌ |
| Notificaciones | ✅ | ✅ | ✅ | ✅ |

---

## 🎯 **FLUJOS POR ROL**

### **Administrador:**
```
Login → Dashboard → Acceso a TODO
```

### **Veterinario:**
```
Login → Dashboard → Calendario → Ver Cita → Iniciar Consulta → Registrar Historial
```

### **Administrativo:**
```
Login → Dashboard → Calendario → Agendar Cita → Registrar Pago
```

### **Propietario:**
```
Login → Mis Mascotas → Ver Historial Médico de su Mascota
```

---

## 🔐 **SEGURIDAD IMPLEMENTADA**

- ✅ Decoradores `@staff_required` en vistas administrativas
- ✅ Decorador `@veterinario_required` para historiales clínicos
- ✅ Validación en templates (navbar dinámico según rol)
- ✅ Redirección automática según rol al hacer login
- ✅ Propietarios solo ven sus datos (Http404 si intentan acceder a otros)

---

## 🧪 **CÓMO PROBAR**

1. Inicia sesión con cada rol
2. Verifica que el navbar muestre solo las opciones permitidas
3. Prueba acceder a URLs directas (ej: `/propietarios/`) con un propietario → debe dar 404
4. Veterinarios: Pueden crear historiales
5. Administrativos: NO pueden crear historiales, pero sí citas y pagos
