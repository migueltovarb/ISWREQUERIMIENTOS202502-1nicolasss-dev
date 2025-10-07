# La clase de contacto y defino todas las funciones necesarias

class Contacto:
    def __init__(self, nombre, telefono, correo, cargo):
        # Valido que el nombre solo tenga letras y espacios
        if not self.validar_nombre(nombre):
            raise ValueError("El nombre solo puede contener letras y espacios")
        
        # Valido que el telefono solo tenga numeros
        if not self.validar_telefono(telefono):
            raise ValueError("El telefono solo puede contener numeros")
            
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.cargo = cargo
    
    def validar_nombre(self, nombre):
        # Funcion para validar que el nombre solo tenga letras
        # Acepto espacios tambien porque los nombres pueden tener espacios
        return nombre.replace(" ", "").isalpha()
    
    def validar_telefono(self, telefono):
        # Funcion para validar que el telefono solo tenga numeros
        # isdigit() para verificar que solo sean numeros
        return telefono.isdigit()

    def verNombre(self):
        return self.nombre

    def editarNombre(self, nombre):
        self.nombre = nombre

    def verTelefono(self):
        return self.telefono
    
    def editarTelefono(self, telefono):
        self.telefono = telefono

    def verCorreo(self):
        return self.correo
    
    def editarCorreo(self, correo):
        self.correo = correo
        
    def verCargo(self):
        return self.cargo
    
    def editarCargo(self, cargo):
        self.cargo = cargo