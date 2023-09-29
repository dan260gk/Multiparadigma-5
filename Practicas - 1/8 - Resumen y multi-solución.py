# 8.1.-Definir una clase usuario que contenga como atributos: 
# Usuario
# Contraseña
# Rol
# Nombre
# CURP
# Ciudad

# 8.2.-Realizar un programa que contenga el siguiente menú 
# 1.- Registro
# 2.- Inicio de sesión
# 3.- Salida 
# La opción de registro solicitará al usuario registrarse solicitando la información de los atributos la clase 
# exceptuando el atributo Rol que por defecto será rol cliente, no se permitirán usuarios con CURP repetido en 
# caso de mostrar mensaje de “El usuario ya existe” 
# La opción de inicio de sesión permitirá al usuario introducir sus credenciales al ser correctas desplegar en 
# pantalla la información del usuario de lo contrario mostrar mensaje de “datos incorrectos“.

# 8.3.- Declarar un usuario con rol “Administrador” el cual al momento de iniciar sesión despliegue la información 
# de todos los usuarios registrados al momento.

class Usuario:
    def __init__(self, usuario, contraseña, nombre, curp, ciudad, rol="Cliente"):
        self._usuario = usuario
        self._contraseña = contraseña
        self._rol = rol
        self._nombre = nombre
        self._curp = curp
        self._ciudad = ciudad

usuariosRegistrados = []
admin = Usuario("admin", "password", "Brayan", "EIJ4KD92KEU93J83KK", "Nuevo Laredo", rol="Administrador")
usuariosRegistrados.append(admin)

def registrarUsuario():
    print("\nRegistro de Usuario\nIngrese lo que se le pida")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    nombre = input("Nombre: ")
    curp = input("CURP: ").upper()
    ciudad = input("Ciudad: ")
    
    for usuarioRegistrado in usuariosRegistrados:
        if usuarioRegistrado._curp == curp:
            print("El usuario ya existe")
            return
    
    usuarioNuevo = Usuario(usuario, contraseña, nombre, curp, ciudad)
    usuariosRegistrados.append(usuarioNuevo)
    print("Registro exitoso.")

def iniciarSesion():
    print("\nInicio de Sesion\nIngrese sus credenciales de acceso")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")    
    for usuarioRegistrado in usuariosRegistrados:
        if usuarioRegistrado._usuario == usuario and usuarioRegistrado._contraseña == contraseña and usuario != "admin":
            print("\nInicio de sesion exitoso.")
            print("Información del usuario:")
            print(f"Usuario: {usuarioRegistrado._usuario}")
            print(f"Contraseña: {usuarioRegistrado._contraseña}")
            print(f"Rol: {usuarioRegistrado._rol}")
            print(f"Nombre: {usuarioRegistrado._nombre}")
            print(f"CURP: {usuarioRegistrado._curp}")
            print(f"Ciudad: {usuarioRegistrado._ciudad}\n")
            return
        elif usuarioRegistrado._usuario == usuario and usuarioRegistrado._contraseña == contraseña and usuario == "admin":
            print("\nInformacion de todos los usuarios registrados:")
            mostrarInfo()
            return
    print("Datos incorrectos")
    

def mostrarInfo():
    for usuarioRegistrado in usuariosRegistrados:
            print(f"Usuario: {usuarioRegistrado._usuario}")
            print(f"Contraseña: {usuarioRegistrado._contraseña}")
            print(f"Rol: {usuarioRegistrado._rol}")
            print(f"Nombre: {usuarioRegistrado._nombre}")
            print(f"CURP: {usuarioRegistrado._curp}")
            print(f"Ciudad: {usuarioRegistrado._ciudad}\n")

while True:
    print("\nMenú:")
    print("1.- Registro")
    print("2.- Inicio de Sesion")
    print("3.- Salida")
    opcion = input("Seleccione una opcion: ")
    
    if opcion == "1":
        registrarUsuario()
    elif opcion == "2":
        iniciarSesion()
    elif opcion == "3":
        print("Saliendo...")
        break
    else:
        print("Opcion no válida.")

    
