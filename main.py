from contacto import Contacto

# lista vacia de contactos donde guardo todos los contactos ( no se como funciona para hacer el csv :c )
contactos = []

# Funcion para buscar contactos por nombre o correo con un bucle for
def buscar_contacto(termino_busqueda):
    # Lista vacia para guardar los contactos encontrados
    contactos_encontrados = []
    for contacto in contactos:
        # Busco por nombre o por correo electronico
        if termino_busqueda.lower() in contacto.verNombre().lower() or termino_busqueda.lower() in contacto.verCorreo().lower():
            # El append es para agregar lo que se encuentre dentro de la anterior lista vacia
            contactos_encontrados.append(contacto)
    return contactos_encontrados

# Función para verificar si ya existe un correo en la lista con otro bucle for
def correo_ya_existe(correo):
    for contacto in contactos:
        if contacto.verCorreo().lower() == correo.lower():
            return True
    return False

# Funcion para mostrar el menu principal
def mostrar_menu():
    print()
    print('SISTEMA DE CONTACTOS CONNECTME')
    print('1. Ver lista de contactos')
    print('2. Añadir contacto')
    print('3. Buscar contacto')
    print('4. Eliminar contacto')
    print('5. Editar contacto')
    print('6. Salir')

# Funcion para ver todos los contactos
def ver_contactos():
    print('Ver lista de contactos')
    if len(contactos) == 0:
        print('No hay contactos en la lista')
    else:
        print(f'Total de contactos: {len(contactos)}')
        for i, contacto in enumerate(contactos, 1):
        
            print(f'{i}. Nombre: {contacto.verNombre()}, Telefono: {contacto.verTelefono()}, Correo: {contacto.verCorreo()}, Cargo: {contacto.verCargo()}')

# Funcion para añadir un nuevo contacto
def anadir_contacto():
    print('Añadir contacto')
    try:
        nombre = input('Ingrese el nombre del contacto: ')
        telefono = input('Ingrese el telefono del contacto: ')
        correo = input('Ingrese el correo del contacto: ')
        cargo = input('Ingrese el cargo del contacto: ')
        
        # Verifico que el correo no este repetido
        if correo_ya_existe(correo):
            print('Error: Ya existe un contacto con ese correo electronico')
            return
        
        # Creo el contacto con las validaciones
        contacto = Contacto(nombre, telefono, correo, cargo)
        contactos.append(contacto)
        print('Contacto añadido correctamente')
        
    # si hay un error se guarda en la variable e y se muestra
    except ValueError as e:
        print(f'Error: {e}')

# Funcion para buscar contactos
def buscar_contactos():
    print('Buscar contacto')
    if len(contactos) == 0:
        print('No hay contactos para buscar')
        return
    
    termino = input('Ingrese el nombre o correo a buscar: ')
    resultados = buscar_contacto(termino)
    
    if len(resultados) == 0:
        print('No se encontraron contactos con ese criterio')
    else:
        print(f'Se encontraron {len(resultados)} contacto(s):')
        for i, contacto in enumerate(resultados, 1):
            print(f'{i}. Nombre: {contacto.verNombre()}, Telefono: {contacto.verTelefono()}, Correo: {contacto.verCorreo()}, Cargo: {contacto.verCargo()}')

# Funcion para eliminar un contacto
def eliminar_contacto():
    print('Eliminar contacto')
    if len(contactos) == 0:
        print('No hay contactos para eliminar')
        return
    
    # Muestro la lista numerada para que el usuario elija
    print('Contactos disponibles:')
    for i, contacto in enumerate(contactos, 1):
        print(f'{i}. {contacto.verNombre()} - {contacto.verCorreo()}')
    
    try:
        indice = int(input('Ingrese el numero del contacto a eliminar: ')) - 1
        if 0 <= indice < len(contactos):
            contacto_eliminado = contactos.pop(indice)
            print(f'Contacto {contacto_eliminado.verNombre()} eliminado correctamente')
        else:
            print('Numero de contacto invalido')
    except ValueError:
        print('Por favor ingrese un numero valido')

# Funcion para editar un contacto
def editar_contacto():
    print('Editar contacto')
    if len(contactos) == 0:
        print('No hay contactos para editar')
        return
    
    # Muestro la lista numerada para que el usuario elija
    print('Contactos disponibles:')
    for i, contacto in enumerate(contactos, 1):
        print(f'{i}. {contacto.verNombre()} - {contacto.verCorreo()}')
    
    try:
        indice = int(input('Ingrese el numero del contacto a editar: ')) - 1
        if 0 <= indice < len(contactos):
            contacto = contactos[indice]
            print('Que desea editar?')
            print('1. Nombre')
            print('2. Telefono')
            print('3. Correo')
            print('4. Cargo')
            
            campo = input('Seleccione una opcion: ')
            
            if campo == '1':
                nuevo_nombre = input(f'Nombre actual: {contacto.verNombre()}. Nuevo nombre: ')
                if contacto.validar_nombre(nuevo_nombre):
                    contacto.editarNombre(nuevo_nombre)
                    print('Nombre actualizado correctamente')
                else:
                    print('Error: El nombre solo puede contener letras y espacios')
                    
            elif campo == '2':
                nuevo_telefono = input(f'Telefono actual: {contacto.verTelefono()}. Nuevo telefono: ')
                if contacto.validar_telefono(nuevo_telefono):
                    contacto.editarTelefono(nuevo_telefono)
                    print('Telefono actualizado correctamente')
                else:
                    print('Error: El telefono solo puede contener numeros')
                    
            elif campo == '3':
                nuevo_correo = input(f'Correo actual: {contacto.verCorreo()}. Nuevo correo: ')
                # Verifico que el nuevo correo no este repetido
                if correo_ya_existe(nuevo_correo) and nuevo_correo.lower() != contacto.verCorreo().lower():
                    print('Error: Ya existe un contacto con ese correo electronico')
                else:
                    contacto.editarCorreo(nuevo_correo)
                    print('Correo actualizado correctamente')
                    
            elif campo == '4':
                nuevo_cargo = input(f'Cargo actual: {contacto.verCargo()}. Nuevo cargo: ')
                contacto.editarCargo(nuevo_cargo)
                print('Cargo actualizado correctamente')
            else:
                print('Opcion invalida')
        else:
            print('Numero de contacto invalido')
    except ValueError:
        print('Por favor ingrese un numero valido')

# Aqui es la funcion que muestra el menu
def main():
    print('Sistema de Contactos ConnectMe')
    
    # El While true es para hacer un loop y que la interfaz siempre se este mostrando
    while True:
        mostrar_menu()
        opcion = input('Ingrese una opción: ')
        
        if opcion == '1':
            ver_contactos()
        elif opcion == '2':
            anadir_contacto()
        elif opcion == '3':
            buscar_contactos()
        elif opcion == '4':
            eliminar_contacto()
        elif opcion == '5':
            editar_contacto()
        elif opcion == '6':
            print('Saliendo del programa')
            print('Gracias por usar ConnectMe')
            break
        else:
            print('Opcion invalida, por favor seleccione una opcion del menu')

# Aqui se ejecuta el programa
if __name__ == "__main__":
    main()
